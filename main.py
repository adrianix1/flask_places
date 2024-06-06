from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, URL, NumberRange

app = Flask(__name__)
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///place.db"
app.config['SECRET_KEY'] = 'very_secret_key'


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


class AddForm(FlaskForm):
    place = StringField('Place name', [DataRequired()])
    date = DateField('Date of visit', [DataRequired()])
    rating = IntegerField('Rating 1-5', [DataRequired(), NumberRange(1, 5)])
    location = StringField('Google location URL', [DataRequired(), URL()])
    submit_button = SubmitField('Submit Form')


class RatePlaceForm(FlaskForm):
    new_rating = StringField('New rating, eg 3', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
#
#
# with app.app_context():
#     db.create_all()
#
#     db.session.add_all([place1, place2])
#     db.session.commit()


@app.route("/")
def home():
    places = Place.query.all()
    return render_template("index.html", places=places)


@app.route('/add', methods=['GET', 'POST'])
def add_data():
    form = AddForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_entry = Place(
            place_name=form.place.data,
            visit_date=form.date.data.strftime("%d.%m.%Y"),
            rating=str(form.rating.data)+"/5",
            google_location=form.location.data
        )
        with app.app_context():
            db.session.add(new_entry)
            db.session.commit()
        return redirect("/", code=200)
    return render_template("add.html", form=form)


@app.route("/del/<id>")
def delete(id):
    with app.app_context():
        to_del = Place.query.get(id)
        db.session.delete(to_del)
        db.session.commit()
    return redirect("/", code=200)


@app.route("/update/<id>", methods=['GET', 'POST'])
def update(id):
    form = RatePlaceForm()
    place = db.session.execute(db.select(Place).filter_by(id=id)).scalar_one()
    if request.method == 'POST' and form.validate():
        place.rating = str(request.form['new_rating']) + "/5"
        db.session.commit()
        return redirect(url_for('home'), code=200)
    return render_template("edit.html", form=form, place_name=place.place_name)


if __name__ == '__main__':
    app.run(debug=True)
