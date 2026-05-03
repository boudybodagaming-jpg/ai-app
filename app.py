from openai import OpenAI
import streamlit as st
from gtts import gTTS
import requests
import time
import os

# 🔑 المفاتيح
OPENAI_API_KEY = os.getenv("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")
DID_API_KEY = os.getenv("YWlwNTg4Njg2QGdtYWlsLmNvbQ:-E5QbR-bchTR_9lf8vez8")

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="AI Teacher", layout="centered")

st.title("👩‍🏫 Smart AI Teacher")

question = st.text_input("Ask your question:")

if st.button("Ask"):

    if question:

        # 🧪 Animation loading
        loading = st.empty()

        loading.markdown("""
        <div style="text-align:center; padding:30px;">
            <div style="
                width:120px;
                height:120px;
                border:5px solid #00c6ff;
                border-radius:50%;
                margin:auto;
                position:relative;
                animation:spin 3s linear infinite;
            ">
                <div style="
                    position:absolute;
                    bottom:10px;
                    left:25px;
                    width:60px;
                    height:60px;
                    background:linear-gradient(#00c6ff,#0072ff);
                    border-radius:0 0 30px 30px;
                    animation:boil 1s infinite alternate;
                "></div>
            </div>

            <h3 style="margin-top:20px;">🧪 Cooking your answer...</h3>
        </div>

        <style>
        @keyframes spin {
            0% {transform:rotate(0deg);}
            100% {transform:rotate(360deg);}
        }

        @keyframes boil {
            0% {height:40px;}
            100% {height:70px;}
        }
        </style>
        """, unsafe_allow_html=True)

        # 🤖 AI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Explain simply in Arabic and English."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content

        # 🔊 صوت
        tts = gTTS(text=answer, lang="en")
        tts.save("voice.mp3")

        # 🎥 D-ID
        url = "https://api.d-id.com/talks"

        headers = {
            "Authorization": f"Basic {DID_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "source_url": "https://create-images-results.d-id.com/DefaultPresenters/Noelle_f/v1_image.jpeg",
            "script": {
                "type": "text",
                "input": answer
            }
        }

        res = requests.post(url, json=data, headers=headers)

        video_url = None

        if res.status_code == 201:
            talk_id = res.json()["id"]

            while True:
                video_res = requests.get(
                    f"https://api.d-id.com/talks/{talk_id}",
                    headers=headers
                )

                result = video_res.json()
                if result.get("status") == "done":
                    video_url = result.get("result_url")
                    break

                time.sleep(3)

        # ❌ شيل الانيميشن
        loading.empty()

        # 💥 عرض كله مرة واحدة
        st.write(answer)
        st.audio("voice.mp3")

        if video_url:
            st.video(video_url)
        else:
            st.error("Video failed ❌")