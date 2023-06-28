from flask import Flask, request, render_template, redirect, url_for, session
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename
import numpy as np
import os
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'your_secret_key'

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
            'description': 'Batik Bali adalah hasil penyebaran Batik dari Pulau Jawa. Bali mempunyai potensi yang besar sebagai tempat bertumbuh dan berkembangnya batik, karena masyarakat Bali diketahui secara luas mempunyai kepandaian yang tinggi dalam olah seni.'
        },
        1: {
            'name': 'Batik Betawi',
            'description': 'Batik Betawi adalah kerajinan tradisional masyarakat Jakarta. Pembuatannya diawali pada abad ke-19. Motif awalnya mengikuti corak batik wilayah pesisir utara Pulau Jawa, yaitu bertemakan pesisiran. Corak batik Betawi dipearuhi oleh kebudayaan Tiongkok. Motif batik Betawi menggunakan kaligrafi khas Timur Tengah'
        },
        2: {
            'name': 'Batik Cendrawasih',
            'description': 'Batik Betawi adalah kerajinan tradisional masyarakat Jakarta. Pembuatannya diawali pada abad ke-19. Motif awalnya mengikuti corak batik wilayah pesisir utara Pulau Jawa, yaitu bertemakan pesisiran. Corak batik Betawi dipearuhi oleh kebudayaan Tiongkok. Motif batik Betawi menggunakan kaligrafi khas Timur Tengah'
        },
        # Tambahkan data batik lainnya di sini
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
        return render_template('index.html', error='No file selected.')

    file = request.files['image']

    if file.filename == '':
        return render_template('index.html', error='No file selected.')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        result = model_predict(file_path, model)

        # Simpan nama file gambar di sesi Flask
        session['image_name'] = filename

        # Arahkan ke halaman result.html
        return redirect(url_for('result'))
    else:
        return render_template('index.html', error='Invalid file format.')

@app.route('/result')
def result():
    # ...

    # Render template result.html
    return render_template('result.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
