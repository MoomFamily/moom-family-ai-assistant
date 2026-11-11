import base64, hashlib, hmac, json, secrets, time
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db import get_db
from app.models import User

_bearer = HTTPBearer(auto_error=False)
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16); rounds = 310_000
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, rounds)
    return f'pbkdf2_sha256${rounds}${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}'
def verify_password(password: str, encoded: str) -> bool:
    try:
        algo, rounds, salt, expected = encoded.split('$')
        if algo != 'pbkdf2_sha256': return False
        actual = hashlib.pbkdf2_hmac('sha256', password.encode(), base64.urlsafe_b64decode(salt), int(rounds))
        return hmac.compare_digest(base64.urlsafe_b64encode(actual).decode(), expected)
    except Exception: return False
def create_access_token(user_id: int) -> str:
    if settings.secret_key == 'change-me-before-use': raise RuntimeError('Set SECRET_KEY before issuing tokens')
    enc=lambda b: base64.urlsafe_b64encode(b).rstrip(b'=').decode()
    header=enc(b'{"alg":"HS256","typ":"JWT"}')
    payload=enc(json.dumps({'sub':str(user_id),'exp':int(time.time())+settings.access_token_minutes*60}).encode())
    body=f'{header}.{payload}'
    sig=enc(hmac.new(settings.secret_key.encode(),body.encode(),hashlib.sha256).digest())
    return f'{body}.{sig}'
def decode_access_token(token: str) -> int:
    try:
        h,p,s=token.split('.'); body=f'{h}.{p}'
        expected=base64.urlsafe_b64encode(hmac.new(settings.secret_key.encode(),body.encode(),hashlib.sha256).digest()).rstrip(b'=').decode()
        if not hmac.compare_digest(s,expected): raise ValueError()
        payload=json.loads(base64.urlsafe_b64decode(p+'='*(-len(p)%4)))
        if int(payload['exp']) < int(time.time()): raise ValueError()
        return int(payload['sub'])
    except Exception: raise HTTPException(status_code=401, detail='Invalid or expired token')
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_bearer), db: Session = Depends(get_db)) -> User:
    if not credentials: raise HTTPException(status_code=401, detail='Authentication required')
    user=db.get(User,decode_access_token(credentials.credentials))
    if not user or not user.is_active: raise HTTPException(status_code=401, detail='Invalid account')
    return user
