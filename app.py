from flask import Flask, render_template,request, Response,url_for, redirect,flash,send_file
from werkzeug.utils import secure_filename
import json
import os
from main import predict_approval

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def home():
    try:
        out = open('filename.json', "r")
        fname = json.loads(out.read())
        os.remove(fname['filename'])
    except:
        pass
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        json_object = {
            "filename": f.filename
        }
        json_object = json.dumps(json_object)
        with open("filename.json", "w") as outfile:
            outfile.write(json_object)
        return redirect(url_for('prediction'))
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    out = open('filename.json', "r")
    fname = json.loads(out.read())
    status = predict_approval(fname['filename'])
    return render_template('prediction.html',status=status)
@app.route('/download_template')
def download_template():
    return send_file('home-loan-form-new.pdf',as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)