from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename
import numpy as np
import os
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = '12345'

model = load_model('CNN_Model.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def model_predict(img_path, model):
    img = load_img(img_path, target_size=(150, 150))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    preds = int(preds)  # Ubah ke integer

    batik_data = {
        0: {
            'name': 'Batik Bali',
            'description': 'Deskripsi Batik Bali'
        },
        1: {
            'name': 'Batik Jawa',
            'description': 'Deskripsi Batik Jawa'
        },
        2: {
            'name': 'Batik Sunda',
            'description': 'Deskripsi Batik Sunda'
        },
        3: {
            'name': 'Batik Sumatra',
            'description': 'Deskripsi Batik Sumatra'
        },
        4: {
            'name': 'Batik Kalimantan',
            'description': 'Deskripsi Batik Kalimantan'
        },
        5: {
            'name': 'Batik Papua',
            'description': 'Deskripsi Batik Papua'
        }
        # data batik belum semua
    }

    result = {
        'name': batik_data[preds]['name'],
        'description': batik_data[preds]['description']
    }

    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return redirect(url_for('result', status='gagal'))

    file = request.files['image']

    if file.filename == '':
        return redirect(url_for('result', status='gagal'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        result = model_predict(file_path, model)

        session['image_name'] = filename
        session['result'] = result

        return redirect(url_for('result', status='sukses'))
    else:
        return redirect(url_for('result', status='gagal'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    if 'image_name' not in session or 'result' not in session:
        status = request.args.get('status')
        if status == 'gagal':
            return render_template('result.html', result='Gagal Mendeteksi')
        else:
            return render_template('result.html', result=None)

    filename = session['image_name']
    result = session['result']

    return render_template('result.html', filename=filename, result=result)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.debug = True
    app.run(host='0.0.0.0', port=8080)