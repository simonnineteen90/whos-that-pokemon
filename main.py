import pokebase as pb
import random
from flask import Flask, render_template, request


app = Flask(__name__)

# def random_pokemon():
#     id_num = random.randint(1,151)
#     name = pb.pokemon(id)
#     height = name.height
#     image = pb.SpriteResource('pokemon', id)
#     return f"No.{id_num} Name: {name} Height: {height}, Image path: {image.path}"

## use a decorator function to generate the poke data?
# cant work out how to access the pokemon name to check if the user guess is correct


@app.route('/')
def random_pokemon():
    id_num = random.randint(1, 151)
    name = pb.pokemon(id_num)
    height = name.height
    image = pb.SpriteResource('pokemon', id_num)
    return render_template('index.html', p_num=id_num, p_name=name ,p_height=height, p_image=image.url)



@app.route('/check_answer', methods=["POST"])
def check_answer():
    user_answer = request.form["guess"]

    return f"Check answer page. User answer = {user_answer}"


if __name__ == "__main__":
    app.run(debug=True)