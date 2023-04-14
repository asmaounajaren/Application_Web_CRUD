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
    cur.execute("select * from produit")
    fetchdata=cur.fetchall()
    cur.close()
    return render_template("home.html",data=fetchdata)

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
        return redirect(url_for('home_page'))

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
        return redirect(url_for('home_page'))



@skills_app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Bien supprimé")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM produit WHERE id_produit=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('home_page'))

@skills_app.route("/about")
def about_page():
    return render_template("about.html",username="about page")

@skills_app.route("/register")
def register_page():
    return render_template("register.html")

if __name__ == "__main__":
    skills_app.run(debug=True,port=5000)
