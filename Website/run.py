from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
import os
from db import Database
from sklearn.cluster import KMeans
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='public', static_url_path='')
DIRECTORY = 'D:\Drexel Work\Spring-20\Computer Vision\Project\Kaleidoscope-A-tool-for-identifying-colors\Website\public\img'
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadImage')
def uploadImage():
    """ Upload screen """
    return render_template('uploadImage.html')


@app.route('/file_saved')
def save():
    """ Uploaded file saved. """
    return render_template('file_saved.html')


@app.route('/file_unsaved')
def unsave():
    """ Uploaded file not saved. """
    return render_template('file_unsaved.html')

@app.route('/aboutus')
def aboutus():
    """ About Us screen """
    return render_template('aboutus.html')

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
    """ Renders all the images from the folder. """
    a = get_db().load_images()
    if a == "Good":
        return render_template('pictures.html')
    else:
        return render_template('pictures.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    """
    Returns a  template that indicates that the file has been saved successfully or returns a template that indicates the file already exists.
    """
    if request.method == 'POST':
        f = request.files['inpFile']
        if f:
            filename = secure_filename(f.filename)
            val = get_db().create_images(filename)
            if val == "Good":
                f.save(os.path.join(app.config['DIRECTORY'], filename))
                return render_template('file_saved.html')
            else:
                return render_template('file_unsaved.html')


def predominant_colors(image, number_of_colors):
    """
            Function uses rgb2lab to convert the RGB color space into LAB color space, and compute the similarities using cie.
            Args:
                images:  All the images in the folder in terms of matrices.
                number_of_colors: Number of predominant colors to be chosen.
            Returns:
                Predominant colors from the images.

    """
    resized_img = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    d_1, d_2 = resized_img.shape[0], resized_img.shape[1]
    modified_image = resized_img.reshape(d_1 * d_2, 3)

    kmeans_output = KMeans(n_clusters=number_of_colors)
    var_labels = kmeans_output.fit_predict(modified_image)

    # To store the counts such that the maximum frequency colors are selected as predominant colors.
    counts = Counter(var_labels)
    counts_freq = dict(sorted(counts.items()))

    center_colors = kmeans_output.cluster_centers_

    ordered_list = [center_colors[i] for i in counts_freq.keys()]
    rgb = [ordered_list[i] for i in counts_freq.keys()]

    return rgb

def matched_image(image, color, threshold=60, number_of_colors=10):
    """
        Function uses rgb2lab to convert the RGB color space into LAB color space, and compute the similarities using cie.
        Args:
            image:  Every image in the folder.
            color: Chosen color.
            threshold: A value below which the color of the images are considered to be matching with the chosen color.
            number_of_colors: Number of predominant colors to be chosen.

        Returns:
            An image matrix of the images with difference (between chosen color and the color in the images) less than the threshold value.

    """
    selected = False
    image_colors = predominant_colors(image, number_of_colors)
    lab_color = rgb2lab(np.uint8(np.asarray([[color]])))

    for i in range(number_of_colors):
        input_color = rgb2lab(np.uint8(np.asarray([[image_colors[i]]])))
        difference_val = deltaE_cie76(lab_color, input_color)
        if (difference_val < threshold):
            selected = True

    return selected

def selected_images(images, image_names, color, threshold, colors_to_match):
    """
        Function uses rgb2lab to convert the RGB color space into LAB color space, and compute the similarities using cie.
        Args:
            images:  All the images in the folder in terms of matrices.
            image_names:  The names of the images in the folder.
            color: Color chosen by the users.
            threshold: A value below which the color of the images are considered to be matching with the chosen color.

        Returns:
            An image matrix of the images with difference (between chosen color and the color in the images) less than the threshold value.

    """
    selected_images = []
    color_index = 1

    for i in range(len(images)):
        selected = matched_image(images[i], color, threshold, colors_to_match)
        if (selected):
            selected_images.append(image_names[i])
            color_index += 1
    print("Selected Images:", selected_images)

    return selected_images

@app.route('/store_color', methods=['GET', 'POST'])
def store_color():
    """
        Function stores the selected color in the database and returns the images of the same color.
        Args: NA

        Returns:
            An image matrix of the images with difference (between chosen color and the color in the images) less than the threshold value.

    """
    name = ""
    final_matched_images = []
    if request.method == 'POST':
        print("\nComputing the images to be displayed based on the selected color...")
        image_names = []
        name = request.form['colorname']
        name = name.upper()
        get_db().create_color(name)
        images = get_db().get_image_matrix()
        for file in os.listdir(DIRECTORY):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                print("Finished scanning '" +file+ "'")
                image_names.append(file)
        final_matched_images = selected_images(images, image_names, COLORS[name], 60, 5)
        get_db().delete_color()

    return render_template('selection_pictures.html', name = name, final_matched_images = final_matched_images)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
