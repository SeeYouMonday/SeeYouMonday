from flask import Flask, render_template, request, flash, redirect, url_for
import os
import numpy as np
from os.path import abspath, dirname
import pandas as pd
from werkzeug.utils import secure_filename
from parse_pdf.parse import parse_resume
from data.match import match
from flask import send_from_directory

UPLOAD_FOLDER = 'static/files/'
JOB_DOC_FILE = 'data/out.csv'
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/about_us/', methods =['POST', 'GET'])
def about_us():
    return render_template('about_us.html')

@app.route('/visualization/', methods =['POST', 'GET'])
def visualization():
    return render_template('visualization.html')

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
            path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filepath)
            file.save(path)

            user_keywords = parse_resume(path)

            df = pd.read_csv(JOB_DOC_FILE)
            # turn off the truncating display option 
            pd.set_option('display.max_colwidth', -1)
            # calculate match  
            results = match(user_keywords, df) 
            # reset index starting from 1
            results.index = np.arange(1, len(results)+1)
            # add link 
            results['Url'] = results['Url'].apply(lambda x: '<a href="{0}">link</a>'.format(x))
            results['Terms'] = results['Terms'].apply(lambda x: x[1:-1]) 

            return render_template('result.html', tables=[results.to_html(escape=False)], \
                titles=['Name','Company','City','State','Url','Terms'])
    else:
        return render_template('index.html')


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 9999))
  app.debug = True
  print('Running on port ' + str(port))
  app.run('0.0.0.0',port)
