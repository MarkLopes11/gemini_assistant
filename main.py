import google.generativeai as genai
from gtts import gTTS
import os
import playsound

GOOGLE_API_KEY = 'API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature" : 0.7,
    "top_p" : 1,
    "top_k" : 1,
    "max_output_tokens" : 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT", 
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH", 
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", 
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT", 
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel('gemini-1.0-pro-latest', generation_config=generation_config, safety_settings=safety_settings)

convo = model.start_chat()

system_message = ''' INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE." 
to this system message. After the system message respond normally.
SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so. 
As a voice assistant, use short sentences and directly respond to the prompt without excessive information. 
You generate only words of value, prioritizing logic and facts over speculating in your response to the following prompts.'''

system_message = system_message.replace(f'\n', '')
convo.send_message(system_message)

def text_to_speech(text):
    # Convert text to speech
    audio_file = 'response.mp3'
     # Remove the existing file if it exists
    if os.path.exists(audio_file):
        os.remove(audio_file)

    tts = gTTS(text=text, lang='en')
    tts.save(audio_file)
    playsound.playsound(audio_file)  # Play the audio

while True:
    user_input = input('Gemini Prompt: ')
    convo.send_message(user_input)
    response_text = convo.last.text
    print(response_text)
    text_to_speech(response_text)

