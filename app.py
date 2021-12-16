#CMSC 413 Course Project Fall 2021
#By Brandon Mohan and Jared Dun

from flask import Flask, render_template, request, flash, redirect, url_for
from passwordManager import *
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
username = "_"
masterPass = "_"#stores master creds
loggedIn = False#used to prevent users who aren't logged in from entering site

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])#login page
def login():
    global username#use the global variable
    global masterPass
    global loggedIn
    loggedIn = False
    error = None
    if request.method == 'POST' and request.form['button'] == 'Login':#if they click the login button
        username = request.form['username']
        masterPass = request.form['password']#grab entries
        print(masterPass)
        print(checkPassRequirements(masterPass) != 1)
        if(checkPassRequirements(masterPass) != 1):#make sure password is decent
            error = 'Password does not meet requirements. Please try again.'
            return render_template('login.html', error=error)

        num = authenticate(username, masterPass)#check if credentials match
        print(num)
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if (num) == -1:
            error = 'Invalid Credentials. Please try again.' #if credentials don't match
        else:
            loggedIn = True#user has logged in, redirect to password page
            return redirect(url_for('manager'))
    elif request.method == 'POST' and request.form['button'] == 'Register':#if they click the create account button
        username = request.form['username']
        masterPass = request.form['password']#get credentials from boxes
        if(checkPassRequirements(masterPass) != 1):#make sure password is decent
            error = 'Password does not meet requirements. Please try again.'
            return render_template('login.html', error=error)
        setupFile(username, masterPass)#set up the password file
        return redirect(url_for('login'))
    return render_template('login.html', error=error)

@app.route('/manager', methods=['GET', 'POST'])#passwords are displayed on this page
def manager():
    global loggedIn
    if(not loggedIn):#make sure the user is logged in
        return redirect(url_for('login'))#return to login page
    global masterPass
    error = None
    if request.method == 'POST' and request.form['button'] == 'Add':#if they want to add an entry
        if(len(request.form['website'].strip("\n")) > 0 and len(request.form['username'].strip("\n")) > 0 and len(request.form['password'].strip("\n")) > 0):#make sure they have all fields
            addToFile(request.form['website'],request.form['username'],request.form['password'],masterPass)#add credentials to file
    data=[]
    lines = readAllFromFile(masterPass).split("\n")#grab file contents
    length = len(lines)
    for i in range(length):#for each entry in file
        if request.method == 'POST' and request.form['button'] == 'DeleteEntry#'+str(i):#if they click the delete button
            entryToDelete = lines[i].split(",")
            removeLine(entryToDelete[0],entryToDelete[1])#delete the entry
            lines = readAllFromFile(masterPass).split("\n")
            length = len(lines)
    index = 0
    for line in lines:#put items in webpage
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
        dict.update({"index":str(index)})
        index+=1
        data.append(dict)
    del data[length-1]
    return render_template('manager.html',error=error,data=data)

@app.route('/')
def index():
    return redirect(url_for('login'))#no home page, just login

if __name__ == '__main__':
    app.run(debug=True)
