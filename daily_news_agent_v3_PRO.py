import os
import feedparser
import requests
import random
import pytz
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from ics import Calendar
import time

# Directory setup
NEWS_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(NEWS_DIR, "index.html")

# Data sources
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
    "https://tradingeconomics.com/charts/sp-500.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Stock_market_indices_graph_%28August_2023%29.png/800px-Stock_market_indices_graph_%28August_2023%29.png",
]

COMMODITY_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Oil_prices_1970-2017.png/800px-Oil_prices_1970-2017.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Shipping_containers_at_Port_of_Singapore.jpg/800px-Shipping_containers_at_Port_of_Singapore.jpg",
]

TRAINING_IMAGES = [
    "https://images.unsplash.com/photo-1517836357463-d25dfead9741?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
]

# Enhanced keywords for better filtering
TOPIC_KEYWORDS = {
    "Ελληνο-Τουρκικές Σχέσεις": ["Greece", "Turkey", "Greek", "Turkish", "Ελληνο-Τουρκικές", "Ελλάδα", "Τουρκία", "Aegean", "Cyprus", "Κύπρος", "Erdogan", "Mitsotakis"],
    "Γεωπολιτική": ["Geopolitics", "Geopolitical", "Γεωπολιτική", "NATO", "EU", "Middle East", "Russia", "China", "Ukraine", "Putin", "Biden", "Trump"],
    "Διεθνείς Σχέσεις": ["International Relations", "Diplomacy", "Διεθνείς Σχέσεις", "Foreign Policy", "United Nations", "UN Security Council", "G7", "G20"],
    "Οικονομία": ["Economy", "Economic", "Markets", "Stock", "Euro", "Dollar", "Inflation", "GDP", "ECB", "Fed"],
    "Άμυνα": ["Defense", "Defence", "Military", "Army", "Navy", "Air Force", "Weapons", "Security", "Άμυνα", "Στρατός"]
}

def random_image(image_list):
    return random.choice(image_list)

def get_athens_time():
    """Get current Athens time"""
    return datetime.now(pytz.timezone("Europe/Athens"))

def get_time_ago(pub_datetime):
    """Calculate how long ago an article was published"""
    now = datetime.now(pytz.UTC)
    diff = now - pub_datetime
    
    if diff.days > 0:
        return f"{diff.days} ημέρ{'α' if diff.days == 1 else 'ες'} πριν"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} ώρ{'α' if hours == 1 else 'ες'} πριν"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} λεπτ{'ό' if minutes == 1 else 'ά'} πριν"
    else:
        return "μόλις τώρα"

def fetch_feed_links(urls, max_items=6):
    """Enhanced feed fetching with better categorization and timestamps"""
    articles = []
    now = datetime.now(pytz.UTC)
    last_48_hours = now - timedelta(hours=48)  # Extended to 48 hours for more content

    for url in urls:
        try:
            print(f"Fetching feed: {url}")
            feed = feedparser.parse(url)
            if not feed.entries:
                print(f"No entries found for feed: {url}")
                continue
                
            for entry in feed.entries[:max_items]:
                pub_date = entry.get('published_parsed') or entry.get('updated_parsed')
                if not pub_date:
                    continue
                    
                pub_datetime = datetime(*pub_date[:6], tzinfo=pytz.UTC)
                if pub_datetime < last_48_hours:
                    continue

                title = entry.title.lower()
                summary = entry.get('summary', '').lower()
                
                # Categorize article
                category = "Γενικά"
                priority = 3
                for topic, keywords in TOPIC_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword.lower() in title or keyword.lower() in summary:
                            category = topic
                            if topic in ["Ελληνο-Τουρκικές Σχέσεις", "Γεωπολιτική"]:
                                priority = 1
                            elif topic in ["Διεθνείς Σχέσεις", "Άμυνα"]:
                                priority = 2
                            break
                    if category != "Γενικά":
                        break

                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'category': category,
                    'priority': priority,
                    'time_ago': get_time_ago(pub_datetime),
                    'source': url.split('/')[2].replace('www.', '').split('.')[0].title()
                })
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")
            continue
    
    # Sort by priority and then by time
    articles.sort(key=lambda x: (x['priority'], x['title']))
    return articles[:12]  # Return top 12 articles

