from flask import Flask, render_template, request, flash, redirect, url_for
from passwordManager import *
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
username = "_"
masterPass = "_"
loggedIn = False

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    global username
    global masterPass
    global loggedIn
    loggedIn = False
    error = None
    if request.method == 'POST' and request.form['button'] == 'Login':
        username = request.form['username']
        masterPass = request.form['password']
        print(masterPass)
        print(checkPassRequirements(masterPass) != 1)
        if(checkPassRequirements(masterPass) != 1):#make sure password is decent
            error = 'Password does not meet requirements. Please try again.'
            return render_template('login.html', error=error)

        num = authenticate(username, masterPass)
        print(num)
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if (num) == -1:
            error = 'Invalid Credentials. Please try again.'
        else:
            loggedIn = True
            return redirect(url_for('manager'))
    elif request.method == 'POST' and request.form['button'] == 'Register':
        username = request.form['username']
        masterPass = request.form['password']
        if(checkPassRequirements(masterPass) != 1):#make sure password is decent
            error = 'Password does not meet requirements. Please try again.'
            return render_template('login.html', error=error)

        setupFile(username, masterPass)
        return redirect(url_for('login'))
    return render_template('login.html', error=error)

@app.route('/manager')
def manager():
    global loggedIn
    if(not loggedIn):
        return redirect(url_for('login'))
    global masterPass
    error = None
    data=[]
    lines = readAllFromFile(masterPass).split("\n")
    for line in lines:
        items = line.split(",")
        i = 0
        dict = {}
        for item in items:
            print(item)
            if item == '':
                pass
            else:
                if i==0:
                    dict.update({"website":item})
                elif i==1:
                    dict.update({"username":item})
                elif i==2:
                    dict.update({"password":item})
                i += 1
        data.append(dict)


    return render_template('manager.html',error=error,data=data)

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
