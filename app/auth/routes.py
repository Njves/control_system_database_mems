from email_validator import validate_email, EmailNotValidError
from flask import render_template, request, url_for, flash, Response
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect

from app import db
from app.auth import bp
from app.email import send_password_reset_email
from app.models import Account


@bp.route('/register', methods=['POST', 'GET'])
def register():
    form = request.form
    # if client send something - checks data
    if len(form) > 0:
        username = form['username']
        email = form['email']
        password = form['password']
        password_repeat = form['password_repeat']
        if password != password_repeat:
            flash('Пароли не совпадают')
            return redirect(url_for('auth.register'))
        user_account = Account(username=username, email=email)
        if Account.query.filter_by(username=user_account.username).first():
            flash('Такой пользователь уже существует')
            return redirect(url_for('auth.register'))
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            flash('Невалидный email')
            return redirect(url_for('auth.register'))
        user_account.set_password(password)
        db.session.add(user_account)
        db.session.commit()
        login_user(user_account)
        flash("Вы успешно вошли!")
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = request.form
    # if client send something - checks data
    if len(form) > 0:
        username_or_email = form['username_email']
        password = form['password']
        user_account: Account = Account.query.filter_by(username=username_or_email).first()
        if user_account is None:
            user_account: Account = Account.query.filter_by(email=username_or_email).first()
        if user_account is None or not user_account.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for("auth.login"))
        login_user(user_account)
        flash("Success!")
        return redirect(url_for('main.index'))
    return render_template('auth/signIn.html')

@bp.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    if request.form:
        recovered_account = Account.query.filter_by(email=request.form['recovery_email']).first()
        flash(request.form['recovery_email'])
        if not recovered_account:
            return redirect(url_for('auth.forgot_password'))
        send_password_reset_email(recovered_account)
        return render_template('auth/forgot.html', email=request.form['recovery_email'])
    return render_template('auth/forgot.html')

@bp.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token: str):
    account: Account = Account.verify_reset_password_token(token)
    if not account:
        return redirect(url_for('main.index'))
    if request.form:
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        if not account:
            return redirect(url_for('main.index'))
        if not request.form['new_password']:
            flash('Password must contain at least 6 characters')
            return redirect(url_for('auth.reset_password', token=token))
        if not 6 <= len(request.form['new_password']) <= 32:
            flash('The password does not meet the conditions')
            return redirect(url_for('auth.reset_password', token=token))
        form = request.form
        account.set_password(form['new_password'])
        db.session.commit()
        flash('Пароль успешно изменен')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
