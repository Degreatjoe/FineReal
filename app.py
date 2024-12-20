from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, description TEXT)')
    print ("Opened database successfully")
    conn.close()

init_sqlite_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-course/', methods=['POST'])
def add_course():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute ("INSERT INTO courses (title, description) VALUES (?, ?)", (title, description)) 
                con.commit() 
                msg = "Course added successfully" 
        except:
            con.rollback()
            msg = "Error ocurred"
        finally:
            return redirect(url_for('home'))
        con.close()

@app.route('/view-courses/')
def view_courses():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    return render_template('view_courses.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)


