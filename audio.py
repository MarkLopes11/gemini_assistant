import speech_recognition as sr

def record_text_from_wav(wav_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_file_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            print("Processing the audio file...")

            # Listen to the audio file
            audio = recognizer.record(source)

            # Try to recognize the speech in the audio file
            try:
                Mytext = recognizer.recognize_google(audio)
                print(f"Extracted text: {Mytext}")
                return Mytext
            except sr.UnknownValueError:
                print("Couldn't understand the audio. Please try again.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
    except FileNotFoundError:
        print("Audio file not found. Please check the path.")
    return ""

# Example usage
wav_file_path = "output.wav"
record_text_from_wav(wav_file_path)
