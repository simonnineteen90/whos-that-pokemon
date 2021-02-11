import pokebase as pb
import random
from flask import Flask, render_template, request,url_for, redirect, session


app = Flask(__name__)
# require a secret key to use session variable
app.secret_key = "secretPokemon"


@app.route('/')
def start():
    session['chosen_ids'] = []
    session['user_score'] = 0
    return render_template('index.html')


@app.route('/random_pokemon')
def random_pokemon():
    """
    Returns a random pokemon from pokebase / the API
    :return:
    """
    #session['chosen_ids'] = []
    session['current_id_num'] = random.randint(1, 151)

    # while the id_num is in the chosen_ids list generate another random number and check that number
    # to stop duplicate pokemon coming up
    while session['current_id_num'] in session['chosen_ids']:
        session['current_id_num'] = random.randint(1, 151)


    session['chosen_ids'].append(session['current_id_num'])
    print(session['chosen_ids'])
    pokemon = pb.pokemon(session['current_id_num'])
    image = pb.SpriteResource('pokemon', session['current_id_num'])
    height = pokemon.height
    session['pokemon_name'] = str(pokemon)
    print(f"Session variable = {session['pokemon_name']}")


    return render_template('random_pokemon.html', p_num=session['current_id_num'], p_name=pokemon,
                           p_height=height, p_image=image.url, score=session['user_score'])


@app.route('/check_answer', methods=["POST"])
def check_answer():
    """
    Recieves user answer via POST and checks against the session variable of the pokemon name
    returns route to correct/incorrect page
    :return:
    """
    image = pb.SpriteResource('pokemon', session['current_id_num'])
    print(image)

    user_answer = request.form["guess"].lower()
    if user_answer != session['pokemon_name']:
        return render_template('incorrect.html', p_image=image.url, p_name=session['pokemon_name'])
    elif user_answer == session['pokemon_name']:
        session['user_score'] += 1
        if len(session['chosen_ids']) == 150:
            return "Congratulations you have named all 151. You are a pokemon master!"
        return render_template('correct.html', p_image=image.url, p_name=session['pokemon_name'])
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
