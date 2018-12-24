from ..extensions import db
from datetime import datetime


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    share_to = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(), nullable=False)
    sent_on = db.Column(db.DateTime(), default=datetime.utcnow)
    sent_by_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    sent_by = db.relationship(
        'Users',
        backref=db.backref('sent', lazy=True),
        foreign_keys=[sent_by_id]
    )
    sent_to_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=True)
    sent_to = db.relationship(
        'Users',
        backref=db.backref('inbox', lazy=True),
        foreign_keys=[sent_to_id]
    )
