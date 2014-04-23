from bdqdb import db


class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    quotes = db.relationship('Quote',
                             backref='tag',
                             lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %s>' % self.name

    def to_json(self):
        return {
            'name': self.name,
            'quotes': [q.to_json() for q in self.quotes],
        }

    def count(self):
        return self.quotes.count()


class Quote(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    tag_id = db.Column(db.ForeignKey('tag.id'))
    id_within_tag = db.Column(db.Integer)

    def __init__(self, tag_id, text):
        self.tag_id = tag_id
        self.text = text

        tag = Tag.query.filter_by(id=self.tag_id).first()
        self.id_within_tag = tag.count()

    def __repr__(self):
        return '<Quote %s>' % self.text[:16]

    def to_json(self):
        return {
            'id': self.id_within_tag,
            'text': self.text,
        }
