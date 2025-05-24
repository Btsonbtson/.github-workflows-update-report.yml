import os
import feedparser
import requests
import random
import pytz
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from ics import Calendar

NEWS_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(NEWS_DIR, "index.html")

# --- Ρυθμίσεις πηγών ---
GEOPOLITICS_FEEDS = [
    'https://www.politico.eu/rss/feed.xml',
    'https://feeds.reuters.com/reuters/topNews',
    'https://www.lemonde.fr/en/international/rss_full.xml',
    'https://www.foreignaffairs.com/rss.xml',
    'https://www.rednews.gr/feed/',
    'https://www.economist.com/europe/rss.xml',
]

STATIC_GEOPOLITICS_LINKS = [
    ("Politico", "https://www.politico.eu/"),
    ("Reuters", "https://www.reuters.com/"),
    ("TheStreet", "https://www.thestreet.com/"),
    ("LeMonde", "https://www.lemonde.fr/en/"),
    ("Economist", "https://www.economist.com/"),
    ("Foreign Affairs", "https://www.foreignaffairs.com/"),
    ("Flight.gr", "https://flight.com.gr/"),
    ("Defence Point", "https://www.defence-point.gr/news/"),
    ("Elisme", "https://elisme.gr/"),
    ("Nordic Monitor", "https://nordicmonitor.com/"),
]

SPORT_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/el/2/23/Olympiacos_FC_logo.svg",
    "https://www.olympiacos.org/wp-content/uploads/2023/02/omada2023.jpg",
    "https://media.sport24.gr/pictures/1200x675crop/2023/10/19/olympiakos-podosfairo.jpg",
]

YOUTUBE_FEEDS = [
    ("Lambros Kalarritis", "https://www.youtube.com/feeds/videos.xml?channel_id=UCUCgaiCbXcQF9DmQE7TrEbw"),
    ("Geostratigiki", "https://www.youtube.com/feeds/videos.xml?channel_id=UCBwZu8NnOXRV2qG9QRXsOjw"),
    ("Enimerosi kai Skepsi", "https://www.youtube.com/feeds/videos.xml?channel_id=UC9N9Jx1dH3OGJDpS0RHG6vA"),
    ("SporFM 94.6 (Ολυμπιακός)", "https://www.youtube.com/feeds/videos.xml?channel_id=UC9N9Jx1dH3OGJDpS0RHG6vA"),
    ("Red Sports 7", "https://www.youtube.com/feeds/videos.xml?playlist_id=PLjNrFe0Be4XRIU3PUsF4MoPvb1qEqFYUE"),
]

SPORTS_LINKS = {
    'SporFM 94.6 (Ολυμπιακός)': 'https://www.sport-fm.gr/',
    'Red Sports 7': 'https://www.redsports7.gr/',
}

GEOPOLITICS_IMAGES = [
    "https://www.nato.int/nato_static_fl2014/assets/pictures/2021/11/211122a-map/211122a-map-003.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/EU_NATO_map.png/800px-EU_NATO_map.png",
]

MARKET_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Stock_market_indices_graph_%28August_2023%29.png/800px-Stock_market_indices_graph_%28August_2023%29.png",
    "https://tradingeconomics.com/charts/sp-500.png",
]

COMMODITY_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Oil_prices_1970-2017.png/800px-Oil_prices_1970-2017.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Shipping_containers_at_Port_of_Singapore.jpg/800px-Shipping_containers_at_Port_of_Singapore.jpg",
]

# Keywords για φιλτράρισμα θεματολογίας
TOPIC_KEYWORDS = {
    "Ελληνο-Τουρκικές Σχέσεις": ["Greece-Turkey", "Greek-Turkish", "Ελληνο-Τουρκικές", "Ελλάδα-Τουρκία", "Aegean", "Cyprus"],
    "Γεωπολιτική": ["Geopolitics", "Geopolitical", "Γεωπολιτική", "NATO", "EU", "Middle East", "Russia", "China"],
    "Διεθνείς Σχέσεις": ["International Relations", "Diplomacy", "Διεθνείς Σχέσεις", "Foreign Policy", "United Nations"],
}

def random_geopolitics_image():
    return random.choice(GEOPOLITICS_IMAGES)

def random_market_image():
    return random.choice(MARKET_IMAGES)

def random_commodity_image():
    return random.choice(COMMODITY_IMAGES)

def random_sport_image():
    return random.choice(SPORT_IMAGES)

