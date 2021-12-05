import os
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt

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


        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        img = plt.imread(path)
        print(type(img))
        print(img.shape)
        os.remove(path)
        return "success"

if __name__ == '__main__':
    app.run()
