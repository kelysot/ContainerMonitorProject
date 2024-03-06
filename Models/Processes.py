from database import db


class Processes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    cpu_percent = db.Column(db.Float, nullable=False)
    memory_percent = db.Column(db.Float, nullable=False)
    cmdline = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, nullable=False)
    num_threads = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    num_fds = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

