# Clarity Listener

Simple, single-threaded wake-word demo for experimenting with “Clarity” phrases. This is a learning/testing tool only—it blocks while speaking, relies on Google’s API, and is not suitable for production wake-word use.

## Version Overview

**v0.1 (Classic “Hey Clarity”)**
- Single hard-coded wake word and two canned greetings.
- Configuration required editing `wake_word_listener.py`.
- Basic loop with minimal error handling.

**v0.2 (Config-Driven Upgrade)**
- Loads wake phrases, keyword, responses, and audio settings from `config.json`.
- Adds keyword-based matching, friendlier mic/API errors, and graceful Ctrl+C shutdown.
- Uses a `main()` entry point so the module can be imported safely.

## Changes v0.1 → v0.2

- Config moved into `config.json` (wake phrases, responses, mic/audio tuning).
- Added keyword matching, clearer mic/API errors, and clean Ctrl+C exit.
- Script now wraps logic in `main()` so it can be imported without auto-running.

## Requirements

- Python 3.8+
- Microphone with working drivers
- Internet access (Google Speech Recognition)

## Install & Run

```bash
pip install -r requirements.txt
python wake_word_listener.py
```

## Configuration (`config.json`)

```json
{
  "keyword": "clarity",
  "wake_phrases": ["hey clarity", "hello clarity"],
  "responses": ["Hi there!", "How can I help?"],
  "settings": {
    "input_device_index": null,
    "language_code": "en-US",
    "energy_threshold": 4000,
    "phrase_time_limit": 5,
    "ambient_duration": 2,
    "enable_tts": true,
    "tts_rate": 150,
    "tts_volume": 0.9
  }
}
```

- `keyword`: Base word that should fire even inside longer sentences (e.g., “tell me the date clarity”).
- `wake_phrases`: Any phrases that should trigger the listener (case-insensitive).
- `responses`: Possible TTS replies—one is chosen randomly per trigger.
- `input_device_index`: Set to the microphone index from `sr.Microphone.list_microphone_names()`. Leave `null` for default.
- `language_code`: Passed to Google Speech Recognition (e.g., `en-US`, `es-ES`).
- `energy_threshold`: Tune sensitivity. Lower → more sensitive.
- `phrase_time_limit`: Max seconds to capture each utterance.
- `ambient_duration`: Seconds spent sampling ambient noise for calibration.
- `enable_tts`: `false` turns off spoken playback but still logs responses.
- `tts_rate` / `tts_volume`: Controls pyttsx3 speaking style.
- Logs show detected transcription, wake events, and generated responses for debugging.

Restart the script after editing the config.

## Limitations

- Tested on Windows 11 with Python 3.11 and the default system microphone.
- Uses Google’s free Speech Recognition endpoint; offline recognition isn’t included.
- No background hotword detection thread—main loop is blocking.

## Future Improvements

- Multi-threaded listening so TTS doesn’t pause detection.
- Dedicated wake-word/VAD engine instead of full transcription.
- Integrated voice activity detection for better timing and power use.

