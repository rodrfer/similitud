import os
import base64
import secrets
from flask import Flask, request, Response, render_template, url_for, flash, jsonify
from werkzeug.utils import secure_filename   
from PIL import Image

app = Flask(__name__)

def Similarity(img_ideal, img_to_compare):
    i1 = Image.open(img_ideal)
    i2 = Image.open(img_to_compare)
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
    ncomponents = i1.size[0] * i1.size[1] * 3
    diference_between_images = (dif / 255.0 * 100) / ncomponents
    # print ('Image: '+ " = Percentage of Similary:", str(round(100 - diference_between_images, 3)) + '%')
    similarity = str(round(100 - diference_between_images, 3))
    return similarity

@app.route('/', methods=["GET"])
def home():
    hello = "hola"
    return hello 

@app.route('/', methods=["POST"])
def index():
    if True: 
        value = request.json['image']
        base64_message = value
        png_recovered = base64.b64decode(base64_message)

        filename = "temp.png"
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(filename)
        picture_fn = random_hex + f_ext
        in_img = ('static/input_images/' + picture_fn)

        f = open(in_img, "wb")
        f.write(png_recovered)
        f.close()

        img_ideal = 'ideal.png'
        img_to_compare = in_img
        similarity = Similarity(img_ideal, img_to_compare)

        resp = jsonify({'message' : similarity})
        
        return resp

if __name__ == '__main__':
    app.run(debug=True)




