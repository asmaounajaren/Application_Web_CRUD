from database import MySQL
from flask import Blueprint, render_template,flash,request,url_for
import re
from werkzeug.utils import redirect

auth = Blueprint('authentification', __name__)

@auth.route("/register")
def register_page():
    return render_template("register.html")

@auth.route('/register',methods= ['GET','POST'])
def register():
    if request.method == 'POST':
        
        nom_=request.form['nom']
        prenom_=request.form['prenom']
        email_=request.form['email']
        motdepasse_=request.form['motdepasse']
        # request.form.get("motdepasse", False)

        if len(nom_)==0 or len(prenom_)==0 or len(email_)==0 or len(motdepasse_)==0:
            flash('Veuillez remplir tous les champs !')
            return redirect(url_for('register_page'))    
        elif len(nom_)<2:
            flash('le nom doit contenir au moins 2 caractere !')
            return redirect(url_for('register_page'))

        elif len(prenom_)<2:
            flash('le prenom doit contenir au moins 2 caractere !')
            return redirect(url_for('register_page'))
        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_):
            flash('Email adresse Invalide !')
            return redirect(url_for('register_page'))
        #or not re.match(r'^[A-Z\d]$',motdepasse_)
        elif len(motdepasse_)<3 :
            flash('le mot de passe doit contenir au moins un caractere maj et un nombre !')
            return redirect(url_for('register_page'))

        else:
            cur = MySQL.connection.cursor()
            cur.execute("insert into utilisateur (nom,prenom,email,motdepasse) values(%s,%s,%s,%s)",(nom_,prenom_,email_,motdepasse_))
            MySQL.connection.commit()
            flash("bien ajouté avec succès")
            return redirect(url_for('home_page'))