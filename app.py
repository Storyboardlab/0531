import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="wide"
)

# API 키 설정 및 모델 초기화
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Google API 키가 설정되지 않았습니다. .streamlit/secrets.toml 파일에 GOOGLE_API_KEY를 설정해주세요.")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
if not api_key:
    st.error("Google API 키가 비어있습니다. 유효한 API 키를 설정해주세요.")
    st.stop()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # 세션 상태에 모델 저장
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

# 구분선
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
            # 메시지 헤더 스타일 설정
            if message["role"] == "user":
                header = "👤 사용자"
                color = "blue"
            else:
                header = "🤖 Gemini"
                color = "green"
            
            # 메시지 컨테이너 스타일링
            st.markdown(f"<div style='border-left: 2px solid {color}; padding-left: 10px; margin: 10px 0;'>", unsafe_allow_html=True)
            st.markdown(f"**{header}**")
            st.markdown(message["content"])
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 마지막 메시지가 아닌 경우 구분선 추가
            if i < len(st.session_state.chat_history) - 1:
                st.markdown("---")

# 현재 대화 표시
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 채팅 기록에 사용자 메시지 추가
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    try:
        # 로딩 스피너 표시
        with st.chat_message("assistant"):
            with st.spinner("응답 생성 중..."):
                # Gemini 모델에 메시지 전송 및 응답 받기
                response = st.session_state.chat.send_message(prompt)
                
                # 응답 표시
                st.markdown(response.text)
                
                # 채팅 기록에 AI 응답 추가
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    
    except Exception as e:
        st.error(f"응답 생성 중 오류가 발생했습니다: {str(e)}") 