import hashlib
import os

def has_password(password):
    salt = os.urandom(16).hex()  # Generate a random salt
    salted_password = password + salt  # Combine password with salt
    hashed = hashlib.sha256(salted_password.encode()).hexdigest()  # Generate the hash
    return f"{salt}:{hashed}"  # Store the salt and hash together

def verify_password(db_password, input_password):
    try:
        salt, stored_hash = db_password.split(':')  # Split the salt and hash
        salted_password = input_password + salt  # Combine input password with the stored salt
        hashed = hashlib.sha256(salted_password.encode()).hexdigest()  # Hash the salted password
        return hashed == stored_hash  # Compare the hashes
    except ValueError:
        return False  # Return False if the stored password format is invalid