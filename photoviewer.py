# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# Imports for views
from os import listdir, mkdir
from os.path import isdir, join, dirname, exists, splitext
from PIL import Image
import os

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    PHOTO_DIR='/home/pi/dtp/',
    # PHOTO_DIR='static/images/',
    THUMB_SIZE=(128, 128)
))
app.config.from_envvar('PHOTOVIEWER_SETTINGS', silent=True)


# View for the root of the app, shows main photo directory
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def photo_dir(path):
    DEBUG=True,
    pd = app.config['PHOTO_DIR']
    dir_entries = []
    image_entries = []
    up = None

    # Only add 'up' if not in the root
    if path != '':
        up = dirname(join('/',path))

    # One thing that flask does not have by default is regualar expression
    # matching in the routing. Can be added on:
    # http://stackoverflow.com/questions/5870188/does-flask-support-regular-expressions-in-its-url-routing
    # Just handle it here by checking if the current path is a directory or not

    nav = join(pd, path)
    # If it's a directory, show the listing
    if isdir(nav):
    
        # TODO There is no safety here, a user could potentially navigate
        # outside of where they should be allowed

        # If there is no thumbnail directory for this directory, create it
        thumb_dir = join(nav, '.thumbnail')
        if not exists(thumb_dir):
            mkdir(thumb_dir)


        list_all = listdir(nav)
        for list_item in list_all:
            if isdir(join(nav,list_item)) and list_item != '.thumbnail':
                dir_entries.append(list_item)
            # Primitive check for image files, only for jpg and png
            elif list_item.endswith('.png') or list_item.endswith('.jpg'):
                image_entries.append(list_item)

                # Generate thumbnails for any that are missing
                thumb = join(thumb_dir,list_item)
                if not exists(thumb):
                    # Open primary image
                    im = Image.open(join(nav,list_item))
                    # Convert mode on paletted image formats
                    if im.mode != "RGB":
                        im = im.convert("RGB")
                    im.thumbnail(app.config['THUMB_SIZE'], Image.ANTIALIAS)
                    im.save(thumb, "JPEG")

        return render_template('photo_dir.html', dir_entries=dir_entries, image_entries=image_entries, path=path, up=up)

    # Otherwise it must be a file (assuming an image file, but again, unsafe)
    # So display the photo
    else:
        return render_template('photo.html', image=url_for("static", filename=join('images', path)), up=up, file=path)

@app.route('/delete/<file>')
def delete(file):
    print ('file', file)
    os.remove(os.path.join(app.config['PHOTO_DIR'], file))
    return redirect(url_for('photo_dir'))






# Enable running the app directly from python:
# python photoviewer.py
if __name__ == '__main__':
    app.run(host='localhost', port=80)
