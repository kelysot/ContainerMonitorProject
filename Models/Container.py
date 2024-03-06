from database import db


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column(db.String, nullable=False)
    memory_total = db.Column(db.Integer, nullable=False)
    disk_total = db.Column(db.Integer, nullable=False)

