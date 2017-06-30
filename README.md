How to Install
-----

Install flask (http://flask.pocoo.org/)
Something like: ```pip install flask```

Install jpeg:
Something like ```brew install jpeg```

Install PIL:
Something like ```pip install pillow```

Clone this repository: ```git clone https://github.com/dpwrussell/photoviewer.git```

Edit photoviewer/photoviewer.py to change PHOTO_DIR to the correct place.

Symlink 'images' in static directory to PHOTO_DIR, e.g.
```
cd photoviewer/static
ln -s /Users/dpwrussell/Photos images
```

Run
---

```
cd photoviewer
python photoviewer.py
```

Your web browser can then be pointed at http://localhost:5000