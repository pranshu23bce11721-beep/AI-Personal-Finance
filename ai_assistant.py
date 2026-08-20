import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
# You must have GOOGLE_API_KEY set in your environment variables or .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_assistant(question: str, context_data: str) -> str:
    """
    Sends a question and context data to the Gemini model to act as a financial advisor.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an AI Personal Finance Assistant. 
        Here is the user's current financial data (expenses):
        {context_data}
        
        Answer the user's question clearly and concisely based ONLY on this data.
        If the question cannot be answered with the data, politely say so.
        
        User's question: {question}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI Assistant: {str(e)}"

def extract_receipt_data(image_file) -> dict:
    """
    Uses Gemini Vision capabilities to extract total amount and description from a receipt image.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Analyze this receipt image. Extract the following information and return ONLY a valid JSON object:
        {
            "amount": <float, total amount on receipt>,
            "description": "<string, name of the store or main item>"
        }
        Do not include markdown blocks or any other text.
        """
        
        # Read file content depending on how streamlit passes it
        image_data = [{"mime_type": "image/jpeg", "data": image_file.getvalue()}]
        
        response = model.generate_content([prompt, image_data[0]])
        
        # Simple cleanup to parse JSON if model returned markdown
        text = response.text.replace('```json', '').replace('```', '').strip()
        import json
        return json.loads(text)
    except Exception as e:
        return {"error": str(e)}