def fetch_feed_links(urls, max_items=4):
    headlines = []
    now = datetime.now(pytz.UTC)
    last_24_hours = now - timedelta(hours=24)

    for url in urls:
        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                print(f"No entries found for feed: {url}")
                continue
            for entry in feed.entries[:max_items]:
                pub_date = entry.get('published_parsed') or entry.get('updated_parsed')
                if not pub_date:
                    continue
                pub_datetime = datetime(*pub_date[:6], tzinfo=pytz.UTC)
                if pub_datetime < last_24_hours:
                    continue

                title = entry.title.lower()
                summary = entry.get('summary', '').lower()
                matches_topic = False
                for topic, keywords in TOPIC_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword.lower() in title or keyword.lower() in summary:
                            matches_topic = True
                            break
                    if matches_topic:
                        break

                if matches_topic:
                    headlines.append(f'<li><a href="{entry.link}" target="_blank" class="text-blue-600 hover:underline">{entry.title}</a></li>')
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")
            continue
    return headlines

def scrape_thestreet():
    headlines = []
    url = "https://www.thestreet.com/markets"
    now = datetime.now(pytz.UTC)
    last_24_hours = now - timedelta(hours=24)

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('a', class_='news-listing__title', limit=4)

        for article in articles:
            title = article.text.strip()
            link = "https://www.thestreet.com" + article['href']
            
            matches_topic = False
            for topic, keywords in TOPIC_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in title.lower():
                        matches_topic = True
                        break
                if matches_topic:
                    break

            if matches_topic:
                headlines.append(f'<li><a href="{link}" target="_blank" class="text-blue-600 hover:underline">{title}</a></li>')
    except Exception as e:
        print(f"Error scraping TheStreet: {e}")
    return headlines

def scrape_additional_sources():
    headlines = []
    sources = [
        ("Defence Point", "https://www.defence-point.gr/news/", "article.post"),
        ("Elisme", "https://elisme.gr/", "div.post"),
        ("Nordic Monitor", "https://nordicmonitor.com/", "h2.entry-title"),
    ]
    now = datetime.now(pytz.UTC)
    last_24_hours = now - timedelta(hours=24)

    for name, url, selector in sources:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select(selector, limit=4)

            for article in articles:
                title = article.text.strip()
                link = article.find('a')['href']
                if not link.startswith('http'):
                    link = url + link

                matches_topic = False
                for topic, keywords in TOPIC_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword.lower() in title.lower():
                            matches_topic = True
                            break
                    if matches_topic:
                        break

                if matches_topic:
                    headlines.append(f'<li><a href="{link}" target="_blank" class="text-blue-600 hover:underline">{title}</a></li>')
        except Exception as e:
            print(f"Error scraping {name}: {e}")
    return headlines

def fetch_youtube_videos():
    videos = {}
    now = datetime.now(pytz.UTC)
    last_24_hours = now - timedelta(hours=24)

    for channel_name, feed_url in YOUTUBE_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            if not feed.entries:
                continue
            videos[channel_name] = []
            for entry in feed.entries[:3]:
                pub_date = entry.get('published_parsed')
                if not pub_date:
                    continue
                pub_datetime = datetime(*pub_date[:6], tzinfo=pytz.UTC)
                if pub_datetime < last_24_hours:
                    continue
                video_id = entry.link.split("v=")[1]
                thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                videos[channel_name].append((entry.title, entry.link, thumbnail))
        except Exception as e:
            print(f"Error fetching YouTube feed {feed_url}: {e}")
    return videos

def fetch_market_data():
    market_data = {}
    try:
        eur_usd = yf.Ticker("EURUSD=X")
        eur_usd_data = eur_usd.history(period="1d")
        market_data["EUR/USD"] = round(eur_usd_data["Close"].iloc[-1], 4) if not eur_usd_data.empty else "N/A"
    except:
        market_data["EUR/USD"] = "N/A"

    market_data["Brent Crude"] = "N/A (requires API or scraping)"

    indexes = {
        "S&P500": "^GSPC",
        "DJI": "^DJI",
        "Nasdaq": "^IXIC",
        "FTSE": "^FTSE",
        "ASE": "ASE",
    }
    for name, symbol in indexes.items():
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            market_data[name] = round(data["Close"].iloc[-1], 2) if not data.empty else "N/A"
        except:
            market_data[name] = "N/A"

    market_data["Baltic Dry Index"] = "N/A (requires API or scraping)"

    return market_data

