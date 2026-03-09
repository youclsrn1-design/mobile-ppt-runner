import streamlit as st
import os
import sys
from io import StringIO
import base64

st.set_page_config(page_title="AI 코드 실행 허브", layout="centered")

# --- UI 헤더 ---
st.markdown("## 🎯 AI 파이썬 코드 만능 실행기")
st.write("이미지, PDF, PPTX를 생성하는 파이썬 코드를 아래에 넣고 버튼을 누르세요!")

# --- 상태 초기화 및 기존 파일 정리 ---
def cleanup_old_files():
    for ext in ['png', 'jpg', 'pdf', 'pptx']:
        if os.path.exists(f"output.{ext}"):
            os.remove(f"output.{ext}")

# --- PDF 미리보기 함수 ---
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400" type="application/pdf" style="border: 2px solid #ccc; border-radius: 10px;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- 코드 입력창 ---
user_code = st.text_area(
    "여기에 AI가 짜준 코드를 붙여넣으세요:", 
    height=250, 
    placeholder="import matplotlib.pyplot as plt...\n\n# 반드시 마지막에 output.png, output.pdf, output.pptx로 저장되게 해주세요."
)

if st.button("🚀 코드 실행 및 결과물 굽기", use_container_width=True):
    cleanup_old_files()
    
    # 에러 출력을 화면에 잡기 위한 설정
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    with st.spinner("코드를 실행하며 파일을 굽는 중입니다... ⏳"):
        try:
            # 💡 핵심: 입력받은 코드를 즉시 실행
            exec(user_code)
            sys.stdout = old_stdout
            
            st.success("✅ 파일이 성공적으로 구워졌습니다!")
            st.divider()
            
            # --- 결과물 확인 및 UI 출력 ---
            file_found = False
            
            # 1. 이미지(PNG) 처리
            if os.path.exists("output.png"):
                file_found = True
                st.markdown("### 👀 이미지 미리보기")
                st.image("output.png", use_container_width=True)
                with open("output.png", "rb") as file:
                    st.download_button(label="📥 [클릭] 이미지 다운로드", data=file, file_name="ai_image.png", mime="image/png", use_container_width=True)
            
            # 2. PDF 처리
            if os.path.exists("output.pdf"):
                file_found = True
                st.markdown("### 👀 PDF 미리보기")
                show_pdf("output.pdf")
                with open("output.pdf", "rb") as file:
                    st.download_button(label="📥 [클릭] 완성된 PDF 다운로드", data=file, file_name="ai_document.pdf", mime="application/pdf", use_container_width=True)
            
            # 3. PPTX 처리 (PPT는 브라우저 미리보기가 어려워 다운로드만 제공)
            if os.path.exists("output.pptx"):
                file_found = True
                st.markdown("### 📊 PPT 생성 완료")
                st.info("PPT 파일은 사파리에서 바로 다운로드하여 확인해 주세요!")
                with open("output.pptx", "rb") as file:
                    st.download_button(label="📥 [클릭] 파워포인트(PPTX) 다운로드", data=file, file_name="ai_presentation.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation", use_container_width=True)
            
            if not file_found:
                st.warning("⚠️ 코드는 실행되었지만 'output.png', 'output.pdf', 'output.pptx' 중 어떤 파일도 생성되지 않았습니다. AI에게 파일명을 지정해 달라고 다시 요청해 보세요.")
                
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"❌ 코드 실행 중 에러가 발생했습니다:\n{e}")
