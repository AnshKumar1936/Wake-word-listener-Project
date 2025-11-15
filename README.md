# Wake Word Listener - "Clarity" Detection

A simple Python script that listens for the wake word "Clarity" and speaks a greeting when detected.

## What It Does

- Listens continuously for the word **"Clarity"** (case-insensitive)
- When detected, speaks a random greeting: "How can I help you?" or "Hi buddy"
- Runs locally, no cloud APIs required

## Requirements

- Python 3.7+
- Microphone


## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python wake_word_listener.py
```

**What happens:**
1. Script calibrates microphone (~2 seconds)
2. Starts listening for "Clarity"
3. When you say "Clarity", it speaks a greeting
4. Press `Ctrl+C` to stop

**Output:** All output appears in your terminal window. You'll also hear the greeting through your speakers.

## Configuration

Edit `wake_word_listener.py` to change:

```python
listener = WakeWordListener(
    wake_word="clarity",        
    energy_threshold=4000       
)
```

## Troubleshooting

**"No module named 'pyaudio'"**
- Windows: `pip install pipwin && pipwin install pyaudio`
- Linux: Install system dependencies first (see Requirements)

**"Could not find a microphone"**
- Check microphone is connected and enabled
- Windows: Settings > Privacy > Microphone > Allow apps access

**Wake word not detected**
- Speak clearly and ensure "Clarity" is in your phrase
- Try saying "Hey Clarity" or "Hello Clarity"
- Lower `energy_threshold` if your voice is quiet

## Project Structure

```
├── wake_word_listener.py    # Main script
├── requirements.txt          # Dependencies
└── README.md                # This file
```

## License

Provided as-is for educational purposes.
