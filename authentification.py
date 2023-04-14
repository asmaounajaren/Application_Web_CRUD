from flask import Flask, render_template, flash,url_for,request
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

skills_app =Flask(__name__)
skills_app.secret_key = 'many random bytes'

skills_app.config['MYSQL_HOST'] = 'localhost'
skills_app.config['MYSQL_USER'] = 'root'
skills_app.config['MYSQL_PASSWORD'] = ''
skills_app.config['MYSQL_DB'] = 'gestioncommande'

mysql = MySQL(skills_app)
@skills_app.route('/register',methods= ['GET','POST'])
def ajouter():
    if request.method == 'POST':
        flash("bien ajouté avec succès")
        nom_=request.form['nom']
        prenom_=request.form['prenom']
        email_=request.form['email']
        motdepasse_=request.form['motdepasse']
        # request.form.get("motdepasse", False)
        cur = mysql.connection.cursor()
        cur.execute("insert into utilisateur (nom,prenom,email,motdepasse) values(%s,%s,%s,%s)",(nom_,prenom_,email_,motdepasse_))
        mysql.connection.commit()
        return redirect(url_for('home_page'))