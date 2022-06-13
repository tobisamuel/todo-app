from flask_sqlalchemy import SQLAlchemy

database_name = "test"
database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", "tobabes55", "localhost:5432", database_name
)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# Models
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, description, completed):
        self.title = title
        self.description = description
        self.completed = completed

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
        }
