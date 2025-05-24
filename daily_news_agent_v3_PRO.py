import os
import feedparser
import requests
import random
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from ics import Calendar

NEWS_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(NEWS_DIR, "index.html")

# --- Ρυθμίσεις πηγών ---
GEOPOLITICS_FEEDS = [
    'https://www.politico.eu/feed/',
    'https://www.reuters.com/tools/rss',
    'https://www.thestreet.com/feeds/rss/articles',
    'https://www.lemonde.fr/en/rss/une.xml',
    'https://www.economist.com/rss',
    'https://www.foreignaffairs.com/rss.xml',
    'https://www.rednews.gr/feed/'
]

STATIC_GEOPOLITICS_LINKS = [
    ("Politico", "https://www.politico.eu/"),
    ("Reuters", "https://www.reuters.com/"),
    ("TheStreet", "https://www.thestreet.com/"),
    ("LeMonde", "https://www.lemonde.fr/en/"),
    ("Economist", "https://www.economist.com/"),
    ("Foreign Affairs", "https://www.foreignaffairs.com/"),
    ("Flight.gr", "https://flight.com.gr/")
]

SPORT_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/el/2/23/Olympiacos_FC_logo.svg",
    "https://www.olympiacos.org/wp-content/uploads/2023/02/omada2023.jpg",
    "https://media.sport24.gr/pictures/1200x675crop/2023/10/19/olympiakos-podosfairo.jpg"
]

YOUTUBE_CHANNELS = [
    ("Lambros Kalarritis", "https://www.youtube.com/@LAMBROSKALARRYTIS", "https://img.youtube.com/vi/TdU4ErvYv0I/0.jpg"),
    ("Geostratigiki", "https://www.youtube.com/@geostratigiki", "https://img.youtube.com/vi/Iynb0ZkKHAs/0.jpg"),
    ("Enimerosi kai Skepsi", "https://www.youtube.com/@Enimerosi.kai.Skepsi", "https://img.youtube.com/vi/XiXPo3Eq0Jk/0.jpg")
]

SPORTS_LINKS = {
    'SporFM 94.6 (Ολυμπιακός)': 'https://www.sport-fm.gr/',
    'Red Sports 7': 'https://www.redsports7.gr/'
}

MARKET_IMAGES = [
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3",
    "https://images.unsplash.com/photo-1590283603385-17d352d74a38",
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3"
]

COMMODITY_IMAGES = [
    "https://images.unsplash.com/photo-1590283603385-17d352d74a38",
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3",
    "https://images.unsplash.com/photo-1590283603385-17d352d74a38"
]

def random_interview_image():
    return random.choice([channel[2] for channel in YOUTUBE_CHANNELS])

def random_market_image():
    return random.choice(MARKET_IMAGES)

def random_commodity_image():
    return random.choice(COMMODITY_IMAGES)

def random_sport_image():
    return random.choice(SPORT_IMAGES)

def fetch_feed_links(urls, max_items=4):
    headlines = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_items]:
                headlines.append(f'<li><a href="{entry.link}" target="_blank">{entry.title}</a></li>')
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")
            continue
    return headlines

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
        return "<p>Σφάλμα: Το αρχείο ημερολογίου δεν βρέθηκε.</p>"
    except Exception as e:
        return f"<p>Σφάλμα κατά την ανάγνωση του ημερολογίου: {e}</p>"

