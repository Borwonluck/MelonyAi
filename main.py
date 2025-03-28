from speech2text import record_audio_auto, recognize_speech, detect_wake_word
from chatbot import get_response
from text2speech import speak, get_audio_device

import os


print("💬 เมโลนี่พร้อมคุยและพูดผ่าน VAC แล้วน้า~ เมี๊ยว~ 🎤🐱")
print("💬 กด Enter เพื่อพูดไ้ด้เลยนะคะ~ 🎤🐱")

# 🔍 ค้นหา Device Index ของ Virtual Audio Cable
device_index = get_audio_device()
if device_index is None:
    print("❌ ไม่พบ Virtual Audio Cable นะเมี๊ยว~ หยุดก่อนดีกว่า")
    exit()

# 🔁 วนลูปรอรับคำพูดจากวอน
while True:
    try :
        # 🎤 ตรวจจับคำว่า "เมโลนี่"
        detect_wake_word()
        # 🔴 บันทึกเสียงจากไมโครโฟน
        record_audio_auto()

        # 📝 ถอดเสียงเป็นข้อความ
        user_input = recognize_speech()
        if not user_input:
            print("❌ เมโลนี่ฟังไม่เข้าใจเลยเมี๊ยว~ ลองใหม่อีกครั้งได้นะ~")
            continue

        if user_input in ["บ๊ายบาย", "ไปก่อนนะ"]:
            print("👋 แล้วเจอกันใหม่นะเมี๊ยว~")
            speak("แล้วเจอกันใหม่นะเมี๊ยว", device_index=device_index)
            if os.path.exists("recorded.wav"):
                os.remove("recorded.wav")
            break

        print(f"👦 Won: {user_input}")

        # 🤖 ส่งข้อความไปให้ ChatGPT
        reply = get_response(user_input)
        print(f"🐱 Melony: {reply}")

        # 🔊 พูดออกผ่าน Virtual Audio Cable
        speak(reply, device_index=device_index)

         # 🧹 ลบไฟล์เสียงที่บันทึกไว้
        if os.path.exists("recorded.wav"):
            os.remove("recorded.wav")

    except KeyboardInterrupt:
            print("\n⛔️ หยุดการสนทนาด้วยคีย์บอร์ด เมี๊ยว~")
            if os.path.exists("recorded.wav"):
                os.remove("recorded.wav")
            break
