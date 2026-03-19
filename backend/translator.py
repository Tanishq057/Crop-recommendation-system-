from googletrans import Translator

class LanguageTranslator:
    def __init__(self):
        self.translator = Translator()
        self.indian_languages = {
            'hindi': 'hi', 'bengali': 'bn', 'telugu': 'te', 'marathi': 'mr',
            'tamil': 'ta', 'urdu': 'ur', 'gujarati': 'gu', 'kannada': 'kn',
            'malayalam': 'ml', 'punjabi': 'pa'
        }
        
    def detect_language(self, text):
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except Exception as e:
            print(f"Error detecting language: {e}")
            return 'en'
    
    def translate_to_english(self, text, source_language=None):
        try:
            if not source_language:
                source_language = self.detect_language(text)
            
            if source_language == 'en':
                return text
            
            translation = self.translator.translate(text, src=source_language, dest='en')
            return translation.text
        except Exception as e:
            print(f"Error translating to English: {e}")
            return text
    
    def translate_from_english(self, text, target_language):
        try:
            if target_language == 'en':
                return text
            
            translation = self.translator.translate(text, src='en', dest=target_language)
            return translation.text
        except Exception as e:
            print(f"Error translating from English: {e}")
            return text
