# # from flask import Flask
# #
# # app = Flask(__name__)
# #
# #
# # @app.route('/')
# # def hello_world():  # put application's code here
# #     return 'Hello World!'
# #
# #
# # if __name__ == '__main__':
# #     app.run()
# from flask import Flask, render_template, request, redirect, url_for
# from models import db, Character
# from forms import CharacterForm
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///characters.db'
# #
# # config_name = os.getenv('FLASK_CONFIG') or 'default'
# # app.config.from_object(config[config_name])
# db.init_app(app)
#
# # @app.route('/characters', methods=['POST'])
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/create_character', methods=['GET', 'POST'])
# def create_character():
#     form = CharacterForm()
#     if form.validate_on_submit():
#         character = Character(name=form.name.data, strength=form.strength.data, agility=form.agility.data)
#         db.session.add(character)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('create_character.html', form=form)
#
# # def create_character():
# #     data = request.json
# #     new_character = Character(name=data['name'], strength=data['strength'], agility=data['agility'])
# #     db.session.add(new_character)
# #     db.session.commit()
# #     return jsonify({
# #         'id': new_character.id,
# #         'name': new_character.name,
# #         'strength': new_character.strength,
# #         'agility': new_character.agility,
# #         'message': 'Character created successfully.'
# #     }), 201
#
# if __name__ == '__main__':
#     app.run(debug=True)

#ffffffffffffffffffffffffffffffffffffffFF

# Писала Ангелина  )))))

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Character
from forms import CharacterForm
from config import config

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load configuration
config_name = os.getenv('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])

db.init_app(app)

@app.route('/')
def index():
    form = CharacterForm()
    return render_template('index.html', form=form)

@app.route('/characters', methods=['POST'])
def create_character():
    form = CharacterForm()
    if form.validate_on_submit():
        new_character = Character(
            name=form.name.data,
            strength=form.strength.data,
            agility=form.agility.data
        )
        db.session.add(new_character)
        db.session.commit()
        return jsonify({
            'id': new_character.id,
            'name': new_character.name,
            'strength': new_character.strength,
            'agility': new_character.agility,
            'message': 'Character created successfully.'
        }), 201
    return jsonify({'message': 'Form validation failed'}), 400

@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get_or_404(id)
    return jsonify({
        'id': character.id,
        'name': character.name,
        'strength': character.strength,
        'agility': character.agility
    })

@app.route('/characters/<int:id>', methods=['PUT'])
def update_character(id):
    character = Character.query.get_or_404(id)
    data = request.json
    character.strength = data.get('strength', character.strength)
    character.agility = data.get('agility', character.agility)
    db.session.commit()
    return jsonify({
        'id': character.id,
        'name': character.name,
        'strength': character.strength,
        'agility': character.agility,
        'message': 'Character updated successfully.'
    })

@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get_or_404(id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Character deleted successfully.'})

@app.route('/battle', methods=['POST'])
def battle():
    data = request.json
    char1 = Character.query.get_or_404(data['character1_id'])
    char2 = Character.query.get_or_404(data['character2_id'])
    if char1.strength + char1.agility > char2.strength + char2.agility:
        winner, loser = char1, char2
    else:
        winner, loser = char2, char1
    return jsonify({
        'winner': {
            'id': winner.id,
            'name': winner.name,
            'strength': winner.strength,
            'agility': winner.agility
        },
        'loser': {
            'id': loser.id,
            'name': loser.name,
            'strength': loser.strength,
            'agility': loser.agility
        },
        'message': f'{winner.name} won the battle against {loser.name}.'
    })

if __name__ == '__main__':
    app.run(debug=True)
