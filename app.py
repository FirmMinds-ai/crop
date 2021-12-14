import os
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from flask import jsonify

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
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
        B1 = img[:,:,0].mean()
        B2 = img[:,:,1].mean()
        B3 = img[:,:,2].mean()

        NDVI = ((B1-B2)/(B1+B2)
        SR1 = (B1/B2)
        SR2 = (B1/B3)

        if season == "Harvesting":
            l1 = []
            if 0 <= NDVI <= 0.4:
                l1.append("vegetation and crop (leaves are turned to orange now)")

            if 0.41 <= NDVI <= 0.6:
                l1.append("healthy remaining soybean leaves")

            if 0.61 <= NDVI <= 1 :
                l1.append("understory, branches etc")

            l2 = []
            if 0.0 <= SR1<= 3.125:
                l2.append("remaining green leaves and branches ")

            if 3.126 <= SR1<=  4.8 :
                l2.append("space between trees")

            if 4.9 <= SR1<= 50 :
                l2.append("branches, shadows, spaces between trees ")
            l3 = []

            if 1 <= SR2  <=  10 :
                l3.append("shadow, branches, spaces between trees")

            if 11 <= SR2  <= 100 :
                l3.append("healthy remaining soybean leaves")

            if SR2 >100 :
                l3.append("green leaves")

        if season == "Growing" :

            l1 = []

            if 0.0 <= NDVI <=  0.35:
                l1.append("shadows, other sides of leaves and branches ")

            if (0.36 <= NDVI <=  0.8 ) or (NDVI == 1)  :
                l1.append("healthy soybean")


            l2 = []
            if 0.0 <= SR1<= 3.125:
                l2.append("vegetation ")

            if 3.126 <= SR1<=  4.8 :
                l2.append("healthy vegetations")

            if 4.9 <= SR1<= 50 :
                l2.append("branches, shadows, spaces between tree")

            l3 = []

            if 0.0 <= SR2  <= 3.2 :
                l3.append("shadow, branches, spaces between trees")

            if 3.21 <= SR2  <= 12 :
                l3.append("healthy vegetation")


        d = {"output" :[l1,l2,l3]}





        print(type(img))
        print(img.shape)
        os.remove(path)
        return jsonify(d)

if __name__ == '__main__':
    app.run()