def format_training_program_from_ics(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            calendar = Calendar(f.read())
        now = datetime.now()
        week_later = now + timedelta(days=7)
        event_html = '<section class="max-w-4xl mx-auto py-12 px-4"><h2 class="text-2xl font-bold mb-4">🏃 Πρόγραμμα Προπονήσεων</h2><ul class="list-disc list-inside text-md">'

        for e in sorted(calendar.events):
            if now.date() <= e.begin.date() <= week_later.date():
                local_date = e.begin.astimezone(pytz.timezone("Europe/Athens"))
                weekday = local_date.strftime('%A').replace("Monday", "Δευτέρα").replace("Tuesday", "Τρίτη").replace("Wednesday", "Τετάρτη").replace("Thursday", "Πέμπτη").replace("Friday", "Παρασκευή").replace("Saturday", "Σάββατο").replace("Sunday", "Κυριακή")
                date_str = local_date.strftime("%d %B").replace("May", "Μαΐου")
                event_html += f'<li><strong>{weekday} {date_str}</strong>: {e.name} - <em>{e.description or "Χωρίς περιγραφή"}</em></li>'
        event_html += '</ul></section>'
        return event_html
    except FileNotFoundError:
        return '<section class="max-w-4xl mx-auto py-12 px-4"><h2 class="text-2xl font-bold mb-4">🏃 Πρόγραμμα Προπονήσεων</h2><p>Το πρόγραμμα προπονήσεων δεν είναι διαθέσιμο αυτή τη στιγμή.</p></section>'
    except Exception as e:
        return f'<section class="max-w-4xl mx-auto py-12 px-4"><h2 class="text-2xl font-bold mb-4">🏃 Πρόγραμμα Προπονήσεων</h2><p>Σφάλμα κατά την ανάγνωση του ημερολογίου: {e}</p></section>'

def build_html():
    athens_time = datetime.now(pytz.timezone("Europe/Athens"))
    refresh_time = athens_time.strftime("%H:%M %p").lower().replace("am", "π.μ.").replace("pm", "μ.μ.")

    html = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <title>Ημερήσια Αναφορά</title>
    <script>
        function updateRefreshTime() {{
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const ampm = hours >= 12 ? 'μ.μ.' : 'π.μ.';
            const displayHours = hours % 12 || 12;
            document.getElementById("last-refresh").innerText = `Τελευταία ανανέωση σελίδας: ${displayHours}:${minutes} ${ampm}`;
        }}
    </script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body onload="updateRefreshTime()" class="bg-gray-100 text-gray-900">
    <header class="bg-gray-900 text-white py-6">
        <div class="text-center">
            <h1 class="text-3xl font-bold">Ημερήσια Αναφορά</h1>
            <p class="mt-2">Ημερήσια ενημέρωση: 05:55 π.μ. (Ώρα Ελλάδας)</p>
            <p id="last-refresh" class="mt-1">Τελευταία ανανέωση σελίδας: {refresh_time}</p>
            <button onclick="location.reload()" class="mt-4 px-4 py-2 bg-white text-gray-900 rounded hover:bg-gray-300 transition">Ανανέωση</button>
        </div>
    </header>
    <main class="py-10 px-6 max-w-6xl mx-auto">
"""

    # Συνεντεύξεις
    youtube_videos = fetch_youtube_videos()
    html += '<section class="py-6"><h2 class="text-xl font-semibold mb-4">📺 Συνεντεύξεις</h2><div class="grid grid-cols-1 md:grid-cols-3 gap-4">'
    for channel_name, _ in YOUTUBE_FEEDS[:3]:
        videos = youtube_videos.get(channel_name, [])
        html += f"""
        <div class="bg-white shadow rounded p-4">
            <h3 class="font-semibold">{channel_name}</h3>
            {"".join([f'<p class="mt-2"><a href="{link}" class="text-blue-600 hover:underline">{title}</a></p><img src="{thumbnail}" class="w-full h-40 object-cover rounded mt-2" alt="{title}">' for title, link, thumbnail in videos]) if videos else '<p>Δεν βρέθηκαν πρόσφατα βίντεο.</p>'}
        </div>
        """
    html += '</div></section>'

    # Geopolitics
    headlines = fetch_feed_links(GEOPOLITICS_FEEDS)
    thestreet_headlines = scrape_thestreet()
    additional_headlines = scrape_additional_sources()
    headlines.extend(thestreet_headlines)
    headlines.extend(additional_headlines)

    html += f"""
    <section class="py-6 bg-blue-50 rounded-lg shadow"><h2 class="text-xl font-semibold mb-2 text-blue-800">🌐 Geopolitics & International Relations</h2>
    <img src="{random_geopolitics_image()}" class="w-full rounded shadow mb-4" alt="Geopolitics Map">
    <h3 class="text-lg font-semibold mt-4 mb-2 text-blue-700">Πηγές</h3><ul class="list-disc list-inside">
    {''.join([f'<li><a href="{link}" class="text-blue-600 hover:underline">{name}</a></li>' for name, link in STATIC_GEOPOLITICS_LINKS])}
    </ul>
    <h3 class="text-lg font-semibold mt-4 mb-2 text-blue-700">Πρόσφατα Νέα (Τελευταίες 24 Ώρες)</h3><ul class="list-disc list-inside">
    {''.join(headlines) if headlines else '<li>Δεν βρέθηκαν πρόσφατα νέα για τις επιλεγμένες θεματολογίες.</li>'}
    </ul></section>"""

    # Markets
    market_img = random_market_image()
    html += f"""
    <section class="py-6"><h2 class="text-xl font-semibold mb-2">📈 Markets Summary</h2>
    <img src="{market_img}" class="w-full rounded shadow mb-4" alt="Markets Summary Image" onerror="this.onerror=null; this.parentElement.innerHTML='<p>Η εικόνα για την Αναφορά Αγορών δεν είναι διαθέσιμη.</p>';">
    </section>"""

    # Commodities / FX / Shipping
    market_data = fetch_market_data()
    html += f"""
    <section class="py-6"><h2 class="text-xl font-semibold mb-2">💱 Commodities / FX / Shipping</h2>
    <img src="{random_commodity_image()}" class="w-full rounded shadow mb-4" alt="Commodities Image">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
            <h3 class="text-lg font-semibold mb-2">FX</h3>
            <p>EUR/USD: {market_data['EUR/USD']}</p>
        </div>
        <div>
            <h3 class="text-lg font-semibold mb-2">Commodities</h3>
            <p>Brent Crude: {market_data['Brent Crude']}</p>
        </div>
        <div>
            <h3 class="text-lg font-semibold mb-2">Stock Indexes</h3>
            <p>S&P500: {market_data['S&P500']}</p>
            <p>DJI: {market_data['DJI']}</p>
            <p>Nasdaq: {market_data['Nasdaq']}</p>
            <p>FTSE: {market_data['FTSE']}</p>
            <p>ASE: {market_data['ASE']}</p>
        </div>
        <div>
            <h3 class="text-lg font-semibold mb-2">Shipping</h3>
            <p>Baltic Dry Index: {market_data['Baltic Dry Index']}</p>
        </div>
    </div>
    </section>"""

    # ΘΡΥΛΟΣ ΜΟΝΟ
    html += f"""
    <section class="py-6 bg-red-50 rounded-lg shadow"><h2 class="text-xl font-semibold mb-2 text-red-800">🔴 ⚪ ΘΡΥΛΟΣ ΜΟΝΟ</h2>
    <img src="{random_sport_image()}" class="w-full rounded shadow mb-4" alt="Olympiacos Image">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
            <h3 class="text-lg font-semibold mb-2 text-red-700">YouTube Latest Videos</h3>
            <div class="flex items-center space-x-4">
                <img src="https://www.olympiacos.org/wp-content/uploads/2023/03/mendilibar.jpg" class="w-24 h-24 rounded" alt="Mendilibar">
                <div>
                    <p><a href="{SPORTS_LINKS['SporFM 94.6 (Ολυμπιακός)']}" class="text-red-600 hover:underline">SporFM 94.6 (Ολυμπιακός)</a></p>
                    {"".join([f'<p class="mt-2"><a href="{link}" class="text-red-600 hover:underline">{title}</a></p>' for title, link, _ in youtube_videos.get("SporFM 94.6 (Ολυμπιακός)", [])])}
                </div>
            </div>
            <p class="mt-2"><a href="{SPORTS_LINKS['Red Sports 7']}" class="text-red-600 hover:underline">Red Sports 7</a></p>
            {"".join([f'<p class="mt-2"><a href="{link}" class="text-red-600 hover:underline">{title}</a></p>' for title, link, _ in youtube_videos.get("Red Sports 7", [])])}
        </div>
    </div>
    </section>"""

    # Πρόγραμμα προπονήσεων
    html += format_training_program_from_ics(os.path.join(NEWS_DIR, "full_training_plan_may2025.ics"))

    # Κλείσιμο
    html += """
    </main>
    <footer class="text-center text-gray-500 text-sm py-4 mt-8 bg-gray-200">
        © 2025 Ημερήσια Αναφορά - Ανανεώνεται καθημερινά στις 05:55 | <a href="https://github.com/Btsonbtson/NewsBrief" class="text-blue-600 hover:underline">GitHub</a>
    </footer>
</body>
</html>"""
    return html

def generate_report():
    html = build_html()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Report generated successfully at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_report()
