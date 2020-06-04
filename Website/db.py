import os
import re
import sqlite3
import cv2

SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'kaleidoscope.db')
IMAGE_DIRECTORY = 'D:\Drexel Work\Spring-20\Computer Vision\Project\Kaleidoscope-A-tool-for-identifying-colors\Website\public\img'

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
        img = self.select('SELECT * FROM Images')
        return img

    def load_images(self):
        for file in os.listdir(IMAGE_DIRECTORY):
            image_names.append(file)
        try:
            for i in image_names[1:]:
                self.execute('INSERT INTO Images (Name) VALUES (?)', [i])
            return "Good"
        except sqlite3.Error as er:
            return er

    def create_images(self, name):
        try:
            self.execute('INSERT INTO Images (Name) VALUES (?)', [name])
            return "Good"
        except sqlite3.Error as er:
            return er

    def get_image_matrix(self):
        images = []
        for file in os.listdir(IMAGE_DIRECTORY):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                images.append(self.get_image(os.path.join(IMAGE_DIRECTORY, file)))
        return images

    def get_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def create_color(self, name):
        self.execute('INSERT INTO colors (Name) VALUES (?)',[name])

    def delete_color(self):
        self.execute('DELETE FROM colors')

    def close(self):
        self.conn.close()
