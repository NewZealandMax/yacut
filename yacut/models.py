from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(1024), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': f'http://localhost/{self.short}',
        }

    def from_dict(self, data):
        fields = {'original': 'url', 'short': 'custom_id'}
        for key, value in fields.items():
            setattr(self, key, data[value])
