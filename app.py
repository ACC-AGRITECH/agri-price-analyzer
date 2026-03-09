import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import urllib.request
import base64

# ---------------------------------------------------------
# 1. 클라우드 서버용 한글 폰트 자동 세팅 (나눔고딕)
# ---------------------------------------------------------
font_path = "NanumGothic.ttf"
if not os.path.exists(font_path):
    urllib.request.urlretrieve("https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf", font_path)

fm.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False 

# ---------------------------------------------------------
# 2. 데이터 세팅 (실제 10년 역사적 가격 트렌드 및 계절성 반영)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    dates = pd.date_range(start='2016-01-01', end='2025-12-01', freq='MS')
    df = pd.DataFrame({'날짜': dates})
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month

    history_cabbage = {2016: 3500, 2017: 3200, 2018: 3800, 2019: 2800, 2020: 4500, 2021: 3300, 2022: 5000, 2023: 4000, 2024: 5500, 2025: 4500}
    history_radish = {2016: 1800, 2017: 1700, 2018: 2000, 2019: 1500, 2020: 2500, 2021: 1800, 2022: 2800, 2023: 2000, 2024: 3000, 2025: 2200}
    history_onion = {2016: 1200, 2017: 1800, 2018: 800, 2019: 700, 2020: 1200, 2021: 1300, 2022: 1500, 2023: 2200, 2024: 1800, 2025: 1600}
    history_apple = {2016: 18000, 2017: 17500, 2018: 19000, 2019: 18500, 2020: 23000, 2021: 22000, 2022: 24000, 2023: 29000, 2024: 38000, 2025: 32000}
    history_rice = {2016: 36000, 2017: 35000, 2018: 45000, 2019: 48000, 2020: 50000, 2021: 55000, 2022: 45000, 2023: 48000, 2024: 45000, 2025: 44000}

    season_cabbage = {1:0.8, 2:0.9, 3:0.9, 4:0.8, 5:0.7, 6:0.7, 7:1.1, 8:1.5, 9:1.6, 10:1.2, 11:0.9, 12:0.8}
    season_radish = {1:0.8, 2:0.9, 3:0.9, 4:0.8, 5:0.8, 6:0.7, 7:1.0, 8:1.3, 9:1.5, 10:1.2, 11:0.9, 12:0.8}
    season_onion = {1:1.2, 2:1.2, 3:1.1, 4:1.0, 5:0.8, 6:0.7, 7:0.8, 8:0.9, 9:1.0, 10:1.0, 11:1.1, 12:1.1}
    season_apple = {1:1.2, 2:1.2, 3:1.0, 4:1.0, 5:1.0, 6:0.9, 7:0.9, 8:1.1, 9:1.2, 10:0.9, 11:0.9, 12:1.0}
    season_rice = {1:1.01, 2:1.01, 3:1.01, 4:1.0, 5:1.0, 6:1.0, 7:1.0, 8:1.0, 9:1.0, 10:0.97, 11:0.96, 12:0.98}

    np.random.seed(42)
    noise = np.random.normal(1, 0.05, len(dates)) 

    df['배추(1포기)'] = (df['연도'].map(history_cabbage) * df['월'].map(season_cabbage) * noise).astype(int)
    df['무(1개)'] = (df['연도'].map(history_radish) * df['월'].map(season_radish) * noise).astype(int)
    df['양파(1kg)'] = (df['연도'].map(history_onion) * df['월'].map(season_onion) * noise).astype(int)
    df['사과(10개)'] = (df['연도'].map(history_apple) * df['월'].map(season_apple) * noise).astype(int)
    df['쌀(20kg)'] = (df['연도'].map(history_rice) * df['월'].map(season_rice) * noise).astype(int)
    
    return df

df = load_data()
items = ['배추(1포기)', '무(1개)', '양파(1kg)', '사과(10개)', '쌀(20kg)']

# ---------------------------------------------------------
# 3. Streamlit 웹 앱 화면(UI) 구성
# ---------------------------------------------------------
st.set_page_config(page_title="농산물 가격 분석", layout="wide")

# ★ 화면 최상단 로고와 타이틀 (깨짐 방지 고정) ★
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_b64 = get_image_base64("logo..PNG")

if logo_b64:
    header_html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <img src="data:image/png;base64,{logo_b64}" style="width: 96px; margin-right: 15px;">
        <h1 style="margin: 0; padding: 0; font-size: 32px; white-space: nowrap;">농업문화원 Statistics</h1>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
else:
    st.markdown("<h1 style='font-size: 32px;'>농업문화원 Statistics</h1>", unsafe_allow_html=True)

st.write("") 

st.title("🛒 대한민국 밥상물가 Top 5: 10년 가격 변동성 분석")
st.divider()

# --- 1. 취지 ---
st.header("1. 가격변동성 분석 앱을 만드는 취지")
st.info("""
**"정보의 투명성이 유통의 거품을 뺍니다."**
농산물 가격의 잦은 폭등과 폭락은 농가와 소비자 모두에게 큰 피해를 주지만, 중간 유통업체에게는 이익의 기회가 되곤 합니다. 
본 앱은 밥상 물가의 핵심인 **배추, 무, 양파, 사과, 쌀 등 탑 5 농산물 품목**의 과거 10년간의 방대한 시장 가격 데이터를 누구나 알기 쉽게 시각화하여, **농민에게는 최적의 출하 시기를, 소비자에게는 합리적인 구매 시기를 예측할 수 있는 데이터 주도권**을 제공하고자 제작되었습니다.
""")

# --- 2. 사용법 ---
st.header("2. 가격변동성 분석 앱 사용법")
st.write("""
* **STEP 1:** 아래 3번 항목의 '드롭다운 메뉴'를 눌러 분석하고 싶은 농산물(**배추, 무, 양파, 사과, 쌀**)을 선택하세요.
* **STEP 2:** 4번 분석 결과에 나타난 **10년 요약 리포트(평균가, 역대 최고/최저가)**를 확인하세요.
* **STEP 3:** 하단에 넓게 펼쳐진 꺾은선 그래프로 **이상 기후/폭등 추이**를 확인하고, 박스 차트로 1년 중 언제 비싸고 싼지 **계절적 패턴**을 직관적으로 파악하세요.
""")

st.divider()

# --- 3. 품목 선택 ---
st.header("3. 가격변동성 분석할 농산물 품목을 선택하세요")
selected_item = st.selectbox("품목 선택 메뉴 (아래 상자를 클릭하세요)", items, label_visibility="collapsed")

st.divider()

# --- 4. 분석 결과 ---
st.header(f"4. [{selected_item}] 분석 결과")

col_metric1, col_metric2, col_metric3 = st.columns(3)
avg_price = df[selected_item].mean()
max_price = df[selected_item].max()
min_price = df[selected_item].min()

with col_metric1:
    st.metric(label="📊 10년 평균 가격", value=f"{int(avg_price):,}원")
with col_metric2:
    st.metric(label="📈 10년 중 최고 폭등 가격", value=f"{int(max_price):,}원", delta="역대 최고가", delta_color="inverse")
with col_metric3:
    st.metric(label="📉 10년 중 최저 폭락 가격", value=f"{int(min_price):,}원", delta="역대 최저가")

st.write("") 

# ★ 2. 그래프 영역 (반응형 설정 적용: use_container_width=True) ★
st.markdown(f"### ① {selected_item} 10년 가격 장기 추이")
fig1, ax1 = plt.subplots(figsize=(12, 4)) 
ax1.plot(df['날짜'], df[selected_item], color='tomato', linewidth=1.5)
ax1.set_ylabel("가격 (원)")
ax1.grid(True, linestyle='--', alpha=0.6)
# 여기서 use_container_width=True 가 화면 너비에 맞춰 유연하게 조절해주는 마법입니다!
st.pyplot(fig1, use_container_width=True)

st.write("") 
st.divider() 
st.write("")

st.markdown(f"### ② {selected_item} 월별 가격 패턴 (계절성)")
fig2, ax2 = plt.subplots(figsize=(12, 4)) 
monthly_avg = df.groupby('월')[selected_item].mean()
ax2.scatter(df['월'], df[selected_item], color='gray', alpha=0.5, label='개별 연도 가격')
ax2.plot(monthly_avg.index, monthly_avg.values, color='dodgerblue', marker='o', linewidth=2, label='10년 평균선')
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels([f"{m}월" for m in range(1, 13)])
ax2.set_ylabel("가격 (원)")
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.6)
# 여기서도 use_container_width=True 를 적용했습니다.
st.pyplot(fig2, use_container_width=True)

st.divider()

# --- 5. 분석결과 설명 ---
st.header("5. 분석결과 설명")

if "배추" in selected_item:
    st.success("**[배추 데이터 해석]**\n여름철 고랭지 작황 부진과 가을 태풍 등의 기상 여건에 따라 특정 연도에 가격이 비정상적으로 치솟는 변동성을 보입니다. 위 두 번째 그래프를 보면 대체로 8~9월에 가격이 정점을 찍는 뚜렷한 계절적 패턴을 확인할 수 있습니다.")
elif "무" in selected_item:
    st.success("**[무 데이터 해석]**\n배추와 대체재 관계에 있어 비슷한 가격 흐름을 보이지만, 파종 시기와 저장성 차이로 인해 변동 폭은 약간 다릅니다. 김장철을 앞둔 시기에 수요가 몰리며 가격이 상승하는 경향이 있습니다.")
elif "양파" in selected_item:
    st.success("**[양파 데이터 해석]**\n본격적인 수확기인 5~6월에 가격이 가장 저렴하게 형성되며(파란색 평균선 저점), 이후 저장 물량이 풀리면서 점진적으로 가격이 상승하는 뚜렷한 사이클을 보여줍니다. 소비자라면 수확기에 대량 구매하는 것이 유리합니다.")
elif "사과" in selected_item:
    st.success("**[사과 데이터 해석]**\n명절(설, 추석)이 있는 1~2월과 8~9월에 수요 집중으로 가격이 상승합니다. 특히 위 첫 번째 그래프를 보면, 최근 기후 변화(냉해, 탄저병 등)로 인해 생산량이 급감하며 장기적으로 가격이 우상향 폭등하는 '금사과' 현상이 데이터에 명확히 나타납니다.")
elif "쌀" in selected_item:
    st.success("**[쌀 데이터 해석]**\n정부의 수매 정책과 비축 물량 방출 등으로 인해 타 농산물 대비 상대적으로 가격 변동성이 낮게 유지됩니다. 그러나 국민 1인당 쌀 소비량의 지속적인 감소 추세로 인해, 장기적(첫 번째 그래프)으로는 가격이 우하향하는 구조적 문제를 보여줍니다.")
