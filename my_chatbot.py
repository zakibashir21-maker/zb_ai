#my_chatbot.py
import os
import tempfile
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
from openai import OpenAI

# Load API key from credentials file
CREDENTIALS_FILE = "credentials.txt"

if not os.path.exists(CREDENTIALS_FILE):
    raise FileNotFoundError(f"Credentials file '{CREDENTIALS_FILE}' not found.")

with open(CREDENTIALS_FILE, "r") as f:
    api_key = f.read().strip()
client = OpenAI(api_key=api_key)


def record_until_enter(samplerate=16000, channels=1):
    frames = []

    def callback(indata, frames_count, time_info, status):
        frames.append(indata.copy())

    stream = sd.InputStream(samplerate=samplerate, channels=channels, callback=callback)
    stream.start()
    try:
        input("Recording... press Enter to stop.")
    finally:
        stream.stop()
        stream.close()

    if not frames:
        return None
    # Save recorded data to a temporary WAV file
    data = np.concatenate(frames, axis=0)
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, data, samplerate)
    return tmp.name


end_program = False
# Ask for an adjective and incorporate it into the system prompt
adjective = input("Enter an adjective to describe the chatbot's personality (e.g., sarcastic, witty, happy): ").strip()
while not end_program:
    cmd = input("Press Enter to record your prompt (or type 'exit' to quit): ")
    if cmd.lower() in ("goodbye", "exit"):
        end_program = True
        print("You have exited the chat. Goodbye!")
        break

    # Start recording until user presses Enter
    audio_path = record_until_enter()
    if not audio_path:
        print("No audio captured. Try again.")
        continue
    #Transcribe audio using OpenAI's Whisper model    
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    try:
        get_input = transcript.text
    except Exception:
        print("Failed to transcribe audio.")
        os.remove(audio_path)
        continue

    print("You said:", get_input)
    os.remove(audio_path)

    messages = [
        {"role": "system", "content": "You are " + adjective},
        {"role": "user", "content": get_input}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    assistant_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_response})
    print("Assistant: " + assistant_response)