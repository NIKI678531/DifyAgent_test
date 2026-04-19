import datetime as dt

def fetch_news_headlines(ticker: str, limit=6):
    headlines = []
    try:
        tk = yf.Ticker(ticker)
        # Newer yfinance versions often provide a list of dicts with 'title' and 'link'
        for n in (tk.news or [])[:limit]:
            headlines.append({
                "title": n.get("title", "")[:160],
                "url": n.get("link") or n.get("providerPublishTime") or "",
            })
    except Exception:
        pass  # fallback below

    # Optional: Alpha Vantage Market News (requires ALPHA_VANTAGE_API_KEY)
    if len(headlines) == 0 and os.getenv("ALPHA_VANTAGE_API_KEY"):
        import requests
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker.upper(),
            "apikey": os.getenv("ALPHA_VANTAGE_API_KEY"),
            "sort": "LATEST",
            "limit": limit
        }
        r = requests.get("https://www.alphavantage.co/query", params=params, timeout=30)
        if r.ok:
            data = r.json().get("feed", [])[:limit]
            for item in data:
                headlines.append({
                    "title": item.get("title", "")[:160],
                    "url": item.get("url", "")
                })
    return headlines