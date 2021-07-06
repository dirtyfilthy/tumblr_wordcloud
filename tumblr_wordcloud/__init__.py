import matplotlib
matplotlib.use('Agg')

import os
import sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import cloud
import config
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # index
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/generate', methods=["POST"])
    def generate():
        blog = request.form.get('blog')
        tag  = request.form.get('tag')
        blog = blog.strip()
        tag  = tag.strip()
        blog = blog.replace("https://", "")
        blog = blog.replace("/", "")
        if not re.search(r"\.tumblr\.com$", blog):
            blog = blog + ".tumblr.com"
        
        tag  = tag.replace("#", "")

        cloud_image =  os.path.basename(cloud.save_cloud(blog, tag, config.DATA_DIR))

        if not cloud_image:
            flash(r"Could not retrieve posts for {blog}")
            return redirect(url_for('index'))

        return render_template("generate.html", blog=blog, tag=tag, image=cloud_image)




    return app