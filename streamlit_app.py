import streamlit as st
import requests
import textwrap

# --------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 스타일링
# --------------------------------------------------------------------------

# 페이지의 제목과 레이아웃을 설정합니다.
st.set_page_config(
    page_title="실시간 뉴스 검색기",
    page_icon="📰",
    layout="wide"
)

# CSS를 사용하여 앱의 전체적인 스타일을 진한 남색 테마로 지정합니다.
st.markdown("""
<style>
/* 전체 배경 */
.stApp {
    background-color: #0A192F;
}

/* 메인 콘텐츠 영역 */
.main .block-container {
    background-color: #0A192F;
    color: #E6F1FF;
}

/* 제목 텍스트 */
h1 {
    color: #CCD6F6 !important;
    text-align: center;
    padding-bottom: 20px;
}

/* 검색 입력창 */
.stTextInput > div > div > input {
    background-color: #172A45;
    color: #E6F1FF;
    border: 1px solid #2A3C5A;
    border-radius: 8px;
}

/* 검색 버튼 */
.stButton > button {
    width: 100%;
    background-color: #64FFDA;
    color: #0A192F;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    background-color: #0A192F;
    color: #64FFDA;
    border: 1px solid #64FFDA;
}

/* 뉴스 카드 스타일 */
.news-card {
    background-color: #172A45;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid #2A3C5A;
    transition: transform 0.2s;
    height: 100%; /* 카드의 높이를 동일하게 설정 */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.news-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}
.news-card img {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 15px;
    object-fit: cover;
    height: 200px;
}
.news-card h3 {
    font-size: 1.2rem;
    color: #CCD6F6;
    margin-bottom: 10px;
    /* 긴 제목을 여러 줄로 표시 */
    white-space: normal;
    word-wrap: break-word;
}
.news-card p {
    font-size: 0.9rem;
    color: #A8B2D1;
    flex-grow: 1; /* 내용이 카드 높이를 채우도록 함 */
}
.news-card a {
    display: inline-block;
    margin-top: 15px;
    padding: 8px 12px;
    background-color: #0A192F;
    color: #64FFDA;
    text-decoration: none;
    border-radius: 5px;
    border: 1px solid #64FFDA;
    text-align: center;
    transition: all 0.2s ease-in-out;
}
.news-card a:hover {
    background-color: #64FFDA;
    color: #0A192F;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 2. 뉴스 데이터 로드 함수
# --------------------------------------------------------------------------

# NewsAPI를 호출하여 뉴스 데이터를 가져오는 함수
def get_news(api_key, query):
    """
    NewsAPI를 사용하여 특정 검색어에 대한 뉴스를 가져옵니다.
    - api_key: NewsAPI에서 발급받은 개인 키
    - query: 검색할 키워드
    - 반환값: 뉴스 기사 리스트 (JSON 형식)
    """
    if not query:
        return None

    url = (f"https://newsapi.org/v2/everything?"
           f"q={query}&"
           f"language=ko&"  # 한국어 뉴스 우선 검색
           f"sortBy=publishedAt&"
           f"apiKey={api_key}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        news_data = response.json()
        return news_data.get("articles", [])
    except requests.exceptions.RequestException as e:
        st.error(f"뉴스 데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return None
    except Exception as e:
        st.error(f"알 수 없는 오류가 발생했습니다: {e}")
        st.error(f"API 응답: {response.text}")
        return None

# --------------------------------------------------------------------------
# 3. 메인 애플리케이션 UI 구성
# --------------------------------------------------------------------------

st.title("📰 실시간 뉴스 검색기")

# NewsAPI 키 입력 (실제 배포 시에는 환경 변수 사용을 권장합니다)
API_KEY = "14509d62727b490ba5a986ddf9ff5c43"  # API 키가 적용되었습니다.

# 사용자로부터 검색어를 입력받습니다.
search_query = st.text_input(
    "검색할 키워드를 입력하세요 (예: AI, 반도체, 날씨 등)",
    value="인공지능" # 기본 검색어
)

# 검색 버튼을 누르면 뉴스 검색을 시작합니다.
if st.button("뉴스 검색하기"):
    if not search_query:
        st.warning("검색어를 입력해주세요.")
    else:
        with st.spinner(f"'{search_query}' 관련 뉴스를 검색 중입니다..."):
            articles = get_news(API_KEY, search_query)

            if articles is None:
                # 오류 메시지는 get_news 함수 내에서 처리됩니다.
                pass
            elif not articles:
                st.info("검색 결과에 해당하는 뉴스가 없습니다.")
            else:
                # 뉴스를 3개의 컬럼으로 나누어 표시합니다.
                cols = st.columns(3)
                for i, article in enumerate(articles):
                    col = cols[i % 3]
                    with col:
                        # 이미지가 없는 경우를 대비한 기본 이미지 URL
                        image_url = article.get("urlToImage", "https://placehold.co/600x400/0A192F/E6F1FF?text=No+Image")

                        # 제목과 요약의 길이를 제한하여 UI가 깨지지 않도록 합니다.
                        title = textwrap.shorten(article.get("title", "제목 없음"), width=50, placeholder="...")
                        description = textwrap.shorten(article.get("description", "요약 없음"), width=100, placeholder="...")

                        # HTML과 CSS를 사용하여 뉴스 카드를 만듭니다.
                        st.markdown(f"""
                        <div class="news-card">
                            <img src="{image_url}" alt="News Image">
                            <h3>{title}</h3>
                            <p>{description}</p>
                            <a href="{article.get('url', '#')}" target="_blank">기사 전문 보기</a>
                        </div>
                        """, unsafe_allow_html=True)
