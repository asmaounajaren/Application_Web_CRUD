from flask import Flask, render_template, flash,url_for,request,session
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
# from authentification import auth

skills_app =Flask(__name__)
skills_app.secret_key = 'many random bytes'
# skills_app.register_blueprint(auth,url_prefix="")

skills_app.config['MYSQL_HOST'] = 'localhost'
skills_app.config['MYSQL_USER'] = 'root'
skills_app.config['MYSQL_PASSWORD'] = ''
skills_app.config['MYSQL_DB'] = 'gestioncommande'

skills_app.config["SESSION_PERMANENT"] = False
skills_app.config["SESSION_TYPE"] = "filesystem"
# session(skills_app)

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

@skills_app.route("/login")
def login_page():
    return render_template("login.html")

@skills_app.route('/register',methods= ['GET','POST'])
def register():
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
    
@skills_app.route('/login', methods=['GET','POST'])
def login():
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
            return redirect(url_for('login_page'))
if __name__ == "__main__":
    skills_app.run(debug=True,port=5000)
