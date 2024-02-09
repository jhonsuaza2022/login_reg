from flask import render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.usuarios import Usuario

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not Usuario.valida_usuario(request.form):
        return redirect('/')
    
    pwd = bcrypt.generate_password_hash(request.form['password'])# encritamos el password del usuario

    formulario = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"],
        "password": pwd
    }


    id_usuarios = Usuario.save(formulario) #RECIBO EL IDENTIFICADOR DEL NUEVO USUARIO

    session['user_id'] = id_usuarios
    return redirect('/dashboard')


@app.route("/login", methods=['POST'])
def login():
    #VERIFICAR QUE EL EMAIL EXISTA
    user = Usuario.get_by_email(request.form) #RECIBIENDO UNA INSTACIA DE USUSARIO FALSO

    if not user:
        flash('E-mail no encontrado', 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')
        
    session['user_id'] = user.id_usuarios

    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    

    formulario = {"id_usuarios": session['user_id']}
    user = Usuario.get_by_id(formulario)
    
    return render_template('dashboard.html', user = user)
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

    