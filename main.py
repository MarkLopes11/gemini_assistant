import google.generativeai as genai
from gtts import gTTS
import os
import playsound
import speech_recognition as sr
import keyboard 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Fetch the API key from the .env file
genai.configure(api_key=GOOGLE_API_KEY)  # Configure the Google API with the loaded key

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
model = genai.GenerativeModel('gemini-pro', generation_config=generation_config, safety_settings=safety_settings)
convo = model.start_chat()

# System message to instruct the model
system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE."
to this system message. After the system message respond normally.
SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so. 
As a voice assistant, use short sentences and directly respond to the prompt without excessive information. 
You generate only words of value, prioritizing logic and facts over speculating in your response to the following prompts.'''

system_message = system_message.replace('\n', '')
convo.send_message(system_message)

# Function to convert the entire response text to speech and play it
def text_to_speech(response_text):
    tts = gTTS(text=response_text, lang='en')
    audio_file = 'response.mp3'
    if os.path.exists(audio_file):
        os.remove(audio_file)  # Remove the file if it already exists
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)  # Remove the file after playing

# Function to record speech and convert it to text
def record_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.1)
        print("Listening... Hold spacebar to speak.")

        # Keep recording as long as the spacebar is pressed
        while keyboard.is_pressed('space'):
            audio = recognizer.listen(source)
            try:
                Mytext = recognizer.recognize_google(audio)
                print(f"You said: {Mytext}")
                return Mytext
            except sr.UnknownValueError:
                print("Couldn't understand the audio. Please try again.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        return ""  # Return empty string if nothing is recognized

# Function to process user input and send it to the model
def process_input():
    user_input = record_text()  # Capture speech input
    if user_input:
        convo.send_message(user_input)  # Send the user input to the model
        response_text = convo.last.text  # Get the model's response
        print(response_text)  # Print the response
        
        text_to_speech(response_text) # Pass the text to the text_to_speech function

        if "goodbye" in response_text.lower():
            print("Exiting program...")
            return False  
    return True  

def main():
    print("Hold the spacebar to speak...")
    while True:
        keyboard.wait('space')  # Wait for the spacebar to be pressed
        
        # Process the input when spacebar is pressed and released
        if not process_input():
            break  # Exit the loop if "goodbye" is detected

if __name__ == "__main__":
    main()
