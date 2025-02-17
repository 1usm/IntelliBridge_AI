from typing import Dict, Tuple
import logging
from app.models.chatbot import ChatGPTBot
from app.models.chat import Chat
from app import db
from config import Config

logger = logging.getLogger(__name__)

class ChatBotService:
    def __init__(self):
        """Initialize the ChatBot service with configuration."""
        try:
            self.bot = ChatGPTBot(
                api_key=Config.OPENAI_API_KEY,
                model_name=Config.MODEL_NAME
            )
        except Exception as e:
            logger.error(f"Error initializing ChatGPTBot: {str(e)}")
            raise

    def create_prompt(self, prompt: str) -> Tuple[Dict, int]:
        """Create a new prompt and return its ID."""
        try:
            prompt_id = self.bot.create_prompt(prompt)
            
            # Save to database
            chat = Chat(id=prompt_id, user_message=prompt)
            db.session.add(chat)
            db.session.commit()
            
            return {"prompt_id": prompt_id, "message": "Prompt created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating prompt: {str(e)}")
            return {"error": str(e)}, 500

    def get_response(self, prompt_id: str) -> Tuple[Dict, int]:
        """Get a response for a specific prompt."""
        try:
            chat = Chat.query.get(prompt_id)
            if not chat or chat.is_deleted:
                return {"error": "Prompt not found"}, 404

            if not chat.bot_response:
                response = self.bot.get_response_sync(prompt_id)
                if response:
                    chat.bot_response = response
                    db.session.commit()
                else:
                    return {"error": "Failed to get response"}, 500

            return {"response": chat.bot_response}, 200
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            return {"error": str(e)}, 500

    def get_chat_history(self) -> Tuple[Dict, int]:
        """Get all chat history."""
        try:
            chats = Chat.query.filter_by(is_deleted=False).order_by(Chat.created_at.desc()).all()
            return {"chats": [chat.to_dict() for chat in chats]}, 200
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            return {"error": str(e)}, 500

    def delete_chat(self, chat_id: str) -> Tuple[Dict, int]:
        """Soft delete a chat."""
        try:
            chat = Chat.query.get(chat_id)
            if not chat or chat.is_deleted:
                return {"error": "Chat not found"}, 404

            chat.is_deleted = True
            db.session.commit()
            return {"message": "Chat deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting chat: {str(e)}")
            return {"error": str(e)}, 500