from flask import Flask, request, jsonify
from chatbot import AgriculturalChatbot
import os
import pickle

   
app = Flask(__name__)
chatbot = AgriculturalChatbot()

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
crop_model_path = os.path.join(MODEL_DIR, 'crop_recommendation_model.pkl')

try:
    with open(crop_model_path, 'rb') as f:
        crop_model = pickle.load(f)
    print("Crop recommendation model loaded successfully.")
except Exception as e:
    print(f"Error loading crop recommendation model: {e}")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    user_language = data.get('language', None)
    
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    response = chatbot.process_query(user_input, user_language)
    return jsonify({'response': response})

@app.route('/languages', methods=['GET'])
def languages():
    # Return supported Indian languages
    supported_languages = {
        'hindi': 'hi', 'bengali': 'bn', 'telugu': 'te', 'marathi': 'mr',
        'tamil': 'ta', 'urdu': 'ur', 'gujarati': 'gu', 'kannada': 'kn',
        'malayalam': 'ml', 'punjabi': 'pa', 'english': 'en'
    }
    return jsonify(supported_languages)

if __name__ == '__main__':
    app.run(debug=True)
