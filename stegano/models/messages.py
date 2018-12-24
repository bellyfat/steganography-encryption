from ..extensions import db
from datetime import datetime


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    share_to = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(), nullable=False)
    sent_on = db.Column(db.DateTime(), default=datetime.utcnow)
