import whisper

model = whisper.load_model("tiny")
result = model.transcribe("tee.m4a", fp16=False)

print(result["text"])