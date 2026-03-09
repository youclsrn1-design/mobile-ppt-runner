import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import urllib.request

# ==========================================
# ⚙️ 0. 한글 폰트 자동 세팅 (글씨 깨짐 완벽 방지)
# ==========================================
font_path = "NanumGothic.ttf"
if not os.path.exists(font_path):
    # 폰트가 없으면 구글 깃허브에서 1초 만에 몰래(?) 다운로드해 옵니다.
    url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
    urllib.request.urlretrieve(url, font_path)

# ==========================================
# 📝 1. 코드 입력 (발표할 내용 세팅)
# ==========================================
st.set_page_config(page_title="예창패 피칭덱 메이커", layout="wide")
st.title("🎯 예창패 PDF 슬라이드 자동 생성기")
st.write("버튼 하나만 누르면 아래 내용이 예쁜 PDF 슬라이드로 변신합니다!")

# 7장짜리 발표 대본 (여기 내용을 자유롭게 수정하시면 됩니다)
slides_data = [
    {"title": "1. 글로벌 AI 페이스메이커", "content": "스마트폰 하나로 시작하는 초정밀 생체역학 코칭\n전 세계 3억 러너를 위한 부상 방지 솔루션"},
    {"title": "2. Problem: 마라톤의 역설", "content": "러너 70%가 부상에 노출\n고가 장비나 레슨 없이는 분석 불가능\n야외 런닝 시 기존 웨어러블의 시야 방해 문제"},
    {"title": "3. Solution: 1초 영상 진단", "content": "찍어둔 영상에서 33개 관절 데이터 즉각 추출\n스포츠 의학 기반 정밀 분석 알고리즘\n개인 맞춤형 오디오 피드백 제공"},
    {"title": "4. Core Tech: AI 아키텍처", "content": "Google MediaPipe 기반 검증된 엔진\n자체 생체역학 룰 엔진 독점\n글로벌 데이터 플라이휠 구조"},
    {"title": "5. Business Model: 생태계 장악", "content": "무료 앱 배포로 글로벌 트래픽 1위 달성\n삼성/메타 XR 안경 B2B 제휴 및 커머스 수익\n전문가용 다중 카메라 프로 요금제(SaaS)"},
    {"title": "6. Future Vision: 공중 AI 코치", "content": "실내: 트레드밀 내 AR 고스트 러너 구현\n야외: DJI 드론 추적 연동 실시간 코칭\n전 세계 표준 스포츠 AI 두뇌 선점"},
    {"title": "7. Team: 비전을 현실로", "content": "하드웨어/소프트웨어 융합 글로벌 아키텍트\n예창패 지원금으로 스케일업 파이프라인 완성\n가장 쉬운 기술로 가장 거대한 시장을 엽니다."}
]

# ==========================================
# 🎨 2. 자동 그리기 (파이썬이 이미지를 굽는 과정)
# ==========================================
def draw_slide(title, content):
    # 16:9 비율 (1280x720) 다크 네이비 배경 생성
    img = Image.new('RGB', (1280, 720), color=(15, 23, 42)) 
    draw = ImageDraw.Draw(img)
    
    # 폰트 크기 설정
    title_font = ImageFont.truetype(font_path, 60)
    content_font = ImageFont.truetype(font_path, 40)
    
    # 네온 그린 테두리 그리기
    draw.rectangle([30, 30, 1250, 690], outline=(0, 255, 157), width=6)
    
    # 제목 쓰기 (네온 그린)
    draw.text((80, 80), title, fill=(0, 255, 157), font=title_font)
    
    # 가로 선 하나 그어주기 (디자인 포인트)
    draw.line([(80, 170), (1200, 170)], fill=(0, 255, 157), width=2)
    
    # 내용 쓰기 (흰색, 줄바꿈 간격 조정)
    draw.text((80, 230), content, fill=(240, 240, 240), font=content_font, spacing=20)
    
    return img

# ==========================================
# 💾 3. 포장 및 다운로드 (PDF로 묶어서 뱉어내기)
# ==========================================
generated_images = []
for data in slides_data:
    slide_image = draw_slide(data["title"], data["content"])
    generated_images.append(slide_image)

st.success("✅ 7장의 슬라이드 이미지가 성공적으로 구워졌습니다!")

# PDF로 변환하기
pdf_buffer = io.BytesIO()
# 첫 번째 이미지에 나머지 이미지들을 덧붙여서 1개의 PDF로 저장
generated_images[0].save(
    pdf_buffer, 
    format='PDF', 
    save_all=True, 
    append_images=generated_images[1:]
)

# 다운로드 버튼 띄우기
st.download_button(
    label="📥 [클릭] 완성된 피칭덱 PDF 다운로드",
    data=pdf_buffer.getvalue(),
    file_name="Pitch_Deck_Master.pdf",
    mime="application/pdf",
    use_container_width=True # 버튼을 큼직하게
)

# 보너스: 화면에 미리보기 띄워주기
st.divider()
st.subheader("👀 PDF 미리보기")
for i, img in enumerate(generated_images):
    st.image(img, caption=f"슬라이드 {i+1}", use_column_width=True)

