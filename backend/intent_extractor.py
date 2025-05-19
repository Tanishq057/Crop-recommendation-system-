import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

class IntentExtractor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        self.area_pattern = r'\b(\d+(?:\.\d+)?)\s*(?:acre|hectare|bigha|gunta|cent|sq ft|square feet|square meter)\b'
        self.investment_pattern = r'\b(?:rs|inr|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:rupees|rs|inr|₹)?\b'
        self.month_pattern = r'\b(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec)\b'
        
        self.location_keywords = [
            'andhra', 'telangana', 'karnataka', 'tamil nadu', 'kerala', 'maharashtra', 
            'punjab', 'haryana', 'uttar pradesh', 'madhya pradesh', 'gujarat', 'rajasthan',
            'bihar', 'west bengal', 'assam', 'odisha', 'jharkhand', 'chhattisgarh'
        ]
    
    def preprocess_text(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)
    
    def extract_area(self, text):
        match = re.search(self.area_pattern, text.lower())
        if match:
            return float(match.group(1))
        return None
    
    def extract_investment(self, text):
        match = re.search(self.investment_pattern, text.lower())
        if match:
            amount = match.group(1).replace(',', '')
            return float(amount)
        return None
    
    def extract_month(self, text):
        match = re.search(self.month_pattern, text.lower())
        if match:
            month = match.group(1)
            month_mapping = {
                'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april',
                'jun': 'june', 'jul': 'july', 'aug': 'august', 'sep': 'september',
                'oct': 'october', 'nov': 'november', 'dec': 'december'
            }
            return month_mapping.get(month, month)
        return None
    
    def extract_location(self, text):
        text_lower = text.lower()
        for location in self.location_keywords:
            if location in text_lower:
                return location
        return None
    
    def extract_all_parameters(self, text):
        return {
            'area': self.extract_area(text),
            'investment': self.extract_investment(text),
            'month': self.extract_month(text),
            'location': self.extract_location(text)
        }
