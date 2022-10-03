from flask import render_template, redirect, request, session
from flask_app import app

from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    #validamos la info que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')

    #guardar registro
    pwd = bcrypt.generate_password_hash(request.form['password'])#encriptar la contraseña del usuario y guardandola en pwd

    #creamos un diccionario con todos los datos del request.form:
    formulario = {
        "first_name" : request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #recibir el identificador del nuevo usuario

    session['user_id'] = id #guardamos en session el identificador del usuario
    return redirect('/dashboard')

#pendiente guardar registro

@app.route('/dashboard')
def dashboard():
    #pendiente validar que si se haya iniciado sesion o registrarme
    return render_template('dashboard.html')




    