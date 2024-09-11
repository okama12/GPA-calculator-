from app import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    programs = db.relationship('Program', backref='faculty', lazy=True)

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    subjects = db.relationship('Subject', backref='program', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)


    