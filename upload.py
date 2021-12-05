import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/image', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            return "fail"

        file = request.files['file']


        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        return "success"

if __name__ == '__main__':
    app.run()
