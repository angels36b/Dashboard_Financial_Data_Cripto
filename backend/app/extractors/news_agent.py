import feedparser
import schedule
import time
import email.utils
from datetime import datetime
from app.database.db_manager import save_news

print("🚀Init SCRIPT: Data Agent Online.")

RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Yahoo_Macro": "https://finance.yahoo.com/news/rssindex"
}

KEYWORDS = ["solana", "bitcoin", "crypto", "fed", "inflation", "rate", "sec", "war", "etf"]
HIGH_IMPACT_WORDS = ["war", "crash", "sec", "fed", "inflation", "hack"]

def evaluate_impact(headline):
    headline_lower = headline.lower()
    if any(word in headline_lower for word in HIGH_IMPACT_WORDS):
        return "high"
    elif any(word in headline_lower for word in KEYWORDS):
        return "medium"
    return "low"

def format_rss_date(rss_date_string):
    """Converts messy RSS dates into a clean 'DD --MM--YYYY HH:MM' format"""
    try:
        # Parse the standard RSS date format
        parsed_tuple = email.utils.parsedate_tz(rss_date_string)
        if parsed_tuple:
            dt = datetime.fromtimestamp(email.utils.mktime_tz(parsed_tuple))
            return dt.strftime("%D  %H:%M UTC")
        return rss_date_string
    except:
        return "Recent"

def fetch_and_filter_news():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Agent Waking Up: Fetching feeds...")
    relevant_news = []

    for source_name, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                title = entry.title

                if any(keyword in title.lower() for keyword in KEYWORDS):
                    impact = evaluate_impact(title)
                    # 👈 NEW: Extracting the publication date
                    raw_date = entry.get('published', entry.get('updated', 'Unknown Date'))
                    clean_date = format_rss_date(raw_date)

                    relevant_news.append({
                        "source": source_name,
                        "headline": title,
                        "impact": impact,
                        "date": clean_date # Saving the date
                    })
        except Exception as e:
            print(f"❌ Error with {source_name}: {e}")

    if relevant_news:
        print(f"✅ Found {len(relevant_news)} relevant events:")
        for item in relevant_news:
            impact_icon = "🔴" if item['impact'] == 'high' else "🟡" if item['impact'] == 'medium' else "🔵"
            # 👈 NEW: Printing the date on the screen
            print(f"  {impact_icon} [{item['date']}] [{item['source']}] {item['headline']}")
        #save data on database
        saved_count = save_news(relevant_news)
        print(f"Saved{saved_count} new articles to tha database")
    else:
        print("💤 No relevant news found in this cycle.")

if __name__ == "__main__":
    
    fetch_and_filter_news()
    print("\n🏁 PRUEBA TERMINADA.")