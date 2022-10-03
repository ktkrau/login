from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def valida_usuario(formulario):
        #formulario = DICCIONARIO con todos los names y valores que el usuario ingresa
        es_valido = True
        #Validamos que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash('El nombre debe tener al menos 3 caracteres', 'registro')
            es_valido = False
        if len(formulario['last_name']) < 3:
            flash('El apellido debe tener al menos 3 caracteres', 'registro')
            es_valido = False
        if len(formulario['password']) < 3:
            flash('La contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False
        #Verificamos que las contraseñas coincidan 
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas NO coinciden', 'registro')
            es_valido = False
        #Revisamos que el email tenga el formato correcto -> Expresiones regulares
        if not EMAIL_REGEX.match(formulario['email']):
            flash('Email inválido', 'registro')
            es_valido = False
        #Consultamos si existe el correo electronico
        query = "SELECT * FROM users WHERE email =  %(email)s"
        results = connectToMySQL('login_registro').query_db(query, formulario)
        if len(results) >= 1:
            flash('Email registrado previamente', 'registro')
            es_valido = False

        return es_valido

    @classmethod
    def save(cls,formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s) "
        result = connectToMySQL('login_registro').query_db(query, formulario)
        return result 