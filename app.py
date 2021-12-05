from flask import Flask, render_template, request, flash, redirect, url_for
from passwordManager import *
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
masterPass = "_"

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    global masterPass
    print(masterPass)
    error = None
    if request.method == 'POST':
        masterPass = request.form['password']
        print(masterPass)
        if(checkPassRequirements(masterPass) != 1):
            error = 'Password does not meet requirements. Please try again.'
            render_template('login.html', error=error)
        bool = authenticate(request.form['username'], request.form['password'])
        #print(bool)
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if (bool) == -1:
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('index.html', error=error)#redirect(url_for('login'))
    return render_template('login.html', error=error)

@app.route('/')
def index():
    global masterPass
    masterPass = "homePage"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
