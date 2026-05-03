from openai import OpenAI
import streamlit as st
from gtts import gTTS
import requests
import time

# 🔑 حط المفاتيح هنا
OPENAI_API_KEY = "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"
DID_API_KEY = "Ym91ZHlhYm9kYUBnbWFpbC5jb20:BjnbCG9gZoatiswpzsI_C"

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="AI Teacher", layout="centered")

st.title("👩‍🏫 Smart AI Teacher")

question = st.text_input("Ask your question:")

if st.button("Ask"):

    if question:

        # 🤖 AI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Explain in a very simple and short way in Arabic and English."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        answer = response.choices[0].message.content

        # 🌍 اللغة
        if any(word in question.lower() for word in ["what", "how", "why"]):
            lang = "en"
        else:
            lang = "ar"

        # 🔊 الصوت
        tts = gTTS(text=answer, lang=lang)
        tts.save("voice.mp3")

        # 🎥 D-ID
        url = "https://api.d-id.com/talks"

        headers = {
            "Authorization": f"Basic {DID_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "source_url": "https://i.ibb.co/VW8PTSMd/Whats-App-Image-2026-04-08-at-11-13-16-PM.jpg",
            "script": {
                "type": "text",
                "input": answer
            }
        }

        res = requests.post(url, json=data, headers=headers)

        if res.status_code == 201:
            talk_id = res.json()["id"]

            st.info("Generating video... ⏳")

            time.sleep(30)

            video_res = requests.get(
                f"https://api.d-id.com/talks/{talk_id}",
                headers=headers
            )

            video_url = video_res.json().get("result_url")

            # 🎥 فيديو فوق + Auto
            if video_url:
                st.markdown(f"""
<video width="100%" autoplay>
    <source src="{video_url}" type="video/mp4">
</video>
""", unsafe_allow_html=True)

                st.caption(answer)
                st.audio("voice.mp3")

            else:
                st.error("Video not ready ❌")