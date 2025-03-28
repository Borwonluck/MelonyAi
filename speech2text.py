import time
import torch
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from transformers import pipeline
from playsound import playsound
import speech_recognition as sr

# โหลดโมเดล Thonburian Whisper
MODEL_NAME = "biodatlab/whisper-th-small-combined"
lang = "th"
device = 0 if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

WAKE_WORDS = ["เมล", "Mel", "เมโลนี่", "Melony", "เมโรนี่", "เมโรนี", "เมโลนี", "Merony", "เมโรนี่้", "เมโรนี้", "เมโลนี้", "เม", "เมว", "mail"]

# ฟังก์ชันเล่นเสียงแจ้งเตือน=
def play_beep(file_path):
    try:
        playsound(file_path)
    except Exception as e:
        print(f"⚠️ ไม่สามารถเล่นเสียง {file_path}: {e}")

# ตรวจจับคำว่า "เมล" ก่อนถึงจะเริ่มฟัง
def detect_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🕵️ รอฟังคำเรียก... (พูดว่า 'เมล' หรือ 'Mel')")

        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=3)
                text = recognizer.recognize_google(audio, language="th-TH").lower()
                for word in WAKE_WORDS:
                    if word.lower() in text:
                        print("🐱 ได้ยินชื่อเมลแล้ว! เริ่มฟังเสียงถัดไปเมี๊ยว~")
                        return
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาดในการตรวจจับ: {e}")
                continue

# ฟังก์ชันบันทึกเสียงพร้อมตรวจจับความเงียบ
def record_audio_auto(filename="recorded.wav", samplerate=16000, silence_threshold=0.05, silence_duration=1.5):
    duration_limit = 30
    frame_duration = 0.1  # วัดทีละ 100ms
    max_silent_chunks = int(silence_duration / frame_duration)

    sd.default.samplerate = samplerate
    sd.default.channels = 1

    frames = []
    silent_chunks = 0
    recording_started = False

    play_beep("assets/beep_sound/start_beep.wav")
    print("🔴 กำลังรอฟังเสียง... (เริ่มพูดเมื่อไหร่เมโลนี่จะเริ่มบันทึกให้นะ~)")

    with sd.InputStream() as stream:
        start_time = time.time()

        while True:
            frame, _ = stream.read(int(samplerate * frame_duration))
            volume = np.linalg.norm(frame)

            if volume > silence_threshold:
                if not recording_started:
                    print("🟢 เริ่มบันทึกเสียงแล้ว~ เมี๊ยว~")
                    recording_started = True

                frames.append(frame)
                silent_chunks = 0
            else:
                if recording_started:
                    silent_chunks += 1
                    if silent_chunks > max_silent_chunks:
                        print("🔕 ตรวจพบความเงียบ~ หยุดบันทึกแล้วเมี๊ยว~")
                        break

            if time.time() - start_time > duration_limit:
                print("⏰ หมดเวลาการบันทึก~ เมี๊ยว~")
                break

    if frames:
        audio_data = np.concatenate(frames, axis=0)
        write(filename, samplerate, audio_data)
        play_beep("assets/beep_sound/end_beep.wav")
        print("✅ บันทึกไฟล์เรียบร้อยแล้วเมี๊ยว~")
    else:
        print("❌ ไม่มีเสียงที่บันทึกได้เลยนะเมี๊ยว~")

# ฟังก์ชันแปลงเสียงเป็นข้อความ
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

# ทดสอบแบบ standalone
if __name__ == "__main__":
    detect_wake_word()
    record_audio_auto()
    text = recognize_speech()
    print(f"📝 ข้อความที่ได้: {text}")
