import streamlit as st
import os
import sys
from io import StringIO

st.set_page_config(page_title="모바일 PPTX 런처", layout="centered")

st.title("🚀 모바일 파이썬 ➡️ PPT 실행기")
st.write("제미나이가 짜준 PPT 생성 파이썬 코드를 아래에 붙여넣고 실행하세요!")
st.info("💡 필수 규칙: 코드 마지막에 반드시 `prs.save('output.pptx')` 로 파일을 저장하도록 코드를 짜달라고 하세요!")

# 기본 예제 코드 (처음 접속했을 때 보이는 코드)
default_code = """from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])
title = slide.shapes.title
title.text = "스마트폰에서 파이썬 코드가 실행되었습니다!"

# 이 이름으로 저장해야 서버가 인식하고 다운로드 버튼을 띄워줍니다.
prs.save('output.pptx')
"""

user_code = st.text_area("여기에 파이썬 코드를 붙여넣으세요:", value=default_code, height=300)

if st.button("▶️ 코드 실행 및 PPT 만들기"):
    # 이전 실행 결과물이 남아있다면 삭제
    if os.path.exists("output.pptx"):
        os.remove("output.pptx")
        
    # 코드 에러를 화면에 보여주기 위한 세팅
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        # 핵심: 입력받은 파이썬 코드를 여기서 즉시 실행(Run)합니다!
        exec(user_code)
        sys.stdout = old_stdout
        
        st.success("✅ 파이썬 코드 실행 완료!")
        
        # 코드가 정상적으로 output.pptx를 만들었는지 확인
        if os.path.exists("output.pptx"):
            with open("output.pptx", "rb") as file:
                st.download_button(
                    label="📥 완성된 PPT 스마트폰에 다운로드",
                    data=file,
                    file_name="my_mobile_presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
        else:
            st.warning("⚠️ 코드는 실행되었지만 `output.pptx` 파일이 생성되지 않았습니다. 코드 마지막 줄을 확인해주세요.")
            
    except Exception as e:
        sys.stdout = old_stdout
        st.error(f"❌ 코드 실행 중 에러가 발생했습니다:\n{e}")
