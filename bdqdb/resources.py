from random import choice

from flask import request
from flask.ext.restful import abort, reqparse, Resource

from bdqdb import api, db, models


class Root(Resource):

    def get(self):
        def remove_empty(tag):
            return len(tag['quotes']) != 0

        parser = reqparse.RequestParser()
        parser.add_argument('search', type=str, default=None,
                            location='args')
        parser.add_argument('random', type=bool, default=False,
                            location='args')
        args = parser.parse_args()

        tags = [t.to_json(search=args.search) for t in models.Tag.query.all()]
        tags = filter(remove_empty, tags)

        if len(tags) == 0:
            return tags

        if args.random:
            tag = choice(tags)
            while len(tag['quotes']) > 1:
                tag['quotes'].remove(choice(tag['quotes']))
            return tag
        else:
            return tags


class Tag(Resource):

    def get(self, tag):
        t = models.Tag.query.filter_by(name=tag).first()
        if t is None:
            msg = 'Tag %s not found' % tag
	    abort(404, message=msg)

        parser = reqparse.RequestParser()
        parser.add_argument('search', type=str, default=None,
                            location='args')
        parser.add_argument('random', type=bool, default=False,
                            location='args')
        args = parser.parse_args()

        if args.search is None:
            quotes = [q.to_json() for q in t.quotes]
        else:
            search_query = models.Quote.query.whoosh_search('"%s"' % args.search)
            quotes = [q.to_json() for q in t.quotes.intersect(search_query).all()]

        if len(quotes) == 0:
            return quotes

        if args.random:
            return choice(quotes)
        else:
            return quotes

    def post(self, tag):
        payload = request.get_json()
        text = payload.get('text', None)
        if text is None:
            abort(400)

        t = models.Tag.query.filter_by(name=tag).first()
        if t is None:
            t = models.Tag(tag)
            db.session.add(t)
            db.session.commit()

        quote = models.Quote(t.id, text)
        db.session.add(quote)
        db.session.commit()
        return quote.to_json(), 201


class TagWithId(Resource):

    def get(self, tag, qid):
	t = models.Tag.query.filter_by(name=tag).first()
        if t is None:
            msg = 'Tag %s not found' % tag
            abort(404, message=msg)

        for q in t.quotes:
            if q.id_within_tag == qid:
                return q.to_json()

        msg = 'No quote with id %d found for tag %s' % (qid, tag)
        abort(404, message=msg)

    def delete(self, tag, qid):
        t = models.Tag.query.filter_by(name=tag).first()
        if t is None:
            msg = 'Tag %s not found' % tag
            abort(404, message=msg)

        for q in t.quotes:
            if q.id_within_tag == qid:
                db.session.delete(q)
                if t.quotes.count() == 1:
                    db.session.delete(t)
                db.session.commit()
                return

        msg = 'No quote with id %d found for tag %s' % (qid, tag)
        abort(404, message=msg)


api.add_resource(Root, '/')
api.add_resource(Tag, '/<string:tag>')
api.add_resource(TagWithId, '/<string:tag>/<int:qid>')
