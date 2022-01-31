from this import d
from flask import render_template,redirect, request,session,flash
from usuario import app
from usuario.models.model_pais import Country
from usuario.models.model_estado_civil import CivilStatus
from usuario.models.model_usuario import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def load_page():
    countries = Country.getCountry()
    status = CivilStatus.getCivilStatus()
    return render_template('index.html',countries=countries,status=status)

@app.route('/dashboard')
def load_dashboard():
    if 'name' in session:
        return render_template('dashboard.html')
    else:
        return redirect('/')

@app.route('/login',methods=["POST"])
def login():
    user = {
        "email" : request.form["input_email_login"],
        "password" : request.form["input_password_login"]
    }
    password = request.form["input_password_login"]
    if(User.verifyDataUserLogin(user)):
        resultado = User.getUserxEmail(user)
        if(resultado != None):
            if not (bcrypt.check_password_hash(resultado.password,password)):
                flash("Invalid credentials","login")
                return redirect("/")
            else:
                session["name"] = resultado.nombres
                session["id"] = resultado.id
                return redirect("/dashboard")
        else:
            flash("Invalid credentials","login")
            return redirect('/') 
    else:
        return redirect('/')

@app.route('/register',methods=["POST"])
def register():
    user = {
        "nombres" : request.form["input_first_name"], 
        "apellidos" : request.form["input_last_name"],
        "email" : request.form["input_email"],
        "celular" : request.form["input_cell_phone_number"], 
        "direccion" : request.form["input_address"],
        "sexo" : request.form["input_sexo"],
        "fecha_nacimiento" : request.form["input_date_birth"],
        "pais" : request.form["select_country"],
        "ciudad" : request.form["input_city"],
        "codigo_postal" : request.form["input_postal_code"],
        "estado_civil" : request.form["select_civil_status"],
        "recibir_correos" : len(request.form.getlist("input_check")),
        "password" : request.form["input_password"],
        "confirm_password" : request.form["input_confirm_password"]
    }
    if(User.verifyDataUserRegister(user)):
        user["password"] = bcrypt.generate_password_hash(request.form["input_password"])
        result = User.addUser(user)
        if(result > 0):
            session["name"] = request.form["input_first_name"]
            session["id"] = result
            return redirect('/dashboard')
        else:
            flash("An error occurred while trying to save the data","register")
            return redirect('/')
    else:
        return redirect('/')


@app.route('/logout',methods=["POST"])
def logout():
    session.clear()
    return redirect('/')