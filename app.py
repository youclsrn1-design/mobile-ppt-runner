import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 화면 설정
st.set_page_config(page_title="예창패 피칭덱 메이커", layout="wide")
st.title("🎨 슬라이드 이미지 생성 및 PDF 변환기")

# 2. 슬라이드 데이터 정의
slides_data = [
    {"title": "1. 글로벌 AI 페이스메이커", "content": "스마트폰 하나로 시작하는 초정밀 생체역학 코칭\n전 세계 3억 러너를 위한 부상 방지 솔루션"},
    {"title": "2. Problem: 마라톤의 역설", "content": "러너 70%가 부상에 노출\n고가 장비/레슨 없이는 분석 불가능\n야외 런닝 시 안전 문제 발생"},
    {"title": "3. Solution: 1초 영상 진단", "content": "찍어둔 영상에서 33개 관절 데이터 즉각 추출\n스포츠 의학 기반 정밀 분석\n개인 맞춤형 오디오 피드백 제공"},
    {"title": "4. Core Tech: AI 아키텍처", "content": "Google MediaPipe 기반 검증된 엔진\n자체 생체역학 룰 엔진 알고리즘 독점\n글로벌 데이터 플라이휠 구조"},
    {"title": "5. Business Model: 생태계 장악", "content": "무료 앱 배포로 글로벌 트래픽 확보\n삼성/메타 XR 안경 B2B 제휴 및 판매\n전문가용 프로 요금제(SaaS) 도입"},
    {"title": "6. Future Vision: 공중 AI 코치", "content": "트레드밀 내 AR 고스트 러너 구현\nDJI 드론 추적 연동 및 실시간 피드백\n전 세계 표준 스포츠 AI 두뇌 선점"},
    {"title": "7. Team: 비전을 현실로", "content": "하드웨어/소프트웨어 융합 아키텍트 역량\n글로벌 스케일업 파이프라인 완성\n가장 쉬운 기술로 가장 거대한 시장을 엽니다."}
]

# 3. 이미지 생성 함수 (슬라이드 한 장 그리기)
def create_slide(title, content):
    # 16:9 비율 (1280x720)
    img = Image.new('RGB', (1280, 720), color=(11, 17, 32)) # 다크 네이비 배경
    draw = ImageDraw.Draw(img)
    
    # 텍스트 그리기 (폰트가 없으면 기본 폰트 사용)
    try:
        title_font = ImageFont.load_default() # 실제 환경에선 한글 폰트 경로 필요
    except:
        title_font = None

    # 테두리 및 텍스트 배치
    draw.rectangle([20, 20, 1260, 700], outline=(0, 255, 157), width=5) # 네온 그린 테두리
    draw.text((60, 60), title, fill=(0, 255, 157), font=title_font)
    draw.text((60, 200), content, fill=(226, 232, 240), font=title_font)
    
    return img

# 4. 실행 및 결과 출력
images = []
st.subheader("🖼️ 생성된 슬라이드 미리보기")
cols = st.columns(2)

for i, data in enumerate(slides_data):
    slide_img = create_slide(data['title'], data['content'])
    images.append(slide_img)
    with cols[i % 2]:
        st.image(slide_img, caption=f"Slide {i+1}")

# 5. PDF 변환 및 다운로드 버튼
if st.button("📄 모든 슬라이드 PDF로 합쳐서 다운로드"):
    pdf_buffer = io.BytesIO()
    # 첫 번째 이미지에 나머지 이미지를 붙여서 PDF로 저장
    images[0].save(pdf_buffer, format='PDF', save_all=True, append_images=images[1:])
    
    st.download_button(
        label="📥 PDF 파일 받기",
        data=pdf_buffer.getvalue(),
        file_name="pitch_deck.pdf",
        mime="application/pdf"
    )
