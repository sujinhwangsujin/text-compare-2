import jwt
from typing import Optional
import os

def generate_jwt(target_url: str, role: str, jwt_secret: Optional[str] = None):
    if jwt_secret is None:
        #jwt_secret = os.environ["jwt_secret"]
        jwt_secret = "reallyreallyreallyreallyverysafe"
    return jwt.encode({"role": role, "aud": target_url}, jwt_secret, algorithm="HS256")
 