import os
from flask import Flask, flash, request, send_file
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from flask import jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import base64
import io
import time

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if os.path.isdir('uploads'):
    pass
else:
    os.mkdir('uploads')


@app.route('/image', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            return "fail"

        file = request.files['file']

        season = request.form.get('season')
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        img = plt.imread(path)

        B1 = img[:, :, 0].mean()
        B2 = img[:, :, 1].mean()
        B3 = img[:, :, 2].mean()
        print("B1", B1)
        print("B2", B2)
        print("B3", B3)
        NDVI = (B1-B2)/(B1+B2)
        SR1 = (B1/B2)
        SR2 = (B1/B3)
        l = []
        sums = 0
        print("NDVI", NDVI)
        print("SR1", SR1)
        print("SR2", SR2)
        if season == "Harvesting":

            if 0 <= NDVI <= 0.4:
                l.append("vegetation and crop (leaves are turned to orange now)")
                sums += 2

            if 0.41 <= NDVI <= 0.6:
                l.append("healthy remaining soybean leaves")
                sums += 1

            if 0.61 <= NDVI <= 1:
                l.append("understory, branches etc")
                sums += 0

            if 0.0 <= SR1 <= 3.125:
                l.append("remaining green leaves and branches ")
                sums += 2

            if 3.126 <= SR1 <= 4.8:
                l.append("space between trees")
                sums += 1

            if 4.9 <= SR1 <= 50:
                l.append("branches, shadows, spaces between trees ")
                sum += 0

            if 1 <= SR2 <= 10:
                l.append("shadow, branches, spaces between trees")
                sums += 0

            if 11 <= SR2 <= 100:
                l.append("healthy remaining soybean leaves")
                sums += 1

            if SR2 > 100:
                l.append("green leaves")
                sums += 2

        if season == "Growing":
            if 0.0 <= NDVI <= 0.35:
                l.append("shadows, other sides of leaves and branches ")
                sums += 0

            if (0.36 <= NDVI <= 0.8) or (NDVI == 1):
                l.append("healthy soybean")
                sums += 2

            if 0.0 <= SR1 <= 3.125:
                l.append("vegetation ")
                sums += 1

            if 3.126 <= SR1 <= 4.8:
                l.append("healthy vegetations")
                sums += 2

            if 4.9 <= SR1 <= 50:
                l.append("branches, shadows, spaces between tree")
                sums += 0

            if 0.0 <= SR2 <= 3.2:
                l.append("shadow, branches, spaces between trees")
                sums += 0

            if 3.21 <= SR2 <= 12:
                l.append("healthy vegetation")
                sums += 2

    if (sums >= 2):
        sums = 2
    d = {
        1: "Moderate Health",
        2: "Healthy",
        0: "Un healthy"
    }
    print(sums)
    img = plt.imread(path)
    img = img/255
    print(path)
    b1 = img[:, :, 0]
    b2 = img[:, :, 1]

    img_shape = list(img.shape)
    conv_img = np.zeros((img_shape[0], img_shape[1]))
    for x in range(img_shape[0]):

        for y in range(img_shape[1]):

            conv_img[x][y] = abs((b1[x][y]-b2[x][y])/(b1[x][y]+b2[x][y]))
    print(conv_img)
    plt.imsave('ndvi.png', conv_img, cmap="gist_ncar_r")
    # time.sleep(20)

    im = Image.open("ndvi.png")
    data = io.BytesIO()
    im.save(data, "png")

    # print(base64.b64encode(data.getvalue()))
    base64string = str(base64.b64encode(data.getvalue()))[2:-1]

    os.remove(path)
    os.remove("ndvi.png")
    print(len(base64string))
    # os.remove("test.png")
    return jsonify({"Prediction": d[sums], "image": base64string})


if __name__ == '__main__':
    app.run()
