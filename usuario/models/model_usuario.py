
from usuario.config.mysqlconnection import connectToMySQL
from flask import flash
import re

NAMES_REGEX = re.compile(r'^[A-Z][a-zA-Z ]{1,80}$')
SEXO_REGEX = re.compile(r'^[M|F|O]{1}$')
PASSWORD_REGEX = re.compile(r'^(.)*(?=\w*\d)(?=\w*[A-Z])\S{8,16}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CELL_PHONE_REGEX = re.compile(r'^[+]*[0-9]{2,3}[ -]+[0-9]{6,15}$')
FECHA_REGEX = re.compile(r'^[1-2]{1}[9|0|1]{1}[0-9]{2}[-][0-1]{1}[0-9]{1}[-][0-3]{1}[0-9]{1}$')
SELECT_REGEX = re.compile(r'^[0-9]{1,4}$')
CIUDAD_REGEX = re.compile(r'^[A-Z][a-zA-Z ]{1,79}$')
DIRECCION_REGEX = re.compile(r'^[A-Z].{1,79}$')
POSTAL_CODE_REGEX = re.compile(r'^[0-9]{4,10}$')

class User:
    name_db = "app_dojo"

    def __init__(self, id, nombres, apellidos, email, password, celular, direccion, sexo, fecha_nacimiento, pais, ciudad, codigo_postal, estado_civil, recibir_correos, created_at):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.password= password
        self.celular = celular
        self.direccion = direccion
        self.sexo = sexo 
        self.fecha_nacimiento = fecha_nacimiento
        self.pais = pais
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.estado_civil = estado_civil
        self.recibir_correos = recibir_correos
        self.created_at = created_at

    @classmethod
    def addUser(cls,user):
        query = '''
                    INSERT INTO user (nombres, apellidos, password, email, celular, direccion, sexo, fecha_nacimiento,
                    pais_id, ciudad, codigo_postal, estado_civil_id, recibir_correos, created_at) 
                    VALUES (%(nombres)s, %(apellidos)s, %(password)s, %(email)s, %(celular)s, %(direccion)s, %(sexo)s, %(fecha_nacimiento)s,
                    %(pais)s, %(ciudad)s, %(codigo_postal)s, %(estado_civil)s, %(recibir_correos)s, now())
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,user)
        return resultado

    @classmethod
    def getUserxEmail(cls,user):
        query = '''
                    SELECT u.*, e.nombre AS estado_civil, p.nombre AS pais
                    FROM user u
                    INNER JOIN estado_civil e ON e.id = u.estado_civil_id
                    INNER JOIN pais p ON p.id = u.pais_id
                    WHERE email = %(email)s;
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,user)
        if(len(resultado) > 0):
            user = User(resultado[0]["id"],resultado[0]["nombres"],resultado[0]["apellidos"],resultado[0]["email"],resultado[0]["password"],resultado[0]["celular"],
            resultado[0]["direccion"],resultado[0]["sexo"],resultado[0]["fecha_nacimiento"],resultado[0]["pais"],resultado[0]["ciudad"],resultado[0]["codigo_postal"],
            resultado[0]["estado_civil"],resultado[0]["recibir_correos"],resultado[0]["created_at"])
            return user
        else:
            return None
        
    @classmethod
    def verifyDataUserRegister(cls,user):
        print(user)
        is_valid = True
        if not NAMES_REGEX.match(user["nombres"]):
            flash("Invalid first name. Must have at least 2 characters. First letter must be capitalized","register")
            is_valid = False
        if not NAMES_REGEX.match(user["apellidos"]):
            flash("Invalid last name. Must have at least 2 characters","register")
            is_valid = False
        if not SEXO_REGEX.match(user["sexo"]):
            flash("Invalid sex. Please enter a correct value","register")
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address","register")
            is_valid = False
        else:
            data = {
                "email" : user["email"]
            }
            if(cls.getUserxEmail(data)!= None):
                flash("There is already a user with the email entered","register")
                is_valid = False
        if not PASSWORD_REGEX.match(user["password"]):
            flash("Invalid password. Must contain at least one capital letter and one number. Minimum of 8 characters and a maximum of 16","register")
            is_valid = False
        if not (user["password"] == user["confirm_password"]):
            flash("The confirmation password is not valid","register")
            is_valid = False
        if not CELL_PHONE_REGEX.match(user["celular"]):
            flash("Invalid Phone number. Separate your country code with a space or a - ","register")
            is_valid = False
        if not FECHA_REGEX.match(user["fecha_nacimiento"]):
            flash("Invalid date of birth","register")
            is_valid = False
        if not SELECT_REGEX.match(user["estado_civil"]):
            flash("You must select the civil status","register")
            is_valid = False
        if not SELECT_REGEX.match(user["pais"]):
            flash("You must select the country","register")
            is_valid = False
        if not CIUDAD_REGEX.match(user["ciudad"]):
            flash("Invalid city name. Must have at least 2 characters. First letter must be capitalized ","register")
            is_valid = False
        if not DIRECCION_REGEX.match(user["direccion"]):
            flash("Invalid address. Must have at least 2 characters. First letter must be capitalized ","register")
            is_valid = False
        if not POSTAL_CODE_REGEX.match(user["codigo_postal"]):
            flash("Invalid postal code. Must have at least 4 characters and a maximum of 10","register")
            is_valid = False
        return is_valid

    @classmethod
    def verifyDataUserLogin(self,user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address","login")
            is_valid = False
        if not PASSWORD_REGEX.match(user["password"]):
            flash("Invalid credentials","login")
            is_valid = False
        return is_valid