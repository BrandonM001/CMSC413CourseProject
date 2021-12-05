#CMSC 413 Password Manager
#This is the security code
#Made by Brandon Mohan and Jared Dunnn

import random
import re
from passlib.hash import scrypt
import cryptocode

masterPass = ""

def setupFile(user, password):
    #set up passwords.txt and put hashes
    file = open("passwords.txt", "w")
    #assume user/password meets requirements cause Jared checks them
    salt = random.randint(1000,9999)
    saltedPass = password + str(salt)
    hashPass = scrypt.hash(saltedPass)#str(hash(saltedPass))
    saltedHashPass = hashPass + str(salt)
    line = str(user) + "|" + str(saltedHashPass) +"\n"
    masterPass = password

    #print(password)
    #print(salt)
    #print(saltedPass)
    #print(hashPass)
    #print(saltedHashPass)

    file.write(line)
    file.close()

def authenticate(username, password):
    #grab hashes from file and check
    file = open("passwords.txt", "r")
    creds = file.readline().split("|")
    file.close()
    grabPass = "".join(creds[1]).strip() #creds[0].strip() #(creds[1])[0:-1]
    salt = (grabPass)[-4:]
    saltedPass = password + str(salt)
    passHash = grabPass[0:-4]
    #hashPass = str(scrypt.hash(saltedPass))
    #saltedHashPass = hashPass[2] + str(salt)
    #print(grabPass)
    #print(password)
    #print(salt)
    #print(saltedPass)
    #print(hashPass)
    #print(saltedHashPass)
    if((creds[0] == username) and (scrypt.verify(saltedPass, passHash))):#grabPass == saltedHashPass)):
        masterPass = password
        return 1
    return -1

def checkPassRequirements(password):
    #call when user enters password
    if(len(password) < 8):
        return "length < 8"
    if(not((re.search(".*[0-9].*", password)) and (re.search(".*[a-zA-Z]+.*", password)))):
        return "Need # and letter"
    if(not(hasConsecLetters(password))):
        return "No consecutive letters"

    return 1

def hasConsecLetters(word):
    word = word.lower().strip()
    consecLetters = 0
    seqLetters = 0
    preqLetters = 0
    for i in range(len(word) - 1):
        #print(word[i])
        if(word[i] == word[i+1]):
            consecLetters +=1
        elif chr(ord(word[i])+1) == word[i+1]:
            seqLetters +=1
        elif chr(ord(word[i])-1) == word[i+1]:
            preqLetters +=1
        else:
            consecLetters = 0
            seqLetters = 0
            preqLetters = 0
        if(consecLetters == 3 or seqLetters == 3 or preqLetters == 3):
            return 0

    return 1

def decryptPass(password, masterPass):
    return cryptocode.decrypt(password, masterPass)

def encryptPass(cipher, masterPass):
    return cryptocode.encrypt(cipher, masterPass)

def addToFile(website, username, password, masterPass):
    file = open("passwords.txt", "a")
    cipher = encryptPass(password, masterPass)
    file.write(website + "," + username + "," + cipher + "\n")
    file.close()
    return 1

def wipeAllPasswords():
    file = open("passwords.txt", "r")
    creds = file.readline()
    file.close()
    file = open("passwords.txt", "w")
    file.write(creds)#doesn't delete passwords, fix later
    file.close()

def ReplaceInFile(username, password):
    return 0

def readAllFromFile(masterPass):
    #decrypt things here
    file = open("passwords.txt", "r")
    lines = file.readlines()
    entries = ""
    #print(lines)
    for line in lines[1:]:
        print("line: " + line)
        line = line.strip()
        data = line.split(",")
        data[2] = decryptPass(data[2], masterPass)
        entries += data[0] + "," + data[1] + "," + str(data[2]) + ",\n"
    #print(entries)
    return entries

def findFromFile(username):
    file = open("passwords.txt", "r")
    lines = file.readLines()
    for line in lines:
        creds = line.split(",")
        if(creds[1] == username):
            return creds[0]
    return 0

def main():
    setupFile("useer", "passs1256")
    #print("auth")
    #print(authenticate("useer", "passs"))
    #cipher = encryptPass("dumb", "plants")
    #print(cipher)
    #print(decryptPass(cipher, "plants"))
    addToFile("Walmart", "bob", "passz", "passs1256")
    addToFile("Target", "Tom", "reallycool", "passs1256")
    print(readAllFromFile("passs1256"))
    #print(checkPassRequirements("kek49282d4321"))
#J sends seach entry of password file

if __name__ == "__main__":
    main()
