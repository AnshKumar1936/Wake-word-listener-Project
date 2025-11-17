import json
import random
from pathlib import Path
from typing import Any, Dict, List

import pyttsx3
import speech_recognition as sr

CONFIG_PATH = Path(__file__).with_name("config.json")


def load_config(path: Path) -> Dict[str, Any]:
    """Load JSON configuration from disk."""
    try:
        with path.open("r", encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found at {path}.")
    except json.JSONDecodeError as exc:
        print(f"Configuration file is invalid JSON: {exc}")

    return {}


class WakeWordListener:
    """Listens for configured wake phrases and executes an action."""

    def __init__(self, config: Dict[str, Any]):
        settings = config.get("settings", {})

        self.keyword = config.get("keyword", "clarity").lower()
        self.wake_phrases: List[str] = [
            phrase.lower() for phrase in config.get("wake_phrases", ["hey clarity"])
        ]
        self.responses: List[str] = config.get(
            "responses", ["How can I assist you?", "Hi there!"]
        )

        self.input_device_index = settings.get("input_device_index")
        self.language_code = settings.get("language_code", "en-US")
        self.energy_threshold = settings.get("energy_threshold", 4000)
        self.phrase_time_limit = settings.get("phrase_time_limit", 5)
        self.ambient_duration = settings.get("ambient_duration", 2)

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.dynamic_energy_threshold = True

        # Initialize TTS
        self.tts = None
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty("rate", settings.get("tts_rate", 150))
            self.tts.setProperty("volume", settings.get("tts_volume", 0.9))
        except Exception as exc:
            print(f"TTS initialization failed: {exc}")

    def setup_microphone(self) -> bool:
        """Initialize and calibrate microphone."""
        try:
            self.microphone = sr.Microphone(device_index=self.input_device_index)
        except OSError as exc:
            print(f"Microphone unavailable: {exc}")
            print("Verify your input device index in config.json.")
            return False
        except Exception as exc:
            print(f"Unexpected microphone error: {exc}")
            return False

        print("Calibrating microphone...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=self.ambient_duration
                )
        except Exception as exc:
            print(f"Calibration failed: {exc}")
            return False

        print("Microphone ready!\n")
        return True

    def listen_for_wake_word(self) -> bool:
        """Listen and detect configured wake phrases."""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, timeout=None, phrase_time_limit=self.phrase_time_limit
                )
        except Exception as exc:
            print(f"Listening error: {exc}")
            return False

        try:
            text = self.recognizer.recognize_google(audio, language=self.language_code)
            text = text.lower()
            print(f"Heard: {text}")
            if any(phrase in text for phrase in self.wake_phrases):
                return True
            if self.keyword and self.keyword in text:
                return True
            return False
        except sr.UnknownValueError:
            return False
        except sr.RequestError as exc:
            print(f"Recognition error (network/API): {exc}")
        except Exception as exc:
            print(f"Recognition failed: {exc}")

        return False

    def speak_greeting(self):
        """Speak a random greeting."""
        greeting = random.choice(self.responses)
        print(f"Speaking: {greeting}")

        if not self.tts:
            print(f"TTS unavailable. Message: {greeting}")
            return

        try:
            self.tts.say(greeting)
            self.tts.runAndWait()
            print("✓ Greeting spoken")
        except Exception as exc:
            print(f"TTS error: {exc}. Message: {greeting}")

    def run(self):
        """Main loop."""
        print("=" * 50)
        print("Clarity Listener v0.2")
        print(f"Listening for: {', '.join(self.wake_phrases)}")
        print("Press Ctrl+C to stop")
        print("=" * 50 + "\n")

        if not self.setup_microphone():
            return

        try:
            while True:
                if self.listen_for_wake_word():
                    print("\n" + "=" * 50)
                    print("Wake phrase detected. Executing action...")
                    print("=" * 50 + "\n")
                    self.speak_greeting()
                    print("\n" + "=" * 50)
                    print("Action completed. Listening again...")
                    print("=" * 50 + "\n")
        except KeyboardInterrupt:
            print("\nShutting down Clarity Listener...")
        except Exception as exc:
            print(f"\nListener stopped due to error: {exc}")


def main():
    """Entry point."""
    config = load_config(CONFIG_PATH)
    if not config:
        print("Unable to start without a valid configuration file.")
        return

    listener = WakeWordListener(config)
    listener.run()


if __name__ == "__main__":
    main()
