from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import CharacterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    agility = db.Column(db.Integer, nullable=False)
    endurance = db.Column(db.Integer, nullable=False)
    story = db.Column(db.Text, default='')

    def __repr__(self):
        return f'<Character {self.name}>'

class CharacterAPI(Resource):
    def get(self, character_id):
        character = Character.query.get(character_id)
        if character:
            return {
                'id': character.id,
                'name': character.name,
                'strength': character.strength,
                'agility': character.agility,
                'endurance': character.endurance,
                'story': character.story
            }, 200
        return {"message": "Character not found"}, 404

    def put(self, character_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('strength', type=int)
        parser.add_argument('agility', type=int)
        parser.add_argument('endurance', type=int)
        args = parser.parse_args()

        character = Character.query.get(character_id)
        if character:
            character.name = args['name'] if args['name'] else character.name
            character.strength = args['strength'] if args['strength'] else character.strength
            character.agility = args['agility'] if args['agility'] else character.agility
            character.endurance = args['endurance'] if args['endurance'] else character.endurance
            db.session.commit()
            return {"message": "Character updated successfully"}, 200
        return {"message": "Character not found"}, 404

    def delete(self, character_id):
        character = Character.query.get(character_id)
        if character:
            db.session.delete(character)
            db.session.commit()
            return {"message": "Character deleted successfully"}, 200
        return {"message": "Character not found"}, 404

class CharacterListAPI(Resource):
    def get(self):
        characters = Character.query.all()
        return [{
            'id': char.id,
            'name': char.name,
            'strength': char.strength,
            'agility': char.agility,
            'endurance': char.endurance,
            'story': char.story
        } for char in characters], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('strength', type=int, required=True)
        parser.add_argument('agility', type=int, required=True)
        parser.add_argument('endurance', type=int, required=True)
        args = parser.parse_args()

        character = Character(name=args['name'], strength=args['strength'], agility=args['agility'], endurance=args['endurance'])
        db.session.add(character)
        db.session.commit()
        return {"message": "Character created successfully", "id": character.id}, 201

api.add_resource(CharacterAPI, '/api/character/<int:character_id>')
api.add_resource(CharacterListAPI, '/api/characters')

@app.route('/')
def index():
    characters = Character.query.all()
    return render_template('index.html', characters=characters)

@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character(name=form.name.data, strength=form.strength.data, agility=form.agility.data, endurance=form.endurance.data)
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_character.html', form=form)

@app.route('/character/<int:character_id>')
def character_detail(character_id):
    character = Character.query.get_or_404(character_id)
    return render_template('character_detail.html', character=character)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
