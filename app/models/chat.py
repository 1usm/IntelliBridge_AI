from datetime import datetime
from app import db

class Chat(db.Model):
    __tablename__ = 'chats'
    
    id = db.Column(db.String(36), primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }