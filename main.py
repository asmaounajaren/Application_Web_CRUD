from flask import Flask, render_template, flash,url_for,request,session
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
# from database import MySQL
import re
from authentification import auth
from form import loginForm
import os

skills_app =Flask(__name__)
skills_app.secret_key = os.urandom(32)
# skills_app.register_blueprint(auth,url_prefix="")

skills_app.register_blueprint(auth)

skills_app.config['MYSQL_HOST'] = 'flaskdb1.caa3epyonmig.eu-north-1.rds.amazonaws.com'
skills_app.config['MYSQL_USER'] = 'admin'
skills_app.config['MYSQL_PASSWORD'] = 'admin1234'
skills_app.config['MYSQL_DB'] = 'gestioncommande'

skills_app.config["SESSION_PERMANENT"] = False
skills_app.config["SESSION_TYPE"] = "filesystem"
# session(skills_app)

mysql = MySQL(skills_app)

@skills_app.route("/")
def home_page():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['nom'])
    return render_template("login.html")

@skills_app.route("/products")
def products_page():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("select * from produit")
        fetchdata=cur.fetchall()
        cur.close()
        return render_template("products.html",data=fetchdata)
    return render_template("login.html")


@skills_app.route('/ajouter',methods= ['POST'])
def ajouter():
    if request.method == 'POST':
        flash("bien ajouté avec succès")
        designation=request.form['designation']
        description=request.form['description']
        prix=request.form['prix']
        qteStock=request.form['qteStock']
        # request.form.get("qteStock", False)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO produit (designation, description, prix, qteStock) values(%s,%s,%s,%s)",(designation,description,prix,qteStock))
        mysql.connection.commit()
        return redirect(url_for('products_page'))

@skills_app.route('/update', methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id_produit = request.form['id_produit']
        designation=request.form['designation']
        description=request.form['description']
        prix=request.form['prix']
        qteStock=request.form['qteStock']
        cur = mysql.connection.cursor()
        cur.execute("""
        update produit set designation=%s, description=%s,prix=%s,qteStock=%s
        where id_produit=%s
        """,(designation,description,prix,qteStock,id_produit))
        flash("Bien modifié avec succès")
        mysql.connection.commit()
        return redirect(url_for('products_page'))



@skills_app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Bien supprimé")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM produit WHERE id_produit=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('products_page'))

@skills_app.route("/about")
def about_page():
    if 'loggedin' in session:
        return render_template("about.html",username="about page")
    return render_template("login.html")


# @skills_app.route("/register")
# def register_page():
#     return render_template("register.html")

@skills_app.route("/login")
def login_page():
    return render_template("login.html")

@skills_app.route('/login', methods=['GET','POST'])
def login():
    log= loginForm()
    if request.method=='POST':
        email=request.form['email']
        motdepasse=request.form['motdepasse']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM utilisateur WHERE email = %s AND motdepasse = %s', (email, motdepasse,))
        # Fetch one record and return result
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        print(user)
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['nom'] = user[1]
            session['prenom'] = user[2]
            # Redirect to home page
            return redirect(url_for('home_page'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('email ou mot de passe est incorrect !')
    return render_template('login.html')
@skills_app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('nom',None)
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@skills_app.route("/profile")
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM utilisateur WHERE id_utilisateur = %s', (session['id'],))
        user = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', user=user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
if __name__ == "__main__":
    skills_app.run(host='0.0.0.0',debug=True,port=8000)
