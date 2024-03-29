from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False, unique=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    todos = db.relationship("ToDos", backref="user" )
    contacts = db.relationship("Contacts", backref="user")
    memos = db.relationship("Memos", backref="user")

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.first_name, 
            "todos": list(map(lambda x: x.serialize(), self.todos)),
            "contacts": list(map(lambda y:y.serialize(), self.contacts)),
            "memos": list(map(lambda z:z.serialize(), self.memos))
        }
    
class ToDos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120), nullable=True)
    task = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ToDos {self.task}>'

    def serialize(self):
        return {
            "id": self.id,
            "task": self.task,
            "status": self.status,
            "notes": self.notes
        }

class Memos(db.Model):
    __tablename__ = 'memos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=True)
    memo_body = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Memos {self.title}>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "memo_body" : self.memo_body
        }

class Contacts(db.Model):
    __tablename__ = 'Contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=False)
    phone = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Contacts {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }
