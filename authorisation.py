import bcrypt
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

KEY=os.getenv('JWT_KEY')

#bcrypt always needs bytes to work on so it always necessary to convert it into bytes before passing to any of the bcrypt functions.
# bytea data types is returned as memory view from postgres so use bytes() to convert memoryview to bytes.
# .encode() and decode() works for string 
# for int .to_bytes() is used to convert to bytes
# This is one of the issues which i had to solve.

def Hasher(password):
    # This is the way to convert string to bytes and this 
    hashed=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed



def Checker(password, hashed):
    if bcrypt.checkpw(password.encode(), hashed):
        return True
    else:
        return False


def token(id, username):

    payload={"data_id": id, 
             "name": username}

    #payload is just to get the rough idea of the user. algorithm should be singular here and plural in decode.

    encoded=jwt.encode(payload, KEY, algorithm="HS256")

    return encoded
  

def verify(encoded):

      #This is the function for verification.
      
      decoded=jwt.decode(encoded, KEY, algorithms=["HS256"])
    
      return decoded









