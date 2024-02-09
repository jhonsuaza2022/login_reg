from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:

    def __init__(self, data):
        self.id_usuarios = data['id_usuarios']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def valida_usuario(formulario):

        es_valido = True
        #Validar que el nombre tenga al menos 3 caracteres
        if len(formulario['nombre']) < 3 :
            flash('Nombre debe tener al menos 3 caracteres', 'registro')
            es_valido = False
        
        if len(formulario['apellido']) < 3 :
            flash('Apellido debe tener al menos 3 caracteres', 'registro')
            es_valido = False

        
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail invalido', 'registro')
            es_valido = False

        if len(formulario['password']) < 6 :
            flash('Contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False

        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas no coinciden', 'registro')
            es_valido = False

        query = "SELECT * FROM usuarios WHERE email = %(email)s"
        result = connectToMySQL('inicio_reg').query_db(query, formulario)
        if len(result) >=1:
            flash('E-mail registrado previamente', 'registro')
            es_valido = False

        return es_valido 
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s)"
        result = connectToMySQL('inicio_reg').query_db(query, formulario)
        return result
    
    @classmethod
    def get_by_email(cls, formulario):
        
        query = "SELECT * FROM usuarios WHERE email = %(email)s"
        result =connectToMySQL('inicio_reg').query_db(query, formulario) #LOS SELECT regresan una lista
        if len(result) < 1: #NO EXISTE REGISTRO CON ESE CORREO
            return False
        else:
            user = cls(result[0])
            return user
    @classmethod
    def get_by_id(cls, formulario):
        #formulario ={id:4}
        query ="SELECT * FROM usuarios WHERE id_usuarios = %(id_usuarios)s"
        result = connectToMySQL("inicio_reg").query_db(query, formulario)
        user = cls(result[0])
        return user