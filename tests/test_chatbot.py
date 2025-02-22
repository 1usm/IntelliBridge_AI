import unittest
from app import create_app
from app.models.chatbot import Prompt
from app.extensions import db

class ChatbotTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_prompt_response(self):
        prompt = Prompt(id='test-id', response='test-response')
        db.session.add(prompt)
        db.session.commit()

        response = self.app.test_client().get('/api/prompts/test-id/response')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'test-response'})

if __name__ == '__main__':
    unittest.main()