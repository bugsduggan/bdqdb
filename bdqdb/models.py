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


class Quote(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    tag_id = db.Column(db.ForeignKey('tag.id'))

    def __init__(self, tag_id, text):
        self.tag_id = tag_id
        self.text = text

    def __repr__(self):
        return '<Quote %s>' % self.text[:16]

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
        }
