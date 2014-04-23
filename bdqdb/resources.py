from flask import request
from flask.ext.restful import abort, Resource

from bdqdb import api, db, models


class Root(Resource):

    def get(self):
        return [t.to_json() for t in models.Tag.query.all()]


class Tag(Resource):

    def get(self, tag):
        t = models.Tag.query.filter_by(name=tag).first()
        if t is None:
	    abort(404)

        return [q.to_json() for q in t.quotes]

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
            abort(404)

        for q in t.quotes:
            if q.id == qid:
                return q.to_json()

        abort(404)

    def delete(self, tag, qid):
        t = models.Tag.query.filter_by(name=tag).first()
        if t is None:
            abort(404)

        for q in t.quotes:
            if q.id == qid:
                db.session.delete(q)
                if t.quotes.count() == 1:
                    db.session.delete(t)
                db.session.commit()
                return

        abort(404)


api.add_resource(Root, '/')
api.add_resource(Tag, '/<string:tag>')
api.add_resource(TagWithId, '/<string:tag>/<int:qid>')
