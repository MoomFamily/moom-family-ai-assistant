from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import User, Conversation, Message
from app.schemas import RegisterIn, LoginIn, TokenOut, ConversationIn, MessageIn
from app.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.config import settings
from app.providers.gemini import GeminiProvider
from app.retrieval.demo import search as demo_search

router=APIRouter()
@router.post('/auth/register',response_model=TokenOut)
def register(data:RegisterIn,db:Session=Depends(get_db)):
    email=data.email.lower()
    if db.query(User).filter_by(email=email).first(): raise HTTPException(409,'Email already registered')
    user=User(email=email,password_hash=hash_password(data.password)); db.add(user); db.commit(); db.refresh(user)
    return TokenOut(access_token=create_access_token(user.id))
@router.post('/auth/login',response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.query(User).filter_by(email=data.email.lower()).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,'Incorrect email or password')
    return TokenOut(access_token=create_access_token(user.id))
@router.get('/auth/me')
def me(user:User=Depends(get_current_user)): return {'id':user.id,'email':user.email}
@router.get('/conversations')
def list_conversations(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return db.query(Conversation).filter_by(owner_id=user.id).order_by(Conversation.id.desc()).all()
@router.post('/conversations')
def create_conversation(data:ConversationIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    c=Conversation(owner_id=user.id,title=data.title); db.add(c); db.commit(); db.refresh(c); return c
def owned(cid:int,db:Session,user:User):
    c=db.query(Conversation).filter_by(id=cid,owner_id=user.id).first()
    if not c: raise HTTPException(404,'Conversation not found')
    return c
@router.get('/conversations/{cid}/messages')
def get_messages(cid:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    c=owned(cid,db,user); return c.messages
@router.post('/conversations/{cid}/messages')
def send_message(cid:int,data:MessageIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    c=owned(cid,db,user); db.add(Message(conversation_id=c.id,role='user',content=data.content)); db.commit()
    evidence=[]
    if settings.retrieval_enabled:
        if settings.retrieval_backend=='qdrant':
            provider=GeminiProvider(); from app.retrieval.qdrant import QdrantRetriever
            evidence=QdrantRetriever(provider.embed).search(data.content)
        else: evidence=demo_search(data.content)
    provider=GeminiProvider(); prompt='You are a helpful assistant. Answer clearly. If context is insufficient, say so.\nCONTEXT:\n'+'\n'.join(evidence)+'\nUSER QUESTION:\n'+data.content
    answer=provider.generate(prompt)
    db.add(Message(conversation_id=c.id,role='assistant',content=answer)); db.commit()
    return {'role':'assistant','content':answer}
@router.patch('/conversations/{cid}')
def rename(cid:int,data:ConversationIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    c=owned(cid,db,user); c.title=data.title; db.commit(); return c
@router.delete('/conversations/{cid}')
def delete(cid:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    c=owned(cid,db,user); db.delete(c); db.commit(); return {'deleted':True}
