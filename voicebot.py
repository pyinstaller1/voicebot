import openai
import streamlit as st
from audiorecorder import audiorecorder
import os
from datetime import datetime


def STT(audio, apikey):
    filename = "input.mp3"
    audio.export(filename, format="mp3")

    audio_file = open(filename, "rb")
    client = openai.OpenAI(api_key=apikey)
    respons = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    audio_file.close()

    os.remove(filename)
    return respons.text





st.set_page_config(page_title="음성 비서 프로그램", layout="wide")

st.header("음성 비서 프로그램")

st.markdown("---")


with st.expander("음성비서 프로그램에 관하여", expanded=True):
    st.write(
        """
        
        - 음성 비서 프로그램의 UI는 스트림릿을 활용했습니다.
        - STT(Speech-To-Text)는 OpenAI의 Whisper AI를 활용했습니다.
        - 답변은 OpenAI의 GPT 모델을 활용했습니다.
        - TTS는 구글의 Google Translate TTS를 활용했습니다.
        
        """
    )

    st.markdown("")

with st.sidebar:
    st.session_state["OPENAI_API"] = st.text_input(label="OPEN_API 키", placeholder="Enter Your API Key", value="", type="password")
    st.markdown("---")



    model = st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])

    st.markdown("---")

    if st.button(label="초기화"):
        st.session_state["chat"] = []
        st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korea"}]
        st.session_state["check_reset"] = True

col1, col2 = st.columns(2)
with col1:
    st.subheader("질문하기")
    audio = audiorecorder("클릭하여 녹음하기77", "녹음 중...")

    if (audio.duration_seconds > 0) and (st.session_state["check_reset"] == False):
        st.audio(audio.export().read())





        question = STT(audio, st.session_state["OPENAI_API"])
        now = datetime.now().strftime("%H:%M")
        st.session_state["chat"] = st.session_state["chat"] + [("user", now, question)]
        st.session_state["messages"] = st.session_state["message"] + [{"role": "user", "content": question}]



with col2:
    st.subheader("질문/답변")


if "chat" not in st.session_state:
    st.session_state["chat"] = []

if "OPEN_API" not in st.session_state:
    st.session_state["OPENAI_API"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korea"}]

if "check_audio" not in st.session_state:
    st.session_state["check_reset"] = False








