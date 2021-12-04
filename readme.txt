To Do list 
  Brandon
    Convert Password Manager functions in python
  
  Jared
    start to build web framework
    Pages:
      Login Page(Default)-Includes username and password boxes and submit button and link to registration page.
      Registration Page-Includes username and password boxes and submit button.
      Password Manager Page-Includes all stored usernames and passwords and logout button.
      
  Overall Project Flow:
    User registers a master username and password that fits the password criteria from backend program. If it doesn't, the user will be prompted to fix the criteria. 
    When successful, the password is hashed and sent to passwords.txt and the user is taken to password manager page. The user can add a website, username, and password. 
    The password is then checked for criteria and if it doesn't match, the user is asked if they are sure they want to use this password. 
    If they pick a password, the encryption of this is sent to passwords.txt, while the plaintext password is still displayed on the webpage. 
    On logout the user is taken back to the login page. When the user logs in, the hash of their password is checked with the hash in passwords.txt. 
    If it matches, they are taken to the password manager and all passwords from passwords.txt are decrypted and given to the webpage to be displayed.
    Passwords in passwords.txt always remain encrypted in the file.
  Nice to haves:
