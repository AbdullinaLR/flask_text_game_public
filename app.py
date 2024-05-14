from flask import Flask, render_template, redirect, url_for
from forms import CharacterForm
from models import db, Character

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Замените на свой секретный ключ

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Замените на URI вашей базы данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Маршрут для отображения формы создания персонажа
@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character(
            name=form.name.data,
            strength=form.strength.data,
            agility=form.agility.data
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('index'))  # Перенаправление на главную страницу после успешного создания персонажа
    return render_template('create_character.html', form=form)


# Маршрут для главной страницы
@app.route('/')
def index():
    characters = Character.query.all()
    return render_template('index.html', characters=characters)


if __name__ == '__main__':
    app.run(debug=True)
