import google.generativeai as genai

genai.configure(api_key="your-google-ai-studio-key")  # Replace with your key
model = genai.GenerativeModel('gemini-pro')

def process_ai(text, mode, user, language):
    try:
        lang_prompt = "in English" if language == "en-US" else "in Hindi"
        prompt = f"Respond as a {'friendly companion' if mode == 'friend' else 'gentle therapist'} for a neurodiverse person, keeping it simple and supportive, {lang_prompt}: '{text}'"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"