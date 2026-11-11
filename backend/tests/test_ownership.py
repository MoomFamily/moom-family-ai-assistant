from app.models import User, Conversation
def test_conversation_owner_relationship_model():
    user=User(email='test@example.com',password_hash='hash')
    conversation=Conversation(owner=user,title='private')
    assert conversation.owner is user
