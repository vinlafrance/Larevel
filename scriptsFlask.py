from flask import Flask
import hashlib, binascii, os

app = Flask(__name__)
@app.route("/")
def main():
    return "Bonjour et bienvenu!"


if __name__ == "__main__":
    app.run()



def verify_password(stored_password, provided_password):
    #Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password