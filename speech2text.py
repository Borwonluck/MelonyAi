import torch
import sounddevice as sd
from transformers import pipeline
from scipy.io.wavfile import write
import numpy as np
import time
import keyboard
import os


# -----------------------------
# โหลดโมเดล Thonburian Whisper
# -----------------------------
MODEL_NAME = "biodatlab/whisper-th-small-combined"
lang = "th"
device = 0 if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

# -----------------------------
# ฟังก์ชันบันทึกเสียง (กด Enter เพื่อเริ่มและหยุด)
# -----------------------------
def record_audio_enter(filename="recorded.wav", samplerate=16000):
    input()
    print("🟢 กำลังบันทึก... กด Enter อีกครั้งเพื่อหยุดเมี๊ยว~")

    frames = []
    stream = sd.InputStream(samplerate=samplerate, channels=1)
    stream.start()

    try:
        while True:
            if keyboard.is_pressed('enter'):
                break
            data, _ = stream.read(1024)
            frames.append(data)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n⛔️ หยุดการบันทึกด้วยคีย์บอร์ด")
        stream.stop()
        stream.close()
        if os.path.exists(filename):
            os.remove(filename)
        return

    stream.stop()
    stream.close()

    if frames:
        audio_data = np.concatenate(frames, axis=0)
        write(filename, samplerate, audio_data)
        print("✅ บันทึกเสียงเสร็จแล้วเมี๊ยว~")
    else:
        print("⚠️ ไม่มีเสียงที่ถูกบันทึกเลยเมี๊ยว~")

# -----------------------------
# ฟังก์ชันแปลงเสียงเป็นข้อความ
# -----------------------------
def recognize_speech(audio_path="recorded.wav"):
    try:
        result = pipe(
            audio_path,
            generate_kwargs={"language": "<|th|>", "task": "transcribe"},
            batch_size=16
        )
        return result["text"]
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดขณะถอดเสียง: {e}")
        return None

# -----------------------------
# ฟังก์ชันหลักที่วนลูปรอการพูดคุย
# -----------------------------
# def start_voice_loop():
#     print("💬 เมโลนี่พร้อมคุยและพูดผ่าน VAC แล้วน้า~ เมี๊ยว~ 🎤🐱")

#     # ค้นหา Virtual Audio Cable
#     device_index = get_audio_device()
#     if device_index is None:
#         print("❌ ไม่พบ Virtual Audio Cable นะเมี๊ยว~ หยุดก่อนดีกว่า")
#         return

#     while True:
#         try:
#             record_audio_enter()

#             # แปลงเสียงเป็นข้อความ
#             user_input = recognize_speech()
#             if not user_input:
#                 print("❌ เมโลนี่ฟังไม่เข้าใจเลยเมี๊ยว~ ลองใหม่อีกครั้งได้นะ~")
#                 continue

#             if user_input.strip().lower() in ["exit", "quit", "e"]:
#                 print("👋 แล้วเจอกันใหม่นะเมี๊ยว~")
#                 break

#             print(f"👦 Won: {user_input}")

#             # ใช้ ChatGPT ตอบกลับ
#             reply = get_response(user_input)
#             print(f"🐱 Melony: {reply}")

#             # พูดออกเสียง
#             speak(reply, device_index=device_index)

#         except KeyboardInterrupt:
#             print("\n⛔️ หยุดการสนทนาด้วยคีย์บอร์ด เมี๊ยว~")
#             if os.path.exists("recorded.wav"):
#                 os.remove("recorded.wav")
#             break


