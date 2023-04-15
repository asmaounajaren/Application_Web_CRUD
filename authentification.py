# from flask import Blueprint, render_template, flash,url_for,request
# from werkzeug.utils import redirect
# from flask_mysqldb import MySQL
# auth =Blueprint("authentification",__name__)
# auth.secret_key = 'many random bytes'

# auth.config['MYSQL_HOST'] = 'localhost'
# auth.config['MYSQL_USER'] = 'root'
# auth.config['MYSQL_PASSWORD'] = ''
# auth.config['MYSQL_DB'] = 'gestioncommande'
# mysql = MySQL(auth)
# @auth.route('/register',methods= ['GET','POST'])
# def register():
#     if request.method == 'POST':
#         flash("bien ajouté avec succès")
#         nom_=request.form['nom']
#         prenom_=request.form['prenom']
#         email_=request.form['email']
#         motdepasse_=request.form['motdepasse']
#         # request.form.get("motdepasse", False)
#         cur = mysql.connection.cursor()
#         cur.execute("insert into utilisateur (nom,prenom,email,motdepasse) values(%s,%s,%s,%s)",(nom_,prenom_,email_,motdepasse_))
#         mysql.connection.commit()
#         return redirect(url_for('home_page'))
    
# @auth.route('/login', methods=['GET','POST'])
# def login():
#     if request.method=='POST':
#         email=request.form('email')
#         motdepasse=request.form('motdepasse')
#          # Check if account exists using MySQL
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT * FROM utilisateur WHERE email = %s AND motdepasse = %s', (email, motdepasse,))
#         # Fetch one record and return result
#         user = cursor.fetchone()
#                 # If account exists in accounts table in out database
#         if user:
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
#             session['id'] = user['id']
#             session['username'] = user['username']
#             # Redirect to home page
#             return redirect(url_for('home_page'))
#         else:
#             # Account doesnt exist or username/password incorrect
#             flash('Incorrecte email / mot de passe!')
#             return redirect(url_for('register_page'))