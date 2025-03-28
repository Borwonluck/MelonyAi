from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
import pyaudio
import os

# 🔍 ค้นหาอุปกรณ์เสียงที่มีชื่อ "CABLE Input"
def get_audio_device():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        name = device_info.get('name')
        max_output_channels = device_info.get('maxOutputChannels')

        if max_output_channels > 0:
            # print(f"Output Device id {i} - {name}")

            if "CABLE Input" in name:
                # print(f"🎯 Found Virtual Audio Cable at index {i}")
                return i

    print("❌ ไม่พบอุปกรณ์ Virtual Audio Cable เมี๊ยว~")
    return None

# 🗣️ พูดข้อความออกลำโพง (หรือส่งเข้า Virtual Audio Cable)
def speak(text, device_index=None, speed=1.25):
    # สร้างเสียง mp3 จาก gTTS
    tts = gTTS(text=text, lang="th")
    mp3_filename = "melony_voice.mp3"
    wav_filename = "melony_voice.wav"
    tts.save(mp3_filename)

    # แปลง mp3 → wav และปรับความเร็ว
    audio = AudioSegment.from_mp3(mp3_filename)
    faster_audio = audio.speedup(playback_speed=speed)
    faster_audio.export(wav_filename, format="wav")

    # เล่นเสียง wav
    data, samplerate = sf.read(wav_filename)
    print(f"🔊 Playing on device index: {device_index}")
    sd.play(data, samplerate=samplerate, device=device_index)
    sd.wait()

    # ลบไฟล์ชั่วคราว
    os.remove(mp3_filename)
    os.remove(wav_filename)

# # 📋 เรียกดู output device ทั้งหมด
# def list_output_devices():
#     print("🎧 Available Output Devices:\n")
#     devices = sd.query_devices()
#     for i, device in enumerate(devices):
#         if device['max_output_channels'] > 0:
#             print(f"{i}: {device['name']}")

# 🧪 ใช้ทดสอบไฟล์นี้เดี่ยว ๆ
# if __name__ == "__main__":
    # list_output_devices()
    # index = get_audio_device()
    # print(f"✅ Device index สำหรับใช้: {index}")
    # speak("เมโลนี่พร้อมแล้วเมี๊ยว~", device_index=index)
