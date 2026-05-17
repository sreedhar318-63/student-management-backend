from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "vishnu-vardhan-markapuram-kuppam-engineering-college"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(username: str)->str:
    payload ={
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token:str)->str:
    """Decode and verify the token. Return the username, or rise JWTError."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if not username:
        raise JWTError("Token has no subject")
    return username