def build_html():
    athens_time = datetime.now(pytz.timezone("Europe/Athens"))
    refresh_time = athens_time.strftime("%H:%M %p").lower().replace("am", "π.μ.").replace("pm", "μ.μ.")
    today_date = athens_time.strftime("%A %d %B %Y").replace("Monday", "Δευτέρα").replace("Tuesday", "Τρίτη").replace("Wednesday", "Τετάρτη").replace("Thursday", "Πέμπτη").replace("Friday", "Παρασκευή").replace("Saturday", "Σάββατο").replace("Sunday", "Κυριακή").replace("May", "Μαΐου")

    html = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <title>Ημερήσια Αναφορά</title>
    <script>
        function updateTime() {{
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            document.getElementById("last-refresh").innerText = `Τελευταία ενημέρωση σήμερα στις ${hours}:${minutes}`;
        }}
    </script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body onload="updateTime()" class="bg-gray-100 text-gray-900">
    <header class="bg-gray-900 text-white py-6">
        <div class="text-center">
            <h1 class="text-3xl font-bold">Ημερήσια Αναφορά</h1>
            <p id="last-refresh" class="mt-2">Τελευταία ενημέρωση σήμερα στις {refresh_time}</p>
            <button onclick="location.reload()" class="mt-4 px-4 py-2 bg-white text-gray-900 rounded hover:bg-gray-300 transition">Ανανέωση</button>
        </div>
    </header>
    <main class="py-10 px-6 max-w-6xl mx-auto">
"""

    # Συνεντεύξεις
    html += '<section class="py-6"><h2 class="text-xl font-semibold mb-4">📺 Συνεντεύξεις</h2><div class="grid grid-cols-1 md:grid-cols-3 gap-4">'
    for name, link, img in YOUTUBE_CHANNELS:
        html += f"""
        <div class="bg-white shadow rounded p-4">
            <img src="{img}" alt="{name}" class="w-full h-40 object-cover rounded mb-2">
            <p class="font-semibold">{name}</p>
            <a href="{link}" class="text-blue-600 hover:underline text-sm">Δείτε το κανάλι</a>
        </div>
        """
    html += '</div></section>'

    # Geopolitics
    html += '<section class="py-6"><h2 class="text-xl font-semibold mb-2">🌐 Geopolitics & International Relations</h2><ul class="list-disc list-inside">'
    for name, link in STATIC_GEOPOLITICS_LINKS:
        html += f'<li><a href="{link}" class="text-blue-600 hover:underline">{name}</a></li>'
    html += '</ul>'
    
    # RSS Headlines
    headlines = fetch_feed_links(GEOPOLITICS_FEEDS)
    html += '<h3 class="text-lg font-semibold mt-4 mb-2">Πρόσφατα Νέα</h3><ul class="list-disc list-inside">'
    html += ''.join(headlines) if headlines else '<li>Δεν βρέθηκαν πρόσφατα νέα.</li>'
    html += '</ul></section>'

    # Markets
    html += f"""
    <section class="py-6"><h2 class="text-xl font-semibold mb-2">📈 Markets Summary</h2>
    <img src="{random_market_image()}" class="w-full rounded shadow">
    </section>"""

    # Commodities
    html += f"""
    <section class="py-6"><h2 class="text-xl font-semibold mb-2">💱 Commodities / FX / Shipping</h2>
    <img src="{random_commodity_image()}" class="w-full rounded shadow">
    </section>"""

    # ΘΡΥΛΟΣ ΜΟΝΟ
    html += f"""
    <section class="py-6"><h2 class="text-xl font-semibold mb-2">🔴 ⚪ ΘΡΥΛΟΣ ΜΟΝΟ</h2>
    <img src="{random_sport_image()}" class="w-full rounded shadow mb-2">
    <ul class="list-disc list-inside text-sm">
        <li><a href="{SPORTS_LINKS['SporFM 94.6 (Ολυμπιακός)']}" class="text-blue-600 hover:underline">SporFM 94.6 (Ολυμπιακός)</a></li>
        <li><a href="{SPORTS_LINKS['Red Sports 7']}" class="text-blue-600 hover:underline">Red Sports 7</a></li>
    </ul>
    </section>"""

    # Πρόγραμμα προπονήσεων
    html += format_training_program_from_ics(os.path.join(NEWS_DIR, "full_training_plan_may2025.ics"))

    # Κλείσιμο
    html += """
    </main>
    <footer class="text-center text-gray-500 text-sm py-4 mt-8">
        © 2025 Ημερήσια Αναφορά - Ανανεώνεται καθημερινά στις 05:55
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
