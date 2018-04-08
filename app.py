from flask import Flask, render_template, request, flash, redirect, url_for, session
import os, sys
from os.path import abspath, dirname
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

@app.route('/upload/', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('start'))
    file = request.files['file']
    # if user does not selgitect file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        basedir = abspath(dirname(__file__))
        filepath = file.filename
        path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filepath)
        file.save(path)

        user_keywords = parse_resume(path)
        # rs = rec_system(size, funding, user_keywords)
        # rs.loadCompaniesData()
        # companyRankings = rs.rankCompaniesForUser()
        # print("company rankings", companyRankings)

        return user_keywords 
    else:
        return render_template('start.html')


if __name__ == '__main__':
  port = 9999
  app.debug = True
  print('Running on port ' + str(port))
  app.run('0.0.0.0',port)
