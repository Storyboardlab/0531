# Gemini 챗봇

Google의 Gemini-Pro 모델을 활용한 간단한 챗봇 애플리케이션입니다.

## 설치 방법

1. 가상환경 활성화:
```bash
source venv/bin/activate
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. Google API 키 설정:
- `.streamlit/secrets.toml` 파일에서 `GOOGLE_API_KEY` 값을 본인의 API 키로 수정

## 실행 방법

```bash
streamlit run app.py
```

## 주요 기능

- Gemini-Pro 모델을 활용한 대화형 챗봇
- 채팅 기록 유지
- 사용자 친화적인 인터페이스

## 기술 스택

- Python
- Streamlit
- Google Generative AI (Gemini-Pro) 