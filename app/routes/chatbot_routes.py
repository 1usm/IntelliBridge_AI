from flask import Blueprint, request, jsonify, render_template
from app.services.chatbot_service import ChatBotService
from app.utils.helpers import validate_prompt
from app import limiter

main_bp = Blueprint('main', __name__)
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api')
chatbot_service = ChatBotService()

@main_bp.route('/')
def home():
    """Render the chat interface."""
    return render_template('chat.html')

@chatbot_bp.route('/prompts', methods=['POST'])
@limiter.limit("10 per minute")
def create_prompt():
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not validate_prompt(prompt):
        return jsonify({"error": "Invalid prompt"}), 400
        
    response, status_code = chatbot_service.create_prompt(prompt)
    return jsonify(response), status_code

@chatbot_bp.route('/chat-history', methods=['GET'])
def get_chat_history():
    """Get all chat history."""
    response, status_code = chatbot_service.get_chat_history()
    return jsonify(response), status_code

@chatbot_bp.route('/prompts/<prompt_id>', methods=['PUT'])
@limiter.limit("10 per minute")
def update_chat(prompt_id):
    data = request.get_json()
    new_prompt = data.get('prompt')

    response, status_code = chatbot_service.update_prompt(prompt_id, new_prompt)
    return jsonify(response), status_code

@chatbot_bp.route('/prompts/<prompt_id>', methods=['DELETE'])
def delete_chat(prompt_id):
    response, status_code = chatbot_service.delete_chat(prompt_id)
    return jsonify(response), status_code

@chatbot_bp.route('/prompts/<prompt_id>/response', methods=['GET'])
@limiter.limit("10 per minute")
def get_response(prompt_id):
    response, status_code = chatbot_service.get_response(prompt_id)
    return jsonify(response), status_code