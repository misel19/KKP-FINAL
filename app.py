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
    preds = np.argmax(preds, axis=1)[0]  # Ambil elemen pertama dari array

    batik_data = {
        0: {
            'name': 'Batik Bali',
            'description': 'Batik Bali adalah hasil penyebaran Batik dari Pulau Jawa. Bali mempunyai potensi yang besar sebagai tempat bertumbuh dan berkembangnya batik, karena masyarakat Bali diketahui secara luas mempunyai kepandaian yang tinggi dalam olah seni.'
        },
        1: {
            'name': 'Batik Betawi',
            'description': 'Batik Betawi adalah kerajinan tradisional masyarakat Jakarta. Pembuatannya diawali pada abad ke-19. Motif awalnya mengikuti corak batik wilayah pesisir utara Pulau Jawa, yaitu bertemakan pesisiran. Corak batik Betawi dipearuhi oleh kebudayaan Tiongkok. Motif batik Betawi menggunakan kaligrafi khas Timur Tengah.'
        },
        2: {
            'name': 'Batik Cendrawasih',
            'description': 'Cendrawasih merupakan jenis burung khas Papua yang sangat ikonik. Burung ini menjadi inspirasi motif batik cendrawasih. Biasanya motif ini memadukan gambar burung cendrawasih dengan gambar tumbuhan dan bunga khas Papua.'
        },
        3: {
            'name': 'Batik Dayak',
            'description': 'Motif batik Dayak mencerminkan budaya masyarakat Dayak. Istilah Dayak yang mempunyai arti “sungai”. Sehingga batik ini menggambarkan bermacam-macam aktivitas yang sering berkaitan dengan sungai. Secara umum batik Kalimantan memiliki ciri khas warna yang mencolok, berani, dan warna- warni.'
        },
        4: {
            'name': 'Batik Geblek Renteng',
            'description': 'Batik geblek renteng adalah sebuah miniature dan ideologi dasar Kulon Progo. Dapat dilihat pada batik geblek renteng yang juga menggunakan motif-motif representasi lainnya mengenai Kulon Progo seperti flora dan fauna asli, serta simbol dan lambang Kulon Progo yang juga menjadi ideologi dasar.'
        },
        5: {
            'name': 'Batik Ikat Celup',
            'description': 'Menurut sejarah, teknik celup ikat berasal dari tiongkok, teknik ini kemudian berkembang sampai keindia dan wilayah-wilayah nusantara. Pada batik celup ikat adalah proses membuat motif dan warna pada kainputih polos dengan teknik mengikat dan menutup sebagian kain dengan karet / raffia dan plastik gula pasir selanjutnya dicelup pada warna / pewarna kain misalnya wantex.'
        },
        6: {
            'name': 'Batik Insang',
            'description': 'Tenun Corak Insang adalah tenunan tradisional khas masyarakat suku Melayu di Kota Pontianak. Tenunan ini dikenal sejak masa Kesultanan Kadriah di bawah kekuasaan Sultan Syarif Abdurrahman Al Qadrie tahun 1771 hingga saat ini. Awalnya Corak Insang hanya digunakan oleh kaum bangsawan di Istana Kadriah. Fungsi tenun Corak Insang adalah sebagai penunjuk identitas status sosial bagi satu keluarga atau satu kelompok dalam kehidupan bermasyarakat dan saat diadakannya pertemuan antar kerajaan. Pada masa lampau, corak ini juga menjadi tolok ukur keterampilan anak gadis dalam menenun. Penggunaan tenun Corak Insang memiliki fungsi lain sebagai barang hadiah ulang tahun bagi raja, sebagai barang pengantar iringan pengantin dan pengantar sirih pinang pada acara pernikahan dan upacara-upacara tradisional lainnya.'
        },
        7: {
            'name': 'Batik Kawung',
            'description': ' Motif batik Kawung ini pertama kali dikenal pada abad ke 13 tepatnya di pulau Jawa. Batik Kawung adalah motif batik yang bentuknya berupa bulatan mirip buah kawung (sejenis kelapa atau kadang juga dianggap sebagai aren atau kolang-kaling) yang ditata rapi secara geometris. Kadang, motif ini juga ditafsirkan sebagai gambar bunga lotus (teratai) dengan empat lembar mahkota bunga yang merekah. Lotus adalah bunga yang melambangkan umur panjang dan kesucian.'
        },
        8: {
            'name': 'Batik Lasem',
            'description': 'Batik Lasem adalah salah satu jenis kain batik pesisiran yang merupakan hasil silang budaya dari batik lokal yang diilhami oleh ide batik kraton dan serapan unsur-unsur budaya asing. Batik Lasem memiliki ciri khas yang unik dan kental dengan nuansa budaya Cina dan Jawa.'
        },
        9: {
            'name': 'Batik Mega Mendung',
            'description': 'Motif Mega Mendung adalah salah satu jenis batik yang berasal dari daerah Cirebon, Jawa Barat. Berbeda dengan jenis batik lainnya, salah satu yang menjadi ciri khas dari batik motif Mega Mendung adalah ukiran awan dan langit yang digambarkan dalam batik.'
        },
        10: {
            'name': 'Batik Parang',
            'description': 'Batik parang adalah salah satu motif batik khas yang berasal dari Jawa, khususnya Daerah Istimewa Yogyakarta dan Solo. Batik Parang adalah Batik Kerajaan. Motif pada batik parang menggambarkan kekuatan dan pertumbuhan yang digunakan oleh para raja. Oleh karena itu, batik parang disebut juga batik larangan atau batik keraton karena tidak boleh dipakai oleh rakyat biasa.'
        },
        11: {
            'name': 'Batik Poleng',
            'description': 'Batik Poleng merupakan sebuah motif asli Bali yang memiliki ciri khusus yaitu motif yang menyerupai motif papan catur. Poleng atau corak papan catur adalah pola kotak-kotak sederhana yang terbentuk dari selang-seling warna gelap dan terang, biasanya hitam dan putih. Di Bali, kain dengan motif seperti ini disebut sebagai kain poleng. Kain poleng melambangkan keseimbangan antara dua hal yang bertolak belakang.'
        },
        12: {
            'name': 'Batik Sekar Jagad',
            'description': 'Batik Yogyakarta motif sekar jagad merupakan kain tradisional Indonesia yang dapat memberikan nilai lebih pada sebuah poduk busana. Sekar jagad merupakan motif perpaduan dari beberapa motif batik, menggambarkan muatan lingkungan hidup. Motif khas batik sekar jagad adalah terdapat garis pembatas atau range yang tidak simetris. Motifnya mirip tambalan pada kain yang dikenal dengan patchwork Page 3 3 art.'
        },
        13: {
            'name': 'Batik Tambal',
            'description': 'Motif Batik Tambal Berasal dari Yogyakarta. Motif batik tambal memiliki arti tambal bermakna menambal atau memperbaiki hal-hal yang rusak. Dalam perjalanan hidupnya, manusia harus memperbaiki diri menuju kehidupan yang lebih baik, lahir maupun batin. Dahulu, kain batik bermotif tambal dipercaya bisa membantu kesembuhan orang yang sakit.'
        }  
    }

    probabilities = {key: round(float(preds), 4) for key in batik_data}

    result = {
        'name': batik_data[preds]['name'],
        'description': batik_data[preds]['description'],
        'probabilities': probabilities
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
            return render_template('result.html', error=True)
        else:
            return render_template('result.html', error=False)

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
