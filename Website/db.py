import os
import re
import sqlite3
import cv2

SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'kaleidoscope.db')
DIRECTORY = 'D:\Drexel Work\Spring-20\Computer Vision\Project\Kaleidoscope2\Website\public\img'

image_names = []

class Database:

    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_PATH)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    def images_list(self):
        """
            Returns images from the folder.
        """
        img = self.select('SELECT * FROM Images')
        return img

    def load_images(self):
        """
            If file does not exist, the entry is made in the database, else error is returned.
        """
        for file in os.listdir(DIRECTORY):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                image_names.append(file)
        try:
            for i in image_names:
                self.execute('INSERT INTO Images (Name) VALUES (?)', [i])
            return "Good"
        except sqlite3.Error as er:
            return er

    def create_images(self, name):
        """
            Validates for duplicate file in the folder.
        """
        try:
            self.execute('INSERT INTO Images (Name) VALUES (?)', [name])
            return "Good"
        except sqlite3.Error as er:
            return er
    def get_image(self, image_path):
        """
            Returns RGB of the images
        """
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def get_image_matrix(self):
        """
            Returns image matrix of the images in the directory.
        """
        images = []
        for file in os.listdir(DIRECTORY):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                images.append(self.get_image(os.path.join(DIRECTORY, file)))
        return images

    def create_color(self, name):
        """
            Stores the color selected by the user in the database.
        """
        self.execute('INSERT INTO colors (Name) VALUES (?)',[name])

    def delete_color(self):
        """
            Deletes the color stored in the database.
        """
        self.execute('DELETE FROM colors')

    def close(self):
        self.conn.close()
