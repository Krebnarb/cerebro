import whisper

model = whisper.load_model("base")
result = model.transcribe("recording.mp3")
print(result["text"])