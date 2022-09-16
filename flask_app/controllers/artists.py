from flask_app import app, render_template, request, redirect, session, bcrypt, flash
from flask_app.models.artist import Artist



# TODO ROOT ROUTE
@app.route('/')
def index():
    return render_template('index.html')



# TODO REGISTER
@app.route('/register/artist', methods = ['POST'])
def register():
    if not Artist.validate_artist(request.form):
        return redirect('/')

    hashed_pw = bcrypt.generate_password_hash(request.form['password'])

    artist_data = {
        'first_name': request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password': hashed_pw
    }

    artist_id = Artist.save(artist_data)
    session['artist_id'] = artist_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']

    return redirect('/dashboard')


# TODO LOGIN
@app.route('/login', methods = ['POST'])
def login():
    artist = Artist.get_by_email(request.form)
    if not artist:
        flash("invalid credentials")
        return redirect('/')
    password_valid = bcrypt.check_password_hash(artist.password, request.form['password'])

    if not password_valid:
        flash("invalid credentials")
        return redirect('/')
    session['artist_id'] = artist.id
    session['first_name'] = artist.first_name
    session['last_name'] = artist.last_name


    return redirect('/dashboard')

 


