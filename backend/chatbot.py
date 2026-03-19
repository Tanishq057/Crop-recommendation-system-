import pickle
import numpy as np
from translator import LanguageTranslator
from intent_extractor import IntentExtractor

class AgriculturalChatbot:
    def __init__(self):
        self.translator = LanguageTranslator()
        self.intent_extractor = IntentExtractor()
        
        try:
            with open('../models/crop_recommendation_model.pkl', 'rb') as file:
                self.crop_model = pickle.load(file)
            
            with open('../models/roi_prediction_model.pkl', 'rb') as file:
                self.roi_model = pickle.load(file)
                
            self.models_loaded = True
        except Exception as e:
            print(f"Error loading models: {e}")
            self.models_loaded = False
    
    def process_query(self, user_input, user_language=None):
        if not user_language:
            user_language = self.translator.detect_language(user_input)
        
        if user_language != 'en':
            english_input = self.translator.translate_to_english(user_input, user_language)
        else:
            english_input = user_input
        
        params = self.intent_extractor.extract_all_parameters(english_input)
        
        missing_params = [k for k, v in params.items() if v is None]
        
        if missing_params:
            response = "Please provide the following information to get accurate recommendations: " + ", ".join(missing_params)
            if user_language != 'en':
                response = self.translator.translate_from_english(response, user_language)
            return response
        
        if self.models_loaded:
            try:
                n, p, k = 50, 50, 50
                humidity = 50
                ph = 7.0
                rainfall = 200
                temp = self.get_temperature_for_month(params['month'], params['location'])
                
                crop_input = np.array([[n, p, k, temp, humidity, ph, rainfall]])
                recommended_crop = self.crop_model.predict(crop_input)[0]
                
                # Prepare ROI prediction input - this depends on how you encoded data during training
                # You must encode crop, location, month accordingly; here just dummy encoding as example:
                crop_encoded = self.encode_crop(recommended_crop)
                location_encoded = self.encode_location(params['location'])
                month_encoded = self.encode_month(params['month'])
                
                roi_input = np.array([[crop_encoded, params['area'], location_encoded, params['investment'], month_encoded]])
                roi = self.roi_model.predict(roi_input)[0]
                
                response = f"Recommended crop: {recommended_crop}. Estimated ROI: {roi:.2f}%."
                
                if user_language != 'en':
                    response = self.translator.translate_from_english(response, user_language)
                
                return response
            except Exception as e:
                print(f"Error during prediction: {e}")
                response = "Sorry, I am unable to process your request at the moment."
                if user_language != 'en':
                    response = self.translator.translate_from_english(response, user_language)
                return response
        else:
            response = "Models are not loaded properly."
            if user_language != 'en':
                response = self.translator.translate_from_english(response, user_language)
            return response
    
    def get_temperature_for_month(self, month, location):
        # Placeholder: you can connect to weather API or define static mapping
        temp_map = {
            'january': 15, 'february': 18, 'march': 25, 'april': 30, 'may': 35,
            'june': 32, 'july': 28, 'august': 28, 'september': 27, 'october': 25,
            'november': 20, 'december': 15
        }
        return temp_map.get(month.lower(), 25)
    
    def encode_crop(self, crop_name):
        # Placeholder: implement based on your training label encoding
        mapping = {'rice': 0, 'wheat': 1, 'maize': 2, 'cotton': 3, 'groundnut': 4}
        return mapping.get(crop_name.lower(), 0)
    
    def encode_location(self, location):
        # Placeholder: implement based on your training label encoding
        mapping = {
            'andhra': 0, 'telangana': 1, 'karnataka': 2, 'tamil nadu': 3,
            'kerala': 4, 'maharashtra': 5, 'punjab': 6, 'haryana': 7,
            'uttar pradesh': 8, 'madhya pradesh': 9, 'gujarat': 10
        }
        return mapping.get(location.lower(), 0)
    
    def encode_month(self, month):
        mapping = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        return mapping.get(month.lower(), 1)
