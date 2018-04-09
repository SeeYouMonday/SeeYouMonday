from flask import Flask, render_template, request, flash, redirect, url_for, session
import os, sys
from os.path import abspath, dirname
from werkzeug.utils import secure_filename
from parse_pdf.parse import parse_resume
UPLOAD_FOLDER = 'static/files/'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.secret_key = 'youcantguessthisout'
SESSION_TYPE = 'redis' #use RedisSessionInterface
app.config.from_object(__name__)

@app.route('/', methods =['POST', 'GET'])
def home():
    if request.method == "POST":
        return redirect(url_for('upload'))
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    app.logger.info(request.method)
    app.logger.info(request.files)
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload'))

        file = request.files['file']
        # if user does not selgitect file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            basedir = abspath(dirname(__file__))
            filepath = secure_filename(file.filename)
            app.logger.info('got filename and stuff')
            path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filepath)
            file.save(path)

            user_keywords = parse_resume(path)
            
            app.logger.info(user_keywords)
            return render_template('about_us.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
  port = 9999
  app.debug = True
  print('Running on port ' + str(port))
  app.run('0.0.0.0',port)