def scrape_thestreet():
    """Enhanced TheStreet scraping"""
    articles = []
    url = "https://www.thestreet.com/markets"
    
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        soup = BeautifulSoup(response.text, 'html.parser')
        article_elements = soup.find_all('a', class_='news-listing__title', limit=6)

        for article in article_elements:
            title = article.text.strip()
            link = "https://www.thestreet.com" + article['href']
            
            # Check if relevant to our topics
            for topic, keywords in TOPIC_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in title.lower():
                        articles.append({
                            'title': title,
                            'link': link,
                            'category': topic,
                            'priority': 2,
                            'time_ago': 'πρόσφατα',
                            'source': 'TheStreet'
                        })
                        break
                if articles and articles[-1]['title'] == title:
                    break
    except Exception as e:
        print(f"Error scraping TheStreet: {e}")
    return articles

def fetch_youtube_videos():
    """Enhanced YouTube video fetching"""
    videos = {}
    now = datetime.now(pytz.UTC)
    last_48_hours = now - timedelta(hours=48)

    for channel_name, feed_url in YOUTUBE_FEEDS:
        try:
            print(f"Fetching YouTube feed: {channel_name}")
            feed = feedparser.parse(feed_url)
            if not feed.entries:
                continue
                
            videos[channel_name] = []
            for entry in feed.entries[:4]:  # Get more videos
                pub_date = entry.get('published_parsed')
                if not pub_date:
                    continue
                    
                pub_datetime = datetime(*pub_date[:6], tzinfo=pytz.UTC)
                if pub_datetime < last_48_hours:
                    continue
                    
                video_id = entry.link.split("v=")[1].split("&")[0]
                thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                
                videos[channel_name].append({
                    'title': entry.title,
                    'link': entry.link,
                    'thumbnail': thumbnail,
                    'time_ago': get_time_ago(pub_datetime)
                })
        except Exception as e:
            print(f"Error fetching YouTube feed {feed_url}: {e}")
    return videos

def fetch_market_data():
    """Enhanced market data fetching with error handling"""
    market_data = {}
    
    # Currency pairs
    currencies = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "USDJPY=X"
    }
    
    for name, symbol in currencies.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if not hist.empty:
                current = hist["Close"].iloc[-1]
                previous = hist["Close"].iloc[-2] if len(hist) > 1 else current
                change = ((current - previous) / previous) * 100
                market_data[name] = {
                    'value': round(current, 4),
                    'change': round(change, 2)
                }
            else:
                market_data[name] = {'value': 'N/A', 'change': 0}
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            market_data[name] = {'value': 'N/A', 'change': 0}

    # Stock indexes
    indexes = {
        "S&P 500": "^GSPC",
        "Dow Jones": "^DJI",
        "NASDAQ": "^IXIC",
        "FTSE 100": "^FTSE",
        "Athens Exchange": "^ATHEX"  # Greek market
    }
    
    for name, symbol in indexes.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if not hist.empty:
                current = hist["Close"].iloc[-1]
                previous = hist["Close"].iloc[-2] if len(hist) > 1 else current
                change = ((current - previous) / previous) * 100
                market_data[name] = {
                    'value': round(current, 2),
                    'change': round(change, 2)
                }
            else:
                market_data[name] = {'value': 'N/A', 'change': 0}
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            market_data[name] = {'value': 'N/A', 'change': 0}

    # Commodities
    commodities = {
        "Crude Oil": "CL=F",
        "Gold": "GC=F",
        "Natural Gas": "NG=F"
    }
    
    for name, symbol in commodities.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if not hist.empty:
                current = hist["Close"].iloc[-1]
                previous = hist["Close"].iloc[-2] if len(hist) > 1 else current
                change = ((current - previous) / previous) * 100
                market_data[name] = {
                    'value': round(current, 2),
                    'change': round(change, 2)
                }
            else:
                market_data[name] = {'value': 'N/A', 'change': 0}
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            market_data[name] = {'value': 'N/A', 'change': 0}

    return market_data

