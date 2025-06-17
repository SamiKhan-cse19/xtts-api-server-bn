import asyncio
import websockets
import json

async def stream_xtts_ws(ws_url: str, text: str, speaker_wav: str, language: str):
    """
    Streams audio from an XTTS WebSocket server and saves it to a file.

    Args:
        ws_url (str): WebSocket URL, e.g., 'ws://localhost:8020/ws_tts'.
        text (str): Text to synthesize.
        speaker_wav (str): Path to speaker WAV file on server.
        language (str): Language code (e.g., 'en', 'bn').
    """
    try:
        async with websockets.connect(ws_url, max_size=None) as websocket:
            # Send configuration
            config = {
                "text": text,
                "language": language
            }
            await websocket.send(json.dumps(config))
            print("Sent synthesis config. Waiting for audio stream...")

            with open("output_audio.wav", "wb") as audio_file:
                while True:
                    try:
                        message = await websocket.recv()
                        if isinstance(message, bytes):
                            print(f"Received chunk of size: {len(message)} bytes")
                            audio_file.write(message)
                        elif isinstance(message, str):
                            if message == "[DONE]":
                                print("Streaming complete.")
                                break
                            else:
                                print(f"Received text message: {message}")
                    except websockets.exceptions.ConnectionClosedOK:
                        print("Connection closed normally.")
                        break

            print("Audio saved to 'output_audio.wav'.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ws_url = "ws://localhost:8020/tts_stream_ws"
    text = "এ তালিকায় আছেন আফগানিস্তানের তারকা ক্রিকেটার রশিদ খানও। আইপিএলের একাধিক ফ্র্যাঞ্চাইজিও ভুক্তভোগী ও তাঁদের পরিবারের প্রতি সমবেদনা জানিয়েছে। এ ছাড়া বিশ্ব চ্যাম্পিয়নশিপে সোনাজয়ী সাবেক কুস্তিগির ভিনেশ ফোগাট, মেয়েদের ব্যাডমিন্টনের অন্যতম শীর্ষ তারকা পিভি সিন্ধুও দুঃখ প্রকাশ করেছেন।"
    speaker_wav = "/home/samikhan/repos/xtts-api-server/example/male.wav"
    language = "bn"

    asyncio.run(stream_xtts_ws(ws_url, text, speaker_wav, language))
