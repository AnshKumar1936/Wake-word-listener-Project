import speech_recognition as sr
import pyttsx3
import random


class WakeWordListener:
    """Listens for wake word and executes action."""
    
    def __init__(self, wake_word="clarity", energy_threshold=4000):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize TTS
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 150)
            self.tts.setProperty('volume', 0.9)
        except:
            self.tts = None
    
    def setup_microphone(self):
        """Initialize and calibrate microphone."""
        try:
            self.microphone = sr.Microphone()
            print("Calibrating microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Microphone ready!\n")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def listen_for_wake_word(self):
        """Listen and detect wake word."""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
            
            try:
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                return self.wake_word in text
            except sr.UnknownValueError:
                return False
            except sr.RequestError as e:
                print(f"Recognition error: {e}")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def speak_greeting(self):
        """Speak a random greeting."""
        greeting = random.choice(["How can I help you?", "Hi buddy"])
        print(f"Speaking: {greeting}")
        
        if self.tts:
            try:
                self.tts.say(greeting)
                self.tts.runAndWait()
                print("✓ Greeting spoken")
            except:
                print(f"TTS error. Message: {greeting}")
        else:
            print(f"TTS unavailable. Message: {greeting}")
    
    def run(self):
        """Main loop."""
        print("="*50)
        print(f"Wake Word Listener - Listening for '{self.wake_word.upper()}'")
        print("Press Ctrl+C to stop")
        print("="*50 + "\n")
        
        if not self.setup_microphone():
            return
        
        try:
            while True:
                if self.listen_for_wake_word():
                    print("\n" + "="*50)
                    print("Wake word detected. Executing action...")
                    print("="*50 + "\n")
                    self.speak_greeting()
                    print("\n" + "="*50)
                    print("Action completed. Listening again...")
                    print("="*50 + "\n")
        except KeyboardInterrupt:
            print("\n\nShutting down...")


def main():
    """Entry point."""
    listener = WakeWordListener(
        wake_word="clarity",
        energy_threshold=4000
    )
    listener.run()


if __name__ == "__main__":
    main()
