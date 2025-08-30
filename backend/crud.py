from sqlalchemy.orm import Session
from database import Conversation, Message
from datetime import datetime
from typing import List, Optional

def create_conversation(db: Session, conversation_id: str) -> Conversation:
    """Create a new conversation"""
    db_conversation = Conversation(id=conversation_id)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_conversation(db: Session, conversation_id: str) -> Optional[Conversation]:
    """Get conversation by ID"""
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def create_message(
    db: Session,
    conversation_id: str,
    role: str,
    content: str,
    slides_html: Optional[str] = None,
    theme_suggestion: Optional[str] = None,
    slides_generated: bool = False
) -> Message:
    """Create a new message"""
    db_message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        slides_html=slides_html,
        theme_suggestion=theme_suggestion,
        slides_generated=slides_generated
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_conversation_messages(db: Session, conversation_id: str) -> List[Message]:
    """Get all messages for a conversation"""
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp).all()

def get_recent_conversations(db: Session, limit: int = 10) -> List[Conversation]:
    """Get recent conversations"""
    return db.query(Conversation).order_by(
        Conversation.updated_at.desc()
    ).limit(limit).all()
