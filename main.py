import pokebase as pb
import random
from flask import Flask, render_template, request,url_for, redirect
from flask import session as flask_session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# require a secret key to use session variable
app.secret_key = "secretPokemon"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# using SQL Alchemy to set up the leaderboard as an SQLite database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    score = db.Column(db.Integer, nullable=False, default='0')

    def __repr__(self):
        return f"User: {self.id}, {self.username}, {self.score}"


db.create_all()

@app.route('/')
def start():

    pika = pb.SpriteResource('pokemon', 25)
    flask_session['chosen_ids'] = []
    flask_session['user_score'] = 0

    return render_template('index.html', pikachu=pika.url)



@app.route('/leaderboard', methods=["POST"])
def leaderboard():
    new_leaderboard_name = request.form["leaderboard_name"]
    new_highscore= User(username=new_leaderboard_name, score=flask_session['user_score'])
    db.session.add(new_highscore)
    db.session.commit()

    leaderboard = User.query.all()
    return f"New name for leaderboard: {new_leaderboard_name}. Score:{flask_session['user_score']}" \
           f"<br/> Leaderboard data: {leaderboard}"


@app.route('/random_pokemon')
def random_pokemon():
    """
    Returns a random pokemon from pokebase / the API
    :return:
    """

    flask_session['current_id_num'] = random.randint(1, 151)

    # while the id_num is in the chosen_ids list generate another random number and check that number
    # to stop duplicate pokemon coming up
    while flask_session['current_id_num'] in flask_session['chosen_ids']:
        flask_session['current_id_num'] = random.randint(1, 151)

    # adds the current ID to the list of chosen IDs
    flask_session['chosen_ids'].append(flask_session['current_id_num'])
    print(flask_session['chosen_ids'])
    pokemon = pb.pokemon(flask_session['current_id_num']) # get the corresponding pokemon for the ID from the API
    image = pb.SpriteResource('pokemon', flask_session['current_id_num'])
    flask_session['pokemon_name'] = str(pokemon)
    print(f"flask_session variable = {flask_session['pokemon_name']}")

    return render_template('random_pokemon.html', p_num=flask_session['current_id_num'], p_name=pokemon,
                           p_image=image.url, score=flask_session['user_score'])


@app.route('/check_answer', methods=["POST"])
def check_answer():
    """
    Recieves user answer via POST and checks against the session variable of the pokemon name
    returns route to correct/incorrect page
    :return:
    """
    image = pb.SpriteResource('pokemon', flask_session['current_id_num'])
    print(image)

    user_answer = request.form["guess"].lower()
    if user_answer != flask_session['pokemon_name']:
        return render_template('incorrect.html', p_image=image.url, p_name=flask_session['pokemon_name'],
                               current_score=flask_session['user_score'])

    elif user_answer == flask_session['pokemon_name']:
        flask_session['user_score'] += 1
        if len(flask_session['chosen_ids']) == 150:
            return "Congratulations you have named all 151. You are a pokemon master!"
        return render_template('correct.html', p_image=image.url, p_name=flask_session['pokemon_name'])
    else:
        return redirect(url_for('random_pokemon'))


if __name__ == "__main__":
    app.run(debug=True)


# Display home page
# ask user if they want to play
# If yes generate a rnadom pokemon
# display the random pokemon
# get the user answer
# check user answer
# display page based on correct/incorrect answer
# if correct answer
#   update the user score
#   load next pokemon or quit
# elif incorrect answer
#   reset user score
#   reset pokemon list to empty
