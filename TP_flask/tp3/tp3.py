from flask import Flask, render_template, request
import os, sqlite3

app = Flask(__name__, template_folder="templates")
app_dir = os.getcwd()

## it allows to display "filename"
@app.route("/td1/<filename>")
def display_file(filename):
    return render_template("static/" + filename)

## render "index.html" in the "static/" folder from the td1 
@app.route("/td1/")
def display_index():
    return render_template("static/")

## render a message, a table with the form and add new information in the sqlite DB
@app.route("/formproc", methods=['POST'])
def formproc():
    data = request.form
    name = data["prenom"]
    surname = data["nom"]
    sex = data["genre"]

    with sqlite3.connect(app_dir + "/templates/static/db.sqlite3") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO FormData VALUES ({name}, {surname}, {sex})".format(name=name, surname=surname, sex=sex))

    return render_template("table.html", name=name, surname=surname, sex=sex)
    