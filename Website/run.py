from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
from passlib.hash import pbkdf2_sha256
import os
import sqlite3
from db import Database
from sklearn.cluster import KMeans
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = b'lkj98t&%$3rhfSwu3D'
DIRECTORY = 'D:\Courses\Third Quarter\Computer Vision\Project\Kaleidoscope-A-tool-for-identifying-colors\Website\public\img'
app.config['DIRECTORY'] = DIRECTORY

COLORS = {'GREEN': [0, 128, 0], 'BLUE': [0, 0, 128], 'YELLOW': [255, 255, 0], 'WHITE':[255, 255, 255], 'RED' : [204, 0, 0], 'BLACK' : [1, 1, 1]}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Handle the home page.
@app.route('/')
def index():
    return render_template('index.html')

# Handle any files that begin "/" by loading from the packages directory.
@app.route('/packages/<path:path>')
def base_static(path):
    return send_file(os.path.join(app.root_path, '..', 'packages', path))

@app.route('/api/imagesList')
def api_imageList():
    img = get_db().images_list()
    return jsonify(img)

# Handles the insertion of images in the Database.
@app.route('/pictures')
def pictures():
    a = get_db().load_images()
    if a == "Good":
        return render_template('pictures.html')
    else:
        return render_template('pictures.html')

# Handles the task of uploading the file onto a physical memory.
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['inpFile']
      if f:
          filename = secure_filename(f.filename)
          print("filename '" +filename+ "' is uploaded.")
          f.save(os.path.join(app.config['DIRECTORY'], filename))
      return render_template('file_saved.html')

# Function to flatten the array to pass as input, and to arrange the colors in the right order.
def get_colors(image, number_of_colors):
    modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)
    counts = dict(sorted(counts.items()))

    center_colors = clf.cluster_centers_

    ordered_colors = [center_colors[i] for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    return rgb_colors

# Function to try and match to the top 10 color of the images. We use rgb2lab to convert the values, and compute differences using cie colorspace.
def match_image_by_color(image, color, threshold=60, number_of_colors=10):
    image_colors = get_colors(image, number_of_colors)
    selected_color = rgb2lab(np.uint8(np.asarray([[color]])))

    select_image = False
    for i in range(number_of_colors):
        curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[i]]])))
        diff = deltaE_cie76(selected_color, curr_color)
        if (diff < threshold):
            select_image = True

    return select_image

# Function to go through all images in the set, and return relevant images as output.
def show_selected_images(images, image_names, color, threshold, colors_to_match):
    index = 1

    selected_images = []

    for i in range(len(images)):
        selected = match_image_by_color(images[i], color, threshold, colors_to_match)
        if (selected):
            selected_images.append(image_names[i])
            index += 1
    print("Selected Images:", selected_images)

    return selected_images

# Handles the storing of colors in the Database.
@app.route('/store_color', methods=['GET', 'POST'])
def store_color():
    name = ""
    hey = []
    if request.method == 'POST':
        print("\nComputing the images to be displayed based on the selected color...")
        image_names = []
        name = request.form['colorname']
        name = name.upper()
        get_db().create_color(name)
        images = get_db().get_image_matrix()
        for file in os.listdir(DIRECTORY):
            print("Finished scanning '" +file+ "'")
            image_names.append(file)
        hey = show_selected_images(images, image_names, COLORS[name], 60, 5)
        get_db().delete_color()

    return render_template('selection_pictures.html', name = name, hey = hey)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
