from email import message
from email.quoprimime import body_check
from importlib.metadata import files
from pickle import FALSE, TRUE
from flask import url_for , request,flash
from flask import Flask
from flask import render_template,abort
import os
from flask import redirect
from werkzeug.utils import secure_filename
from database import get_db

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
@app.route("/home")
def home():
    return render_template("base.html")

@app.route("/admin_card")
@app.route("/photo_condition")
def card(name = '',email='',number='',date=''):
    conn = get_db().cursor()
    conn.execute("select * from contact_form order by date;")
    data = conn.fetchall()
    return render_template("admin_card.html",name = name,email=email,number=number,date=date,data=data)

@app.route("/admin")
@app.route("/admin/<name>/<email>/<number>/<date>")
def admin(name = '',email='',number='',date=''):
    conn = get_db().cursor()
    conn.execute("select * from contact_form;")
    data = conn.fetchall()
    return render_template("admin.html",name = name,email=email,number=number,date=date,data=data)
    


@app.route('/upload',methods=['POST','GET'])
def upload_file():
    if request.method=="POST" and\
        "file" in request.files :
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            print(app.instance_path)
    return render_template("upload_file.html")

@app.route('/add_app' , methods=['POST','GET'])
def add_app():
    error=None
    if request.method == "POST":
       name = request.form ['name']
       email = request.form['email']
       number = request.form['number']
       date = request.form['date']
       pic = request.files['mypict']
       filename = secure_filename(pic.filename)
       pic.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
       conn = get_db()
       conn.execute(f"INSERT INTO contact_form (name,email,number,date,picture) VALUES ('{name}','{email}','{number}','{date}','{filename}');")
       conn.commit()
       conn.close()
       flash('The Appointment has been submitted Successfully !')
       #return redirect(url_for('admin', date=name ,password = email , id = number, date = date))
    return render_template("add_appointment.html",message = message)

@app.route('/update/<int:id>',methods=['GET','POST'])
def update_appointment(id):
    conn = get_db()
    if request.method == 'POST':
        name = request.form ['name']
        email = request.form['email']
        number = request.form['number']
        date = request.form['date']
        #pic = request.files['mypict']
        # filename = secure_filename(pic.filename)
        # pic.save(os.path.join(
        #         app.config['UPLOAD_FOLDER'], filename))
        conn.execute(f"Update contact_form set name='{name}' , email='{email}' , number='{number}' , date='{date}' where id={id}")
        conn.commit()
        conn.close()
    elif request.method == 'GET':
        conn = conn.cursor().execute(f"select * from contact_form where id={id}")
        row = conn.fetchone()
        conn.close()
        return render_template("update_appointment.html",row=row)
    return redirect(url_for("admin"))

@app.route('/delete_entry/<int:id>', methods=['POST','GET'])
def delete_entry(id):
    db = get_db()
    if request.method == 'POST':
        db.execute(f'delete from contact_form where id={id}')
        db.commit()
        db.close()
    elif request.method == 'GET':
        db = db.cursor().execute(f"select * from contact_form where id={id}")
        row = db.fetchone()
        db.close()
        return render_template("delete_appointment.html",row=row)
    return redirect(url_for("admin"))

@app.route('/delete_id/<int:id>', methods=['POST','GET'])
def delete_id(id):
    db = get_db()
    if request.method == 'GET':
        db.execute(f'delete from contact_form where id={id}')
        db.commit()
        db.close()
        # return render_template("delete_appointment.html",row=row)
    return redirect(url_for("info"))

@app.post('/search')
def search_appointment():
    if 'name' in request.form:
        name = request.form['name']
    conn = get_db().cursor()
    conn.execute(f"Select DISTINCT * from contact_form where name like '{name}%' order by date")
    data = conn.fetchall()
    conn.close()
    return render_template('search_appointment.html',data = data)

@app.get('/filter')
def filter_app():
    conn = get_db().cursor()
    conn.execute(f"Select DISTINCT * from contact_form order by date")
    data = conn.fetchall()
    conn.close()
    return render_template('filter_appointment.html',data = data)

@app.route('/info')
@app.route('/admin/<name>/<email>/<number>/<date>')
def info(name = '',email='',number='',date=''):
    conn = get_db().cursor()
    conn.execute("select * from contact_form order by date;")
    data = conn.fetchall()
    return render_template("info.html" ,name = name,email=email,number=number,date=date,data=data)
    
