from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Api, Resource
from models import db, Character
from forms import CharacterForm


app = Flask(__name__)
api = Api()
class Main(Resource): ## сможем обрабатывать гет пост и делит запросы
    def get(self):
        return {"info":"Some info", "num": 56}## ссоздаем джесон объект

## обработка url адреа
api.add_resource(Main,"/api/main")
api.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character(name=form.name.data, strength=form.strength.data, agility=form.agility.data)
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_character.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1") ## любые ошибки и уведы не выводятся в терминале
