import pokebase as pb
import random
from flask import Flask, render_template, request,url_for, redirect, session


app = Flask(__name__)
# require a secret key to use session variable
app.secret_key = "secretPokemon"

@app.route('/')
def random_pokemon():
    """
    Returns a random pokemon from pokebase / the API
    :return:
    """

    id_num = random.randint(1, 151)
    pokemon = pb.pokemon(id_num)
    image = pb.SpriteResource('pokemon', id_num)
    height = pokemon.height
    session['pokemon_name'] = str(pokemon)
    print(f"Session variable = {session['pokemon_name']}")

    return render_template('index.html', p_num=id_num, p_name=pokemon,
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
        return f" Incorrect answer. User answer = {user_answer}"
    elif user_answer == session['pokemon_name']:
        return f"correct answer! User answer = {user_answer}"
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
# update the user score
