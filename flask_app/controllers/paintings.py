from flask_app import app, render_template, request, redirect, session, bcrypt, flash
from flask_app.models.painting import Painting



# TODO ROOT ROUTE


@app.route('/painting/new')
def painting_new():
    if 'artist_id' not in session:
        return redirect('/logout')
    return render_template("add_new.html")


@app.route("/add_painting", methods=["POST"])
def add_painting():
   if not Painting.validate_painting(request.form):
        return redirect('/painting/new')
   print(request.form)
   Painting.save(request.form)
   return redirect('/dashboard')


@app.route('/painting/<int:id>')
def show(id):
    if 'artist_id' not in session:
        return redirect('/logout')
    data = {'id':id}
    return render_template('show.html', painting=Painting.get_one(data))

@app.route('/dashboard')
def dashboard():
    if 'artist_id' not in session:
        return redirect('/logout')
    return render_template('all_paintings.html', paintings=Painting.get_all())     

 


# ! OPTIONAL

@app.route('/edit/<int:id>')
def edit_painting(id):
    if 'artist_id' not in session:
        return redirect('/logout')
    data = {'id':id}
    return render_template('edit_painting.html', painting = Painting.get_one(data))

@app.route('/update/painting', methods = ['POST'])
def update_painting():
    Painting.update(request.form)
    return redirect('/dashboard')


@app.route('/delete/<int:id>')
def delete_painting(id):
    data = {'id': id}
    Painting.destroy(data)
    return redirect('/dashboard')





# TODO LOGOUT
@app.route('/logout')
def logout():

    session.clear()
    return redirect('/')


# @app.route("/result")
# def result():
#     return render_template('add_new.html', paintings= Painting.get_all())











