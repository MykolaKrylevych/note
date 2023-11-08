from app import app, send_email
from models import db, User, Notes
from forms import LoginForm, RegisterForm, ResetPasswortForm, NewPasswordForm
from flask import request, redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, login_required, logout_user


with app.app_context():
    db.create_all()


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.", 'warning')
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.', 'danger')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    form = ResetPasswortForm()
    if form.validate_on_submit():

        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
        if not user:
            flash("That email does not exist, please try again.", 'warning')
        else:
            send_email(user)
            flash("Reset request sent. Check your email.", "info")

    return render_template("reset_request.html", form=form)


@app.route("/password_reset_verified/<token>", methods=["GET", "POST"])
def reset_verified(token):
    user = User.verify_reset_token(token)
    form = NewPasswordForm()
    if form.validate_on_submit():
        user.set_new_password(form.password.data)

        return redirect(url_for("login"))

    return render_template("reset_verified.html", form=form, username=user.username)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/')
@login_required
def home():
    # in first realise used  notes = Notes.query.all() now we use this current_user.notes
    return render_template('note.html', notes=current_user.notes)


@app.route('/create', methods=['POST'])
@login_required
def create():
    note = request.form['note']
    notes_header = request.form['notes_header']
    color = request.form['selected_item']
    new_note = Notes(notes_header=notes_header, notes=note, border_color=color, user_id=current_user.id)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/update', methods=['POST'])
@login_required
def update():
    index = request.args.get("index")
    note_to_update = db.session.get(Notes, index)
    note_to_update.notes = request.form['note_edit']
    note_to_update.notes_header = request.form['notes_header_edit']
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:index>')
@login_required
def delete(index):
    note = db.session.get(Notes, index)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.username = request.form["new_name"].strip()
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("profile.html")


@app.route("/delete-user/<int:user_id>")
@login_required
def delete_profile(user_id):
    logout_user()
    user = db.session.get(User, user_id)
    for note in user.notes:
        db.session.delete(note)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("register"))


if __name__ == '__main__':
    app.run(debug=True)
