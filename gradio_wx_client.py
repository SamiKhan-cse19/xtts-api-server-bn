import asyncio
import websockets
import json
import sounddevice as sd
import numpy as np
import gradio as gr
import soundfile as sf
import io

# Audio format assumptions
SAMPLE_RATE = 22050  # Or use 24000 depending on your model
CHANNELS = 1
DTYPE = 'int16'

async def stream_and_play(ws_url, text, speaker_wav, language):
    config = {
        "text": text,
        "speaker_wav": speaker_wav,
        "language": language
    }

    async with websockets.connect(ws_url, max_size=None) as ws:
        await ws.send(json.dumps(config))

        # Sounddevice stream
        with sd.OutputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=DTYPE) as stream:
            print("Streaming and playing...")
            while True:
                try:
                    msg = await ws.recv()
                    if isinstance(msg, bytes):
                        audio_data, _ = sf.read(io.BytesIO(msg), dtype=DTYPE)
                        stream.write(audio_data)
                    elif msg == "[DONE]":
                        print("Stream complete.")
                        break
                except websockets.exceptions.ConnectionClosed:
                    break

def speak(text, language):
    ws_url = "ws://localhost:8020/tts_stream_ws"
    speaker_wav = "xtts-api-server/example/male.wav"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stream_and_play(ws_url, text, speaker_wav, language))
    return "✅ Streaming complete and played."

# Gradio Interface
iface = gr.Interface(
    fn=speak,
    inputs=[
        gr.Textbox(label="Text"),
        gr.Dropdown(["en", "bn", "es", "fr"], label="Language", value="bn")
    ],
    outputs="text",
    title="Real-time XTTS WebSocket Player"
)

iface.launch()
