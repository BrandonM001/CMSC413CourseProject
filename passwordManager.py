#CMSC 413 Password Manager
#This is the security code
#Made by Brandon Mohan and Jared Dunnn
#This file works to transfer data between the file and the webpage

import random
import re
from passlib.hash import scrypt #used to generate hash
import cryptocode #used to encrypt/decrypt passwords

masterPass = ""#initialize variable

#---------------Function setupFile------------------------
#This function runs when a new user is created.
#It works to set up passwords.txt and put the master credentials into hashes in the file
def setupFile(user, password):
    file = open("passwords.txt", "w")#open file
    #assume user/password meets requirements cause Jared checks them
    salt = random.randint(1000,9999)#add random 4 digit salt
    saltedPass = password + str(salt)#append salt to password
    hashPass = scrypt.hash(saltedPass)#hash the pass
    saltedHashPass = hashPass + str(salt)#add salt to the end of hash
    line = str(user) + "|" + str(saltedHashPass) +"\n" #syntax to organize file
    masterPass = password

    file.write(line)#write credentials to file
    file.close()#close file

#---------------Function authenticate-------------------
#runs when a user logs in via credentials
#it computes hashes of the entered credentials and compares them to the hashes in the file
def authenticate(username, password):
    file = open("passwords.txt", "r")#open and read from text file
    creds = file.readline().split("|")#parse file input
    file.close()#close file now that we have what we need
    grabPass = "".join(creds[1]).strip() #remove file syntax and grab password
    #creds[0].strip() #(creds[1])[0:-1]
    salt = (grabPass)[-4:]#get hash salt
    saltedPass = password + str(salt)#append salt to potential password
    passHash = grabPass[0:-4]#get stored password hash without appended salt
    if((creds[0] == username) and (scrypt.verify(saltedPass, passHash))):#check if credentials match
        masterPass = password
        return 1
    return -1

#determines if string meets password requirements
def checkPassRequirements(password):
    #call when user enters password
    if(len(password) < 8):#meet length requirements
        return "length < 8"
    if(not((re.search(".*[0-9].*", password)) and (re.search(".*[a-zA-Z]+.*", password)))):
        #does password have at least 1 letter and 1 number?
        return "Need # and letter"
    if(not(hasConsecLetters(password))):#does it have more than 3 consecutive characters?
        return "No consecutive letters"

    return 1

def hasConsecLetters(word):#checks if string has consecutive characters
    word = word.lower().strip()#make string as basic as possible
    consecLetters = 0#checks for consecutive characters ex. 33333 or aaaaa
    seqLetters = 0  #checks for sequential characters ex. abcde or 12345
    preqLetters = 0 #checks for sequential characters ex. edcba or 54321
    for i in range(len(word) - 1):#for each character in a word
        #print(word[i])
        if(word[i] == word[i+1]):#if character is repeated
            consecLetters +=1
        elif chr(ord(word[i])+1) == word[i+1]:#if character increments by 1
            seqLetters +=1
        elif chr(ord(word[i])-1) == word[i+1]:#if character increments by 1
            preqLetters +=1
        else:#if no characters have consecutive issues, return them to 0
            consecLetters = 0
            seqLetters = 0
            preqLetters = 0
        if(consecLetters == 3 or seqLetters == 3 or preqLetters == 3):#character has too much repetition
            return 0

    return 1

def decryptPass(password, masterPass):#decrypt the string using the masterpassword
    return cryptocode.decrypt(password, masterPass)

def encryptPass(cipher, masterPass):#encrypt the string using the masterpassword
    return cryptocode.encrypt(cipher, masterPass)

def addToFile(website, username, password, masterPass):#add given password to file
    file = open("passwords.txt", "a")#open file
    cipher = encryptPass(password, masterPass)#encrypt password before adding it
    file.write(website + "," + username + "," + cipher + "\n")#add file syntax and write
    file.close()#close file
    return 1

def wipeAllPasswords():#wipe the file
#this is a test function, doesn't run in production
    file = open("passwords.txt", "r")
    creds = file.readline()
    file.close()
    file = open("passwords.txt", "w")
    file.write(creds)#doesn't delete passwords, fix later
    file.close()

def removeLine(website, username):#removes specific entry from password file
    #print(website)
    #print(username)
    file = open("passwords.txt", "r")#open file
    lines = file.readlines() #grab data
    bool = ""#keep track of if we delete an entry
    file.close()
    fileWrite = open("passwords.txt", "w")#open file in write mode
    fileWrite.write(lines[0])#rewrite the master credentials
    for line in lines[1:]:#for each password entry
        #line = line.strip("\n")
        #print("line: " + line)
        data = line.split(",") #add file syntax
        #print(data[0])
        #print(data[1])
        if(data[0] != website or data[1] != username):#rewrite to file if not what we're looking for
            print(line)
            fileWrite.write(line)
        else:
            bool += line#we removed a line

    #file.close()
    fileWrite.close()#close files
    return bool

def readAllFromFile(masterPass):#grab everything from file and return it
    file = open("passwords.txt", "r")#open file
    lines = file.readlines()#grab from file
    entries = ""
    #print(lines)
    for line in lines[1:]:#for each line of the file (excluding master creds)
        print("line: " + line)
        line = line.strip()
        data = line.split(",")#remove file syntax
        data[2] = decryptPass(data[2], masterPass)#decrypt passwords
        entries += data[0] + "," + data[1] + "," + str(data[2]) + "\n"#prep to send to website
    #print(entries)
    file.close()#close file
    return entries

def findFromFile(username):#finds an entry from the file and return it
    file = open("passwords.txt", "r")#opens the file
    lines = file.readLines()
    for line in lines:#for each line of file
        creds = line.split(",")#split creds
        if(creds[1] == username):#if we found the right username, return it
            return creds[0]
    return 0

def main():#doesn't run in prod, only used for testing
    #setupFile("useer", "passs1256")
    #print("auth")
    #print(authenticate("useer", "passs"))
    #cipher = encryptPass("dumb", "plants")
    #print(cipher)
    #print(decryptPass(cipher, "plants"))
    #addToFile("Walmart", "bob", "passz", "passs1256")
    #addToFile("Target", "Tom", "reallycool", "passs1256")
    #print(readAllFromFile("passs1256"))
    print(removeLine("Target", "Tom"))
    #print(checkPassRequirements("kek49282d4321"))
#J sends seach entry of password file

if __name__ == "__main__":#get main to run if file runs directly
    main()
