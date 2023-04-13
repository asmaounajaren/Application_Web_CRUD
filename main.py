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

@skills_app.route("/")
def home_page():
    cur = mysql.connection.cursor()
    cur.execute("select * from utilisateur")
    fetchdata=cur.fetchall()
    cur.close()
    return render_template("home.html",data=fetchdata)

@skills_app.route('/ajouter',methods= ['POST'])
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

@skills_app.route('/update', methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id_utilisateur = request.form['id_utilisateur']
        nom=request.form['nom']
        prenom=request.form['prenom']
        email=request.form['email']
        motdepasse=request.form['motdepasse']
        cur = mysql.connection.cursor()
        cur.execute("""
        update utilisateur set nom=%s, prenom=%s,email=%s,motdepasse=%s
        where id_utilisateur=%s
        """,(nom,prenom,email,motdepasse,id_utilisateur))
        flash("Bien modifié avec succès")
        mysql.connection.commit()
        return redirect(url_for('home_page'))



@skills_app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Bien supprimé")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM utilisateur WHERE id_utilisateur=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('home_page'))

@skills_app.route("/about")
def about_page():
    return render_template("about.html",username="about page")

if __name__ == "__main__":
    skills_app.run(debug=True,port=5000)
