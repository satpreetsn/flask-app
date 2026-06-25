from database.db import db

class User(db.Model):
    __tablename__ = "users"

    uid = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(255), nullable=False, unique=True )

    def to_dict(self):
        return{
            "uid" : self.uid,
            "name": self.name,
            "email" : self.email
        }