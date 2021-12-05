from flask import Flask, render_template, request, flash, redirect, url_for
from passwordManager import *

app = Flask(__name__)
masterPass = "_"

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    global masterPass
    error = None
    if request.method == 'POST':
        print(masterPass)
        masterPass = request.form['password']
        print(masterPass)
        num = authenticate(request.form['username'], request.form['password'])
        print(num)
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if (num) == -1:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('login'))
    return render_template('login.html', error=error)

@app.route('/')
def index():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)