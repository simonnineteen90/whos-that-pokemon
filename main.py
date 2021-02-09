import pokebase as pb
import random
from flask import Flask, render_template, request,url_for, redirect


app = Flask(__name__)

# def random_pokemon():
#     id_num = random.randint(1,151)
#     name = pb.pokemon(id)
#     height = name.height
#     image = pb.SpriteResource('pokemon', id)
#     return f"No.{id_num} Name: {name} Height: {height}, Image path: {image.path}"

## use a decorator function to generate the poke data?
# cant work out how to access the pokemon name to check if the user guess is correct




def get_pokemon():
    id_num = random.randint(1, 151)
    pokemon = pb.pokemon(id_num)
    image = pb.SpriteResource('pokemon', id_num)
    new_pokemon = {
        "id_num": id_num,
        "name": pokemon,
        "height": pokemon.height,
        "image": image.url
    }
    return new_pokemon

new_pokemon = get_pokemon()


@app.route('/')
def random_pokemon(new_pokemon):
    return render_template('index.html', p_num=new_pokemon["id_num"], p_name=new_pokemon["name"],
                           p_height=new_pokemon["height"], p_image=new_pokemon["image"])



@app.route('/check_answer', methods=["POST"])
def check_answer():
    user_answer = request.form["guess"]
    if user_answer != "":
        return f"Check answer page. User answer = {user_answer}"
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