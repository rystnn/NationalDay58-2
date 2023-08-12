from flask import Flask, render_template, request, send_from_directory
import sqlite3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

db = sqlite3.connect("database.db")
db.execute('''CREATE TABLE IF NOT EXISTS photo(
pid INTEGER PRIMARY KEY,
pfilename TEXT
)''')
db.commit()
db.close()

@app.route('/', methods = ["GET","POST"])
def index():
  if request.method == "POST" and request.files and 'photo' in request.files:
    photo = request.files["photo"]
    photo_name = secure_filename(photo.filename)
    path = os.path.join("uploads",photo_name)
    photo.save(path)
    db = sqlite3.connect("database.db")
    db.execute("INSERT INTO photo(pfilename) VALUES(?)",(photo_name,))
    db.commit()
    db.close()
  
  return render_template("index.html")

@app.route('/show')
def show():
  db = sqlite3.connect('database.db')
  data = db.execute("SELECT * FROM photo")
  files = []
  for item in data:
    files.append(item[1])
  db.close()
  return render_template("view.html",files=files)

@app.route('/photos/<filename>')
def get_file(filename):
  return send_from_directory("uploads",filename)
  
app.run(host='0.0.0.0', port=81)
