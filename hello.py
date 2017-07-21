"""Cloud Foundry test"""
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from models import db, Video
from ffmpeg.ffmpeg_int import grab_frame
from visualAPI.APIint import similarity_score

import os
import random
import logging
import re

UPLOAD_FOLDER = 'data'
#Cache
cache = {}

if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    pg_uri = services['compose-for-postgresql'][0]['uri']
else:
    pg_uri = 'sqlite:////tmp/test.db'

port = int(os.getenv("PORT")) if 'PORT' in os.environ else 5000

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = pg_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dbtest')
def dbtest():
    vid_new = Video(str(random.random()), 'dev team')
    db.session.add(vid_new)
    db.session.commit()
    return 'Hello friend! I have '+str(Video.query.count())+' videos now.'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        logging.warning(len(request.files))
        if 'video' not in request.files:
            logging.error('File not uploaded.')
            return redirect(request.url)
        file = request.files['video']
        filetype = re.search('\.[a-zA-Z]+', file.filename).group()
        filename = str(random.random()) + filetype
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # called from ffmpeg/ffmpeg_int.py
        in_path = os.path.join(UPLOAD_FOLDER, filename)
        outpng = str(random.random()) + '.png'
        out_path = os.path.join(UPLOAD_FOLDER, outpng)
        grab_frame(in_path, out_path)
        # check cache
        with open(out_path, 'rb') as binary_file:
            cache_key = binary_file.read(128)
            print(cache_key)
            if cache_key in cache:
                return render_template('duplicate.html')
            else:
                cache[cache_key] = True
        # called from visualAPI/APIint.py
        # Debug method, TODO: store similarity score
        if similarity_score(outpng):
            return render_template('duplicate.html')
        else:
            return render_template('original.html')
        # remove temp file
        os.remove(out_path);
    return render_template('upload.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=port)



