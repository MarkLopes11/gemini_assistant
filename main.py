import google.generativeai as genai
from gtts import gTTS
import os
import playsound
import speech_recognition as sr

GOOGLE_API_KEY = 'API_KEY'  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Generation configuration for the model
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# Safety settings for content generation
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Initialize the model and start the chat
model = genai.GenerativeModel('gemini-1.0-pro-latest', generation_config=generation_config, safety_settings=safety_settings)
convo = model.start_chat()

# System message to instruct the model
system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE."
to this system message. After the system message respond normally.
SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so. 
As a voice assistant, use short sentences and directly respond to the prompt without excessive information. 
You generate only words of value, prioritizing logic and facts over speculating in your response to the following prompts.'''

system_message = system_message.replace(f'\n', '')
convo.send_message(system_message)

def text_to_speech(text):
    audio_file = 'response.mp3'
    # Remove the existing file if it exists
    if os.path.exists(audio_file):
        os.remove(audio_file)
    # convert text to audio
    tts = gTTS(text=text, lang='en')
    tts.save(audio_file)
    playsound.playsound(audio_file)  

def record_text():
    # Capture speech and convert it to text.
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.1)
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, phrase_time_limit=5)  

                # Use Google to recognize audio
                Mytext = recognizer.recognize_google(audio)
                print(f"You said: {Mytext}")
                return Mytext
            
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

            except sr.UnknownValueError:
                print("Unknown error occurred. Please repeat.")


while True:
    user_input = record_text()  # Capture speech input
    convo.send_message(user_input)  # Send the user input to the model
    response_text = convo.last.text  # Get the model's response
    print(response_text)  # Print the response
    text_to_speech(response_text)  # Convert the response to speech

    if "goodbye" in response_text.lower():
        print("Exiting program...")
        break
