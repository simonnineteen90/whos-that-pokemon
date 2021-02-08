import pokebase as pb
import random
from flask import Flask, render_template


app = Flask(__name__)

# def random_pokemon():
#     id_num = random.randint(1,151)
#     name = pb.pokemon(id)
#     height = name.height
#     image = pb.SpriteResource('pokemon', id)
#     return f"No.{id_num} Name: {name} Height: {height}, Image path: {image.path}"


@app.route('/')
def random_pokemon():
    id_num = random.randint(1, 151)
    name = pb.pokemon(id_num)
    height = name.height
    image = pb.SpriteResource('pokemon', id_num)
    print(name)
    return render_template('index.html', p_num=id_num, p_name=name ,p_height=height, p_image=image.url)



if __name__ == "__main__":
    app.run(debug=True)