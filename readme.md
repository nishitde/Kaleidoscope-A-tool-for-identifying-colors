<h3 align="center">Kaleidoscope: A tool for Color Identification</h3>

## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
* [Using Flask](#using-flask)
	* [Installing](#installing)
	* [Open the application](#open-the-application)
		* [Prerequisites](#prerequisites)
		* [Execute](#execute)
* [Using GitHub](#using-github)
	* [Cloning](#cloning)
	* [Open the application](#open-the-application)
		* [Prerequisites](#prerequisites)
		* [Execute](#execute)

## About the Project
The goal of our experiment is to filter the images based on the color given by the user. The user can upload images to the site and select a color from a given set of colors and the images with the selected color are returned to the user. Here, we use the K-Means algorithm to form a cluster of colors present in the images, this helps us to make a proper distinction in the colors. We use the **LAB** color space, and in that, we use **CIE** to find the similarity between the colors as some colors may not be an exact match for the colors we are defining so we find the color which is closest to the colors we defined. As the CIE system perceives the colors similar to the human eye it works better for color identification as the user will get a better idea of why an image was returned as the output. We use a threshold value to limit the similarity function value which helps to make the output more accurate in terms of the color distinction. We can also select the top ‘n’ values as far as color is concerned, like, if green exists in the top 5 colors in an image and we make the image selector such that if we select green than the images with green in their top 5 colors will be selected, conversely if we make it so that we only choose top 2 colors of an image than the image with green in the 5th position will not be selected when the user inputs green. This makes the project more adaptive.

We adopted **K-Means Clustering** into our application. To run the application follow the steps mentioned in the 'Getting Started' section.

### Built with
* [Flask](https://palletsprojects.com/p/flask/)
* [HTML](https://en.wikipedia.org/wiki/HTML5)
* [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
* [BootStrap](https://getbootstrap.com/)
* [JavaScript](https://www.javascript.com/)
* [jQuery](https://jquery.com/)

## Getting Started
Following are the instructions for running the code in two different ways:

 1. Using Flask
 2. Using GitHub

## 1.	Using Flask:
We will be using Flask as our web framework. Flask is	a Python-based	framework. If	you	do not	have Python3 on your local machine,	we recommend that	you	look	through	the	Python downloads page (https://www.python.org/downloads/) and	install	Python3 in	whatever way is appropriate for your	machine. In the end, you should be	able	to enter
```
> python3 --version
```
and see a version number of 3.3 or	higher.

### Installing
Next, you will	need to install the Flask package	within	the Python	setup. This is easily done by entering:
```
> pip3 install Flask
```
## Open the application

### Prerequisites
  1. Ensure that the path in `run.py` and `db.py` under the name of `DIRECTORY` has been changed to whatever your path is for the `Kaleidoscope-A-tool-for-identifying-colors/Website/public/img/`.
  2. For re-running the project, ensure that the `img` folder in the `Kaleidoscope-A-tool-for-identifying-colors/Website/public/img` directory is emptied by deleting all of its contents.
  3. Clear out the existing database, and recreate another one by simply running the `new_db.py` file, by executing the following command in the terminal `python3 new_db.py`.

### Execute
To test your setup, please download the ZIP	package available as	part	of this	project. The	directory, Kaleidoscope-A-tool-for-identifying-colors, includes files and libraries	that	we will be using. In a terminal window, please navigate to the `Kaleidoscope-A-tool-for-identifying-colors/Website/` directory and enter the following	command:
```
> python3 run.py
* Restarting with stat
* Debugger is active!
* Debugger PIN: 133-514-852
* Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
```
This	command runs the included	Python file, which	in	turns starts	a Flask web server	on a local address and port number (http://127.0.0.1:8080/). Now, open a web browser (Chrome,	Safari, Firefox, or any browser), and point it to this address; when you do so, Flask will “serve” the	web	page provided and show you a page just like the one we included in our paper.

## 2.	Using GitHub:
For cloning the project repository from the GitHub repository on to your local repository, you must follow the given steps.

### Cloning
 1. Navigate to the GitHub repo on the GitHub Page ([https://github.com/nishitde/Kaleidoscope-A-tool-for-identifying-colors](https://github.com/nishitde/Kaleidoscope-A-tool-for-identifying-colors))
 2. Click on the 'Clone or download' option, or copy the URL (https://github.com/nishitde/Kaleidoscope-A-tool-for-identifying-colors.git)
 3. Open the Git Bash terminal on your desired directory.
 4. Enter the command `git clone https://github.com/nishitde/Kaleidoscope-A-tool-for-identifying-colors.git`.

## Open the application

### Prerequisites
  1. Ensure that the path in `run.py` and `db.py` under the name of `DIRECTORY` has been changed to whatever your path is for the `Kaleidoscope-A-tool-for-identifying-colors/Website/public/img/`.
  2. For re-running the project, ensure that the `img` folder in the `Kaleidoscope-A-tool-for-identifying-colors/Website/public/` directory is emptied by deleting all of its contents.
  3. Clear out the existing database, and recreate another one by simply running the `new_db.py` file, by executing the following command in the terminal `python3 new_db.py`.

### Execute
In	a terminal window, please navigate to the `cd Kaleidoscope-A-tool-for-identifying-colors/Website/` directory and enter the following command:
```
> python3 run.py
* Restarting with stat
* Debugger is active!
* Debugger PIN: 133-514-852
* Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
```
This	command runs the included	Python file, which	in	turns starts	a Flask web server	on a local address and port number (http://127.0.0.1:8080/). Now, open a web browser (Chrome,	Safari, Firefox, or any browser), and point it to this address; when you do so, Flask will “serve” the	web	page provided and show you a page just like the one we included in our paper.
