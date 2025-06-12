from jogoteca import app
from helpers import FormularioUsuario
from flask import url_for, render_template, session, request, flash, redirect
from models import Usuarios
from flask_bcrypt import check_password_hash

@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    if not proxima:
        proxima = url_for('index')
    form = FormularioUsuario()

    return render_template('login.html', proxima=proxima, form=form)

@app.route("/autenticar", methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)

    if usuario and senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuario ou senha invalida')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'usuario_logado' not in session:
        flash('Usuario nao logado')
        return redirect(url_for('index'))
    else:
        session['usuario_logado'] = None
        flash('Logout efetuado com sucesso!')
        return redirect(url_for('index'))
    #return redirect(url_for('index'))
