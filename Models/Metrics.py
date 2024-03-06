from database import db


class Metrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    cpu_percent = db.Column(db.Float, nullable=False)
    memory_used = db.Column(db.Integer, nullable=False)
    memory_percent = db.Column(db.Float, nullable=False)
    disk_percent = db.Column(db.Float, nullable=False)
    disk_used = db.Column(db.Integer, nullable=False)
    num_processes = db.Column(db.Integer, nullable=False)