def format_training_program_from_ics(file_path):
    """Enhanced training program formatting"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            calendar = Calendar(f.read())
        
        now = get_athens_time()
        week_later = now + timedelta(days=7)
        event_html = '<div class="space-y-3">'

        events = []
        for e in calendar.events:
            if now.date() <= e.begin.date() <= week_later.date():
                local_date = e.begin.astimezone(pytz.timezone("Europe/Athens"))
                events.append((local_date, e))
        
        events.sort(key=lambda x: x[0])
        
        for local_date, e in events:
            weekday = local_date.strftime('%A').replace(
                "Monday", "Δευτέρα").replace("Tuesday", "Τρίτη").replace(
                "Wednesday", "Τετάρτη").replace("Thursday", "Πέμπτη").replace(
                "Friday", "Παρασκευή").replace("Saturday", "Σάββατο").replace(
                "Sunday", "Κυριακή")
            
            date_str = local_date.strftime("%d %B").replace(
                "January", "Ιανουαρίου").replace("February", "Φεβρουαρίου").replace(
                "March", "Μαρτίου").replace("April", "Απριλίου").replace(
                "May", "Μαΐου").replace("June", "Ιουνίου").replace(
                "July", "Ιουλίου").replace("August", "Αυγούστου").replace(
                "September", "Σεπτεμβρίου").replace("October", "Οκτωβρίου").replace(
                "November", "Νοεμβρίου").replace("December", "Δεκεμβρίου")
            
            # Determine if it's today
            is_today = local_date.date() == now.date()
            highlight_class = "bg-blue-100 border-l-4 border-blue-500 pl-4" if is_today else "bg-gray-50 border-l-4 border-gray-300 pl-4"
            
            event_html += f'''
            <div class="{highlight_class} p-3 rounded">
                <div class="flex justify-between items-start">
                    <div>
                        <h4 class="font-semibold text-gray-900">{weekday} {date_str}</h4>
                        <p class="text-lg text-gray-800 mt-1">{e.name}</p>
                        <p class="text-sm text-gray-600 mt-1">{e.description or "Χωρίς περιγραφή"}</p>
                    </div>
                    {'<span class="bg-blue-500 text-white px-2 py-1 rounded text-xs">ΣΗΜΕΡΑ</span>' if is_today else ''}
                </div>
            </div>
            '''
        
        event_html += '</div>'
        return event_html
        
    except FileNotFoundError:
        # Enhanced fallback static schedule
        now = get_athens_time()
        event_html = '<div class="space-y-3">'
        
        training_days = [
            ("Σάββατο 24 Μαΐου", "Ενδυνάμωση σώματος", "Push-ups, squats, planks & burpees - 3 sets"),
            ("Κυριακή 25 Μαΐου", "Running RI 4x4'", "10.2 km/h, 1'30\" rest intervals - 5.0 km συνολικά"),
            ("Δευτέρα 26 Μαΐου", "Running RE 6km", "9.3 km/h pace, τελευταίο 1 km στα 9.5 km/h"),
            ("Τρίτη 27 Μαΐου", "Ενδυνάμωση σώματος", "Push-ups, squats, planks & burpees - 3 sets"),
            ("Τετάρτη 28 Μαΐου", "Ανάκαμψη", "Stretching και light cardio - 30 λεπτά"),
            ("Πέμπτη 29 Μαΐου", "Running Tempo", "8 km στα 9.0 km/h με 2x1km intervals"),
            ("Παρασκευή 30 Μαΐου", "Rest Day", "Πλήρης ανάπαυση ή ελαφρύ περπάτημα")
        ]
        
        for i, (day, workout, details) in enumerate(training_days):
            is_today = i == 0  # Assuming first day is today for demo
            highlight_class = "bg-blue-100 border-l-4 border-blue-500 pl-4" if is_today else "bg-gray-50 border-l-4 border-gray-300 pl-4"
            
            event_html += f'''
            <div class="{highlight_class} p-3 rounded">
                <div class="flex justify-between items-start">
                    <div>
                        <h4 class="font-semibold text-gray-900">{day}</h4>
                        <p class="text-lg text-gray-800 mt-1">{workout}</p>
                        <p class="text-sm text-gray-600 mt-1">{details}</p>
                    </div>
                    {'<span class="bg-blue-500 text-white px-2 py-1 rounded text-xs">ΣΗΜΕΡΑ</span>' if is_today else ''}
                </div>
            </div>
            '''
        
        event_html += '</div>'
        return event_html
        
    except Exception as e:
        return f'<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded"><p>Σφάλμα κατά την ανάγνωση του ημερολογίου: {e}</p></div>'

def build_html():
    """Enhanced HTML generation with professional news layout"""
    athens_time = get_athens_time()
    today_str = athens_time.strftime("%A %d %B %Y").replace(
        "Monday", "Δευτέρα").replace("Tuesday", "Τρίτη").replace(
        "Wednesday", "Τετάρτη").replace("Thursday", "Πέμπτη").replace(
        "Friday", "Παρασκευή").replace("Saturday", "Σάββατο").replace(
        "Sunday", "Κυριακή").replace("January", "Ιανουαρίου").replace(
        "February", "Φεβρουαρίου").replace("March", "Μαρτίου").replace(
        "April", "Απριλίου").replace("May", "Μαΐου").replace(
        "June", "Ιουνίου").replace("July", "Ιουλίου").replace(
        "August", "Αυγούστου").replace("September", "Σεπτεμβρίου").replace(
        "October", "Οκτωβρίου").replace("November", "Νοεμβρίου").replace(
        "December", "Δεκεμβρίου")
    
    current_time = athens_time.strftime("%H:%M")
    
    html = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ημερήσια Αναφορά - {today_str}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .breaking-news {{ animation: pulse 2s infinite; }}
        .market-up {{ color: #10B981; }}
        .market-down {{ color: #EF4444; }}
        .news-card:hover {{ transform: translateY(-2px); transition: transform 0.2s; }}
        .section-divider {{ background: linear-gradient(90deg, #1F2937 0%, #3B82F6 50%, #1F2937 100%); height: 2px; }}
    </style>
    <script>
        function updateTime() {{
            const now = new Date();
            const options = {{ 
                timeZone: 'Europe/Athens', 
                hour: '2-digit', 
                minute: '2-digit',
                second: '2-digit'
            }};
            const timeStr = now.toLocaleTimeString('el-GR', options);
            document.getElementById('current-time').textContent = timeStr;
        }}
        
        function refreshPage() {{
            location.reload();
        }}
        
        setInterval(updateTime, 1000);
        window.onload = function() {{
            updateTime();
        }};
    </script>
</head>
<body class="bg-gray-50 text-gray-900 font-sans">
    <!-- Header -->
    <header class="bg-gradient-to-r from-gray-900 via-blue-900 to-gray-900 text-white shadow-lg">
        <div class="container mx-auto px-6 py-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-4xl font-bold mb-2">📰 ΗΜΕΡΗΣΙΑ ΑΝΑΦΟΡΑ</h1>
                    <p class="text-xl text-blue-200">{today_str}</p>
                </div>
                <div class="text-right">
                    <div class="text-3xl font-mono" id="current-time">{current_time}</div>
                    <p class="text-sm text-blue-200 mt-1">Ώρα Ελλάδας</p>
                    <button onclick="refreshPage()" class="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition duration-200">
                        <i class="fas fa-sync-alt mr-2"></i>Ανανέωση
                    </button>
                </div>
            </div>
        </div>
        <div class="section-divider"></div>
    </header>

    <main class="container mx-auto px-6 py-8 space-y-12">
"""

    # Breaking News / Top Stories
    print("Fetching geopolitics news...")
    articles = fetch_feed_links(GEOPOLITICS_FEEDS)
    thestreet_articles = scrape_thestreet()
    articles.extend(thestreet_articles)
    
    # Sort articles by priority
    top_stories = [a for a in articles if a['priority'] == 1][:3]
    
    if top_stories:
        html += '''
        <section class="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg shadow">
            <h2 class="text-2xl font-bold text-red-800 mb-4">
                <i class="fas fa-exclamation-triangle mr-2"></i>ΚΥΡΙΕΣ ΕΙΔΗΣΕΙΣ
            </h2>
            <div class="grid gap-4">
        '''
        
        for story in top_stories:
            html += f'''
            <div class="bg-white p-4 rounded-lg shadow news-card border-l-4 border-red-400">
                <div class="flex justify-between items-start mb-2">
                    <span class="bg-red-500 text-white px-2 py-1 rounded text-xs font-semibold">{story['category']}</span>
                    <span class="text-xs text-gray-500">{story['time_ago']} • {story['source']}</span>
                </div>
                <h3 class="text-lg font-semibold text-gray-900 mb-2">
                    <a href="{story['link']}" target="_blank" class="hover:text-blue-600 transition">{story['title']}</a>
                </h3>
            </div>
            '''
        
        html += '</div></section>'

    # Geopolitics & International Relations
    html += f'''
    <section class="bg-white rounded-lg shadow-lg p-6">
        <div class="flex items-center mb-6">
            <i class="fas fa-globe text-3xl text-blue-600 mr-4"></i>
            <h2 class="text-3xl font-bold text-gray-900">Γεωπολιτική & Διεθνείς Σχέσεις</h2>
        </div>
        
        <img src="{random_image(GEOPOLITICS_IMAGES)}" class="w-full h-64 object-cover rounded-lg shadow-md mb-6" alt="Geopolitics">
        
        <div class="grid md:grid-cols-2 gap-8">
            <div>
                <h3 class="text-xl font-semibold mb-4 text-blue-800">
                    <i class="fas fa-link mr-2"></i>Πηγές Ενημέρωσης
                </h3>
                <div class="grid grid-cols-2 gap-2">
    '''
    
    for name, link in STATIC_GEOPOLITICS_LINKS:
        html += f'<a href="{link}" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm p-2 bg-blue-50 rounded hover:bg-blue-100 transition">{name}</a>'
    
    html += '''
                </div>
            </div>
            <div>
                <h3 class="text-xl font-semibold mb-4 text-blue-800">
                    <i class="fas fa-clock mr-2"></i>Πρόσφατα Νέα
                </h3>
                <div class="space-y-3">
    '''
    
    # Display categorized articles
    other_articles = [a for a in articles if a['priority'] > 1][:8]
    if other_articles:
        for article in other_articles:
            priority_color = "bg-yellow-100 text-yellow-800" if article['priority'] == 2 else "bg-gray-100 text-gray-800"
            html += f'''
            <div class="border-l-4 border-blue-300 pl-4 py-2">
                <div class="flex justify-between items-start mb-1">
                    <span class="{priority_color} px-2 py-1 rounded text-xs">{article['category']}</span>
                    <span class="text-xs text-gray-500">{article['time_ago']}</span>
                </div>
                <a href="{article['link']}" target="_blank" class="text-gray-900 hover:text-blue-600 font-medium transition">
                    {article['title']}
                </a>
            </div>
            '''
    else:
        html += '<p class="text-gray-600 italic">Δεν βρέθηκαν πρόσφατα νέα.</p>'
    
    html += '''
                </div>
            </div>
        </div>
    </section>
    '''

    # Markets Section
    print("Fetching market data...")
    market_data = fetch_market_data()
    
    html += f'''
    <section class="bg-white rounded-lg shadow-lg p-6">
        <div class="flex items-center mb-6">
            <i class="fas fa-chart-line text-3xl text-green-600 mr-4"></i>
            <h2 class="text-3xl font-bold text-gray-900">Χρηματιστήρια & Αγορές</h2>
        </div>
        
        <img src="{random_image(MARKET_IMAGES)}" class="w-full h-64 object-cover rounded-lg shadow-md mb-6" alt="Stock Market">
        
        <div class="grid md:grid-cols-3 gap-6">
            <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-4 text-blue-800">
                    <i class="fas fa-exchange-alt mr-2"></i>Συναλλάγματα
                </h3>
    '''
    
    currencies = ["EUR/USD", "GBP/USD", "USD/JPY"]
    for currency in currencies:
        if currency in market_data:
            data = market_data[currency]
            change_class = "market-up" if data['change'] > 0 else "market-down" if data['change'] < 0 else "text-gray-600"
            change_icon = "↗" if data['change'] > 0 else "↘" if data['change'] < 0 else "→"
            html += f'''
            <div class="flex justify-between items-center py-2 border-b border-blue-200 last:border-b-0">
                <span class="font-medium">{currency}</span>
                <div class="text-right">
                    <div class="font-semibold">{data['value']}</div>
                    <div class="{change_class} text-sm">{change_icon} {data['change']:+.2f}%</div>
                </div>
            </div>
            '''
    
    html += '''
            </div>
            <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-4 text-green-800">
                    <i class="fas fa-chart-bar mr-2"></i>Χρηματιστήρια
                </h3>
    '''
    
    indexes = ["S&P 500", "Dow Jones", "NASDAQ", "FTSE 100", "Athens Exchange"]
    for index in indexes:
        if index in market_data:
            data = market_data[index]
            change_class = "market-up" if data['change'] > 0 else "market-down" if data['change'] < 0 else "text-gray-600"
            change_icon = "↗" if data['change'] > 0 else "↘" if data['change'] < 0 else "→"
            html += f'''
            <div class="flex justify-between items-center py-2 border-b border-green-200 last:border-b-0">
                <span class="font-medium text-sm">{index}</span>
                <div class="text-right">
                    <div class="font-semibold text-sm">{data['value']}</div>
                    <div class="{change_class} text-xs">{change_icon} {data['change']:+.2f}%</div>
                </div>
            </div>
            '''
    
    html += '''
            </div>
            <div class="bg-yellow-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-4 text-yellow-800">
                    <i class="fas fa-oil-can mr-2"></i>Εμπορεύματα
                </h3>
    '''
    
    commodities = ["Crude Oil", "Gold", "Natural Gas"]
    for commodity in commodities:
        if commodity in market_data:
            data = market_data[commodity]
            change_class = "market-up" if data['change'] > 0 else "market-down" if data['change'] < 0 else "text-gray-600"
            change_icon = "↗" if data['change'] > 0 else "↘" if data['change'] < 0 else "→"
            unit = "$" if commodity == "Crude Oil" else "$" if commodity == "Gold" else "$"
            html += f'''
            <div class="flex justify-between items-center py-2 border-b border-yellow-200 last:border-b-0">
                <span class="font-medium text-sm">{commodity}</span>
                <div class="text-right">
                    <div class="font-semibold text-sm">{unit}{data['value']}</div>
                    <div class="{change_class} text-xs">{change_icon} {data['change']:+.2f}%</div>
                </div>
            </div>
            '''
    
    html += '''
            </div>
        </div>
        <div class="mt-4 text-center">
            <a href="https://www.bankingnews.gr/" target="_blank" class="text-blue-600 hover:text-blue-800 font-medium">
                <i class="fas fa-external-link-alt mr-2"></i>Περισσότερα στο BankingNews.gr
            </a>
        </div>
    </section>
    '''

    # YouTube Videos / Interviews
    print("Fetching YouTube videos...")
    youtube_videos = fetch_youtube_videos()
    
    html += '''
    <section class="bg-white rounded-lg shadow-lg p-6">
        <div class="flex items-center mb-6">
            <i class="fab fa-youtube text-3xl text-red-600 mr-4"></i>
            <h2 class="text-3xl font-bold text-gray-900">Συνεντεύξεις & Αναλύσεις</h2>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
    '''
    
    for channel_name, _ in YOUTUBE_FEEDS[:6]:  # Show more channels
        videos = youtube_videos.get(channel_name, [])
        if videos:
            latest_video = videos[0]
            html += f'''
            <div class="bg-gray-50 rounded-lg overflow-hidden shadow news-card">
                <img src="{latest_video['thumbnail']}" class="w-full h-48 object-cover" alt="{channel_name}">
                <div class="p-4">
                    <h3 class="font-semibold text-red-700 mb-2">{channel_name}</h3>
                    <a href="{latest_video['link']}" target="_blank" class="text-gray-900 hover:text-red-600 font-medium line-clamp-2 transition">
                        {latest_video['title'][:100]}{'...' if len(latest_video['title']) > 100 else ''}
                    </a>
                    <p class="text-xs text-gray-500 mt-2">{latest_video['time_ago']}</p>
            '''
            
            # Show additional videos if available
            if len(videos) > 1:
                html += '<div class="mt-3 space-y-1">'
                for video in videos[1:3]:  # Show 2 more videos
                    html += f'''
                    <a href="{video['link']}" target="_blank" class="block text-sm text-gray-600 hover:text-red-600 transition truncate">
                        • {video['title'][:60]}{'...' if len(video['title']) > 60 else ''}
                    </a>
                    '''
                html += '</div>'
            
            html += '''
                </div>
            </div>
            '''
        else:
            # Fallback for channels without recent videos
            html += f'''
            <div class="bg-gray-50 rounded-lg p-4 shadow">
                <h3 class="font-semibold text-red-700 mb-2">{channel_name}</h3>
                <p class="text-gray-600 text-sm">Δεν βρέθηκαν πρόσφατα βίντεο</p>
                <div class="mt-2">
                    <i class="fas fa-play-circle text-red-500 mr-2"></i>
                    <span class="text-sm text-gray-500">Ελέγξτε αργότερα</span>
                </div>
            </div>
            '''
    
    html += '</div></section>'

    # ΘΡΥΛΟΣ ΜΟΝΟ (Olympiacos Section)
    html += f'''
    <section class="bg-gradient-to-r from-red-50 to-white rounded-lg shadow-lg p-6 border-l-4 border-red-500">
        <div class="flex items-center mb-6">
            <div class="bg-red-600 p-3 rounded-full mr-4">
                <i class="fas fa-futbol text-white text-2xl"></i>
            </div>
            <h2 class="text-3xl font-bold text-red-800">🔴 ⚪ ΘΡΥΛΟΣ ΜΟΝΟ</h2>
        </div>
        
        <img src="{random_image(SPORT_IMAGES)}" class="w-full h-64 object-cover rounded-lg shadow-md mb-6" alt="Olympiacos">
        
        <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-white p-4 rounded-lg shadow">
                <h3 class="text-lg font-semibold mb-4 text-red-700">
                    <i class="fas fa-video mr-2"></i>Πρόσφατα Βίντεο
                </h3>
    '''
    
    # Sports YouTube content
    sports_channels = ["SporFM 94.6 (Ολυμπιακός)", "Red Sports 7"]
    for channel in sports_channels:
        if channel in youtube_videos and youtube_videos[channel]:
            html += f'''
            <div class="border-b border-gray-200 pb-3 mb-3 last:border-b-0">
                <h4 class="font-medium text-red-600 mb-2">{channel}</h4>
            '''
            for video in youtube_videos[channel][:2]:
                html += f'''
                <a href="{video['link']}" target="_blank" class="block text-sm text-gray-800 hover:text-red-600 mb-1 transition">
                    • {video['title'][:80]}{'...' if len(video['title']) > 80 else ''}
                </a>
                '''
            html += '</div>'
        else:
            html += f'''
            <div class="border-b border-gray-200 pb-3 mb-3">
                <h4 class="font-medium text-red-600 mb-2">{channel}</h4>
                <p class="text-sm text-gray-500">Δεν βρέθηκαν πρόσφατα βίντεο</p>
            </div>
            '''
    
    html += '''
            </div>
            <div class="bg-white p-4 rounded-lg shadow">
                <h3 class="text-lg font-semibold mb-4 text-red-700">
                    <i class="fas fa-link mr-2"></i>Χρήσιμοι Σύνδεσμοι
                </h3>
                <div class="space-y-2">
    '''
    
    for name, link in SPORTS_LINKS.items():
        html += f'''
        <a href="{link}" target="_blank" class="block bg-red-50 hover:bg-red-100 p-3 rounded transition">
            <i class="fas fa-external-link-alt text-red-500 mr-2"></i>
            <span class="text-red-700 font-medium">{name}</span>
        </a>
        '''
    
    html += '''
                </div>
            </div>
        </div>
    </section>
    '''

    # Training Program
    html += f'''
    <section class="bg-white rounded-lg shadow-lg p-6">
        <div class="flex items-center mb-6">
            <i class="fas fa-dumbbell text-3xl text-purple-600 mr-4"></i>
            <h2 class="text-3xl font-bold text-gray-900">Πρόγραμμα Προπονήσεων</h2>
        </div>
        
        <img src="{random_image(TRAINING_IMAGES)}" class="w-full h-64 object-cover rounded-lg shadow-md mb-6" alt="Training">
        
        <div class="bg-purple-50 p-6 rounded-lg">
            <h3 class="text-xl font-semibold mb-4 text-purple-800">
                <i class="fas fa-calendar-week mr-2"></i>Εβδομαδιαίο Πρόγραμμα
            </h3>
            {format_training_program_from_ics(os.path.join(NEWS_DIR, "full_training_plan_may2025.ics"))}
        </div>
        
        <div class="mt-6 grid md:grid-cols-3 gap-4 text-center">
            <div class="bg-green-50 p-4 rounded-lg">
                <i class="fas fa-heartbeat text-green-600 text-2xl mb-2"></i>
                <h4 class="font-semibold text-green-800">Καρδιαγγειακή</h4>
                <p class="text-sm text-green-700">3x/εβδομάδα</p>
            </div>
            <div class="bg-blue-50 p-4 rounded-lg">
                <i class="fas fa-muscle text-blue-600 text-2xl mb-2"></i>
                <h4 class="font-semibold text-blue-800">Ενδυνάμωση</h4>
                <p class="text-sm text-blue-700">2x/εβδομάδα</p>
            </div>
            <div class="bg-yellow-50 p-4 rounded-lg">
                <i class="fas fa-spa text-yellow-600 text-2xl mb-2"></i>
                <h4 class="font-semibold text-yellow-800">Ανάκαμψη</h4>
                <p class="text-sm text-yellow-700">2x/εβδομάδα</p>
            </div>
        </div>
    </section>
    '''

    # Footer
    current_timestamp = athens_time.strftime("%d/%m/%Y %H:%M:%S")
    html += f'''
    </main>
    
    <footer class="bg-gray-900 text-white py-8 mt-12">
        <div class="container mx-auto px-6">
            <div class="grid md:grid-cols-3 gap-6">
                <div>
                    <h3 class="text-lg font-semibold mb-3">Ημερήσια Αναφορά</h3>
                    <p class="text-gray-400 text-sm">Αυτοματοποιημένη συλλογή και παρουσίαση ειδήσεων, αγορών και προγραμμάτων.</p>
                </div>
                <div>
                    <h3 class="text-lg font-semibold mb-3">Τελευταία Ενημέρωση</h3>
                    <p class="text-blue-400">{current_timestamp}</p>
                    <p class="text-gray-400 text-sm mt-1">Αυτόματη ανανέωση κάθε ώρα</p>
                </div>
                <div>
                    <h3 class="text-lg font-semibold mb-3">Πηγές</h3>
                    <p class="text-gray-400 text-sm">Reuters, Politico, Le Monde, Economist, YouTube Feeds</p>
                    <a href="https://github.com/Btsonbtson/NewsBrief" target="_blank" class="text-blue-400 hover:text-blue-300 text-sm mt-2 inline-block">
                        <i class="fab fa-github mr-2"></i>GitHub Repository
                    </a>
                </div>
            </div>
            <div class="section-divider mt-6 mb-4"></div>
            <div class="text-center">
                <p class="text-gray-400 text-sm">© 2025 Ημερήσια Αναφορά - Powered by Python & RSS Feeds</p>
            </div>
        </div>
    </footer>
    
    <!-- Auto-refresh script -->
    <script>
        // Auto-refresh every hour
        setTimeout(function() {{
            location.reload();
        }}, 3600000); // 1 hour
        
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>'''
    
    return html

def generate_report():
    """Generate the complete daily report"""
    print("🚀 Generating Daily Report...")
    print(f"⏰ Current Athens Time: {get_athens_time().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        html = build_html()
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        
        file_size = os.path.getsize(OUTPUT_FILE) / 1024  # KB
        print(f"✅ Report generated successfully!")
        print(f"📁 File: {OUTPUT_FILE}")
        print(f"📊 Size: {file_size:.1f} KB")
        print(f"🌐 Open in browser: file://{os.path.abspath(OUTPUT_FILE)}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        raise

if __name__ == "__main__":
    generate_report()
