import ibm_db
from flask import Flask, render_template, redirect, url_for, flash, escape, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = "sdkjfbibnbsfm2352ujnhdouafbjn123R2rjkx23bnrzaEvy45yvrtht"


DB_HOSTNAME = "ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
DB_PORT = "31321"
DB_USERNAME = "clq78397"
DB_PASS = "PrRgMAFWWQVjPZEM"

DB_STRING = f"DATABASE=bludb;HOSTNAME={DB_HOSTNAME};PORT={DB_PORT};SECURITY=SSL;SSLServerCertificate=SSLCertificate.crt;UID={DB_USERNAME};PWD={DB_PASS}" 
conn = ibm_db.connect(DB_STRING,'','')
print(conn)

class LoginForm(FlaskForm):
    email = EmailField("email", validators=[InputRequired("Email is required"), Email()])
    password = PasswordField("password", validators=[InputRequired("Password is required")])

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[InputRequired("Username is required")])
    email = EmailField("email", validators=[InputRequired("Email is required"), Email()])
    address = StringField("address", validators=[InputRequired("address is required")])
    date = DateField("date", validators=[InputRequired("address is required")])
    gender = SelectField("gender", choices=[('male', 'Male'), ('female', 'Female')],  validators=[InputRequired("address is required")])

    phone = StringField("phone", validators=[InputRequired("Phone number is required")])
    covid = SelectField("covid", choices=[('Recovered', 'Recovered / Tested Negative'), ('Uninfected', 'Uninfected / No Covid History')],  validators=[InputRequired("Covid record is required")])
    bloodgroup = SelectField("bloodgroup", choices=[('A Positive', 'A postive (A+)'),('A Negative','A postive (A-)'),('B Positive','B Positive (B+)'),
     ('B Negative', 'B Negative (B-)'), ('O Positive','O postive (O+)'),('O Negative','O Negative (O-)'),('AB Positive','AB postive (AB+)'),('AB Negative','AB Negative (AB-)')
     ],  validators=[InputRequired("bloodgroup is required")])


    pass1 = PasswordField("pass1", validators=[InputRequired("Password is required"), EqualTo('pass2', message="Passwords must match"), Length(min=4, max=30, message="Length must be between 4 and 30")])
    pass2 = PasswordField("pass2")

class ForgetPassword(FlaskForm):
    email = EmailField("email", validators=[InputRequired("Email is required"), Email()])

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        sql = f"SELECT * FROM USERS WHERE EMAIL='{escape(email)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        dic = ibm_db.fetch_both(stmt)
        if not dic or password != dic['PASSWORD']:
            flash("Incorrect email or password", "error")
            return redirect(url_for('home'))

        session['username'] =  dic['USERNAME']
        return redirect(url_for('ho'))
    else:
        return render_template("signin.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()

    if request.method=='POST' and form.validate_on_submit():
        username = str(request.form['username'])
        email = str(request.form['email'])
        address = str(request.form['address'])
        date= str(request.form['date'])
        gender= str(request.form['gender'])
        phone= str(request.form['phone'])
        covid=str(request.form['covid'])
        bloodgroup=str(request.form['bloodgroup'])
        pass1 = str(request.form['pass1'])
        pass2 = str(request.form['pass2'])
        print("----------------------------------------------------------")
        print(len(username), len(email), len(address), len(date), len(gender), len(phone), len(covid), len(bloodgroup), len(pass1), len(pass2))
        sql = f"SELECT * FROM USERS WHERE EMAIL='{escape(email)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        dic = ibm_db.fetch_both(stmt)
        if dic:
            flash("User with the email already exist", "error")
            return redirect(url_for('login'))
        sql = "INSERT INTO USERS (USERNAME, PASSWORD, EMAIL, BLOODGROUP, DATE, GENDER, PHONE, ADDRESS, COVID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(prep_stmt, 1, username)
        ibm_db.bind_param(prep_stmt, 2, pass1)
        ibm_db.bind_param(prep_stmt, 3, email)
        ibm_db.bind_param(prep_stmt, 4, bloodgroup)
        ibm_db.bind_param(prep_stmt, 5, date)
        ibm_db.bind_param(prep_stmt, 6, gender)
        ibm_db.bind_param(prep_stmt, 7, phone)
        ibm_db.bind_param(prep_stmt, 8, address)
        ibm_db.bind_param(prep_stmt, 9, covid)
        
        print(prep_stmt)
        ibm_db.execute(prep_stmt)
        flash("Registration Successful", "success")
        response = redirect(url_for('home'))
        return response
    else:
        return render_template("signup.html", form=form)

@app.route('/home')
def ho():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
