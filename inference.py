import httpx
import asyncio

async def stream_xtts(server_url: str, text: str, speaker_wav: str, language: str):
    """
    Streams audio from an XTTS server via GET request and saves it to a file.

    Args:
        server_url (str): The base XTTS server URL, e.g., 'http://localhost:8020/tts_stream'.
        text (str): The text to synthesize.
        speaker_wav (str): Path to the speaker WAV file on the server.
        language (str): Language code (e.g., 'en').
    """
    params = {
        "text": text,
        "speaker_wav": speaker_wav,
        "language": language
    }

    headers = {
        "accept": "application/json"
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("GET", server_url, params=params, headers=headers) as response:
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.reason_phrase}")
                return
            
            print("Streaming audio data from XTTS server...")
            # Save streamed audio to a file
            with open("output_audio.wav", "wb") as audio_file:
                async for chunk in response.aiter_bytes():
                    print(f"Received chunk of size: {len(chunk)} bytes")
                    audio_file.write(chunk)
            print("Audio streaming complete. Saved to 'output_audio.wav'.")

if __name__ == "__main__":
    server_url = "http://localhost:8020/tts_stream"
    text = "যুক্তরাজ্যে বাংলাদেশের সাবেক ভূমিমন্ত্রী সাইফুজ্জামান চৌধুরীর সম্পদ জব্দ করেছে দেশটির ন্যাশনাল ক্রাইম এজেন্সি (এনসিএ)।"
    speaker_wav = "/home/samikhan/repos/xtts-api-server/example/male.wav"
    language = "bn"

    asyncio.run(stream_xtts(server_url, text, speaker_wav, language))
