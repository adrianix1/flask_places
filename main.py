from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///place.db"


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Place(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    place_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    visit_date: Mapped[str]
    rating: Mapped[str]
    google_location: Mapped[str]


# add 2 records to db
# place1 = Place(place_name="Park Józefa Polińskiego",
#                visit_date="27.05.2024",
#                rating="4/5",
#                google_location="https://maps.app.goo.gl/81N1jDHhRxkPpTWj9")
#
# place2 = Place(place_name="Park Obwodu Praga Armii Krajowej",
#                visit_date="26.05.2024",
#                rating="3/5",
#                google_location="https://maps.app.goo.gl/MaAYKqBH8tEkfYjr6")


# with app.app_context():
#     db.create_all()
#
#     db.session.add_all([place1, place2])
#     db.session.commit()


@app.route("/")
def home():
    places = Place.query.all()
    return render_template("index.html", places=places)


if __name__ == '__main__':
    app.run(debug=True)
