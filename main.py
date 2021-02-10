import pokebase as pb
import random
from flask import Flask, render_template, request,url_for, redirect, session


app = Flask(__name__)
# require a secret key to use session variable
app.secret_key = "secretPokemon"


@app.route('/')
def start():
    session['chosen_ids'] = []
    return render_template('index.html')


@app.route('/random_pokemon')
def random_pokemon():
    """
    Returns a random pokemon from pokebase / the API
    :return:
    """
    #session['chosen_ids'] = []
    id_num = random.randint(1, 151)

    # while the id_num is in the chosen_ids list generate another random number and check that number
    # to stop duplicate pokemon coming up
    while id_num in session['chosen_ids']:
        id_num = random.randint(1, 151)

    #if session['chosen_ids'] length is > 151 then the game is completed.

    session['chosen_ids'].append(id_num)
    print(session['chosen_ids'])
    pokemon = pb.pokemon(id_num)
    image = pb.SpriteResource('pokemon', id_num)
    height = pokemon.height
    session['pokemon_name'] = str(pokemon)
    print(f"Session variable = {session['pokemon_name']}")

    return render_template('random_pokemon.html', p_num=id_num, p_name=pokemon,
                           p_height=height, p_image=image.url)


@app.route('/check_answer', methods=["POST"])
def check_answer():
    """
    Recieves user answer via POST and checks against the session variable of the pokemon name
    returns route to correct/incorrect page
    :return:
    """
    user_answer = request.form["guess"]
    if user_answer != session['pokemon_name']:
        return render_template('incorrect.html')
    elif user_answer == session['pokemon_name']:
        return render_template('correct.html')
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
