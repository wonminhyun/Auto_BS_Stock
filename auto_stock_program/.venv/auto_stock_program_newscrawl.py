import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt

def crawl_rss_news(stock_name="삼성전자"):
    url = f"https://news.google.com/rss/search?q={stock_name}+when:1d&hl=ko&gl=KR&ceid=KR:ko"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    articles = []
    for item in soup.find_all('item'):
        title = item.title.text
        link = item.link.text
        articles.append((title, link))

    return articles

def clean_text(text):
    okt = Okt()
    words = okt.nouns(text)
    stopwords = ['기사', '내용', '관련']
    return [w for w in words if w not in stopwords]

def score_news(text):
    positive_keywords = ['호재', '급등', '사상최고', '실적호조']
    negative_keywords = ['악재', '하락', '적자', '급락']
    score = 0
    for word in positive_keywords:
        if word in text:
            score += 1
    for word in negative_keywords:
        if word in text:
            score -= 1
    return score

def make_decision(news_scores, threshold_buy=2, threshold_sell=-2):
    total_score = sum(news_scores)
    if total_score >= threshold_buy:
        return "BUY"
    elif total_score <= threshold_sell:
        return "SELL"
    else:
        return "HOLD"

def send_order(decision):
    if decision == "BUY":
        print("매수")
    elif decision == "SELL":
        print("매도")
    else:
        print("홀드")

def run_pipeline(stock_name):
    articles = crawl_rss_news(stock_name)
    scores = []

    print(f"\n '{stock_name}' 관련 뉴스 분석 결과:\n")
    for title, link in articles:
        print(f"[제목] {title}")
        cleaned = clean_text(title)
        score = score_news(" ".join(cleaned))
        print(f"점수: {score}\n")
        scores.append(score)

    decision = make_decision(scores)
    print(f"\n 뉴스 종합 점수: {sum(scores)} → 매매 판단: {decision}")
    send_order(decision)

if __name__ == "__main__":
    run_pipeline("삼성전자")
