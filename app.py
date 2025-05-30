import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="wide"
)

# API 키 불러오기
try:
    with open("apikey.txt", "r") as f:
        api_key = f.read().strip()
    
    if not api_key:
        st.error("API 키가 비어있습니다. apikey.txt 파일을 확인해주세요.")
        st.stop()
except FileNotFoundError:
    st.error("apikey.txt 파일을 찾을 수 없습니다. 프로젝트 루트에 파일을 추가해주세요.")
    st.stop()

# Gemini 모델 설정
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
except Exception as e:
    st.error(f"모델 초기화 중 오류가 발생했습니다: {str(e)}")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 제목과 설명
st.title("🤖 Gemini 챗봇")
st.markdown("Gemini API를 활용한 기본 챗봇 프레임워크입니다.")
st.divider()

# 사이드바 설정
with st.sidebar:
    st.header("💬 채팅 설정")
    if st.button("대화 내용 초기화"):
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.chat_history = []
        st.rerun()

# 이전 대화 내용 표시
if st.session_state.chat_history:
    with st.expander("📜 이전 대화 보기", expanded=False):
        for i, message in enumerate(st.session_state.chat_history):
            header = "👤 사용자" if message["role"] == "user" else "🤖 Gemini"
            color = "blue" if message["role"] == "user" else "green"
            
            st.markdown(f"<div style='border-left: 2px solid {color}; padding-left: 10px; margin: 10px 0;'>", unsafe_allow_html=True)
            st.markdown(f"**{header}**")
            st.markdown(message["content"])
            st.markdown("</div>", unsafe_allow_html=True)
            
            if i < len(st.session_state.chat_history) - 1:
                st.markdown("---")

# 현재 대화 표시
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    try:
        with st.chat_message("assistant"):
            with st.spinner("응답 생성 중..."):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"응답 생성 중 오류가 발생했습니다: {str(e)}")
