import os
import random
from datetime import datetime, timedelta
from ics import Calendar, Event
import pytz

# Ρυθμίσεις
OUTPUT_FILE = "index.html"
ATHENS_TZ = pytz.timezone("Europe/Athens")
now = datetime.now(ATHENS_TZ)
today_str = now.strftime("%A %d %B %Y")
last_update_time = now.strftime("%H:%M %p").lower()

# ----------- ΠΡΟΓΡΑΜΜΑ ΠΡΟΠΟΝΗΣΕΩΝ -------------------
running_sessions = [
    {"date": "2025-05-21", "title": "Running RHR 4x4'", "desc": "7.5+4% for 4x4', 2' rest. 3.2/4.0 km"},
    {"date": "2025-05-23", "title": "Running RI 4x4'", "desc": "10.2 km/h, 1'30\" rest. 5.0 km"},
    {"date": "2025-05-25", "title": "Running RE 6km", "desc": "9.3 km/h pace, last 1 km at 9.5"},
]
strength_dates = [
    "2025-05-22", "2025-05-24", "2025-05-26"
]

def render_schedule():
    def format_date(d):
        date_obj = datetime.strptime(d, "%Y-%m-%d")
        return date_obj.strftime("%A %d %B").replace("Monday", "Δευτέρα").replace("Tuesday", "Τρίτη")\
            .replace("Wednesday", "Τετάρτη").replace("Thursday", "Πέμπτη").replace("Friday", "Παρασκευή")\
            .replace("Saturday", "Σάββατο").replace("Sunday", "Κυριακή")

    html = '<section class="max-w-5xl mx-auto py-8 px-4">\n'
    html += '<h2 class="text-2xl font-bold mb-4 flex items-center">🏃‍♂️ Πρόγραμμα Προπονήσεων</h2>\n<ul class="list-disc ml-6 space-y-2">\n'

    for d in strength_dates:
        label = format_date(d)
        html += f"<li><strong>{label}:</strong> Ενδυνάμωση σώματος - <em>Push-ups, squats, planks & burpees</em></li>\n"

    for sess in running_sessions:
        label = format_date(sess["date"])
        html += f"<li><strong>{label}:</strong> {sess['title']} - <em>{sess['desc']}</em></li>\n"

    html += "</ul>\n</section>\n"
    return html

# ----------- ΕΙΚΟΝΕΣ -------------------
images = {
    "geopolitics": "https://www.nato.int/nato_static_fl2014/assets/pictures/2021/11/211122a-map/211122a-map-003.jpg",
    "markets": "https://www.investing.com/images/sections/market_overview_300x250.png",
    "commodities": "https://cdn.pixabay.com/photo/2016/11/18/14/50/oil-1837458_1280.jpg",
    "olympiacos": "https://media.sport24.gr/olympiacos/2022/02/olympiacos_panigirismos.jpg"
}

# ----------- HTML -------------------
html = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <title>Ημερήσια Αναφορά</title>
    <script>
        function refreshPage() {{
            window.location.reload();
        }}
    </script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 text-gray-900">

<header class="bg-gray-900 text-white text-center py-6">
    <h1 class="text-3xl font-bold">Ημερήσια Αναφορά</h1>
    <p>Τελευταία ενημέρωση σήμερα στις {last_update_time}</p>
    <button onclick="refreshPage()" class="mt-3 bg-white text-gray-800 px-4 py-1 rounded shadow hover:bg-gray-200">Ανανέωση</button>
</header>

<main class="px-4 py-6 space-y-12">
    <!-- Συνεντεύξεις -->
    <section>
        <h2 class="text-xl font-semibold mb-4">📺 Συνεντεύξεις</h2>
        <div class="grid md:grid-cols-3 gap-4">
            <div class="bg-white p-4 shadow rounded">
                <img src="https://i.ytimg.com/vi/ICGkxaFh0hI/hqdefault.jpg" alt="Lambros" class="mb-2">
                <p><strong>Lambros Kalarritis</strong><br><a class="text-blue-600" href="https://www.youtube.com/@LAMBROSKALARRYTIS/videos">Δείτε το κανάλι</a></p>
            </div>
            <div class="bg-white p-4 shadow rounded">
                <img src="https://i.ytimg.com/vi/Y45xbVOa1bc/hqdefault.jpg" alt="Geostratigiki" class="mb-2">
                <p><strong>Geostratigiki</strong><br><a class="text-blue-600" href="https://www.youtube.com/@geostratigiki/videos">Δείτε το κανάλι</a></p>
            </div>
            <div class="bg-white p-4 shadow rounded">
                <img src="https://i.ytimg.com/vi/d4RqsX4V4OY/hqdefault.jpg" alt="Skepsi" class="mb-2">
                <p><strong>Enimerosi kai Skepsi</strong><br><a class="text-blue-600" href="https://www.youtube.com/@Enimerosi.kai.Skepsi/videos">Δείτε το κανάλι</a></p>
            </div>
        </div>
    </section>

    <!-- Geopolitics -->
    <section>
        <h2 class="text-xl font-semibold mb-4">🌍 Geopolitics & International Relations</h2>
        <img src="{images['geopolitics']}" class="mb-4 rounded">
        <ul class="list-disc ml-6">
            <li><a href="https://www.politico.eu/feed/" class="text-blue-600">Politico</a></li>
            <li><a href="https://www.reuters.com/tools/rss" class="text-blue-600">Reuters</a></li>
            <li><a href="https://www.thestreet.com/feeds/rss/articles" class="text-blue-600">TheStreet</a></li>
            <li><a href="https://www.lemonde.fr/en/rss/une.xml" class="text-blue-600">LeMonde</a></li>
            <li><a href="https://www.economist.com/rss" class="text-blue-600">Economist</a></li>
            <li><a href="https://www.foreignaffairs.com/rss.xml" class="text-blue-600">Foreign Affairs</a></li>
            <li><a href="https://flight.com.gr/" class="text-blue-600">Flight.gr</a></li>
        </ul>
    </section>

    <!-- Markets -->
    <section>
        <h2 class="text-xl font-semibold mb-4">📈 Markets Summary</h2>
        <img src="{images['markets']}" class="rounded">
    </section>

    <!-- Commodities -->
    <section>
        <h2 class="text-xl font-semibold mb-4">🛢️ Commodities / FX / Shipping</h2>
        <img src="{images['commodities']}" class="rounded">
    </section>

    <!-- ΘΡΥΛΟΣ ΜΟΝΟ -->
    <section>
        <h2 class="text-xl font-semibold mb-4">🔴⚪ ΘΡΥΛΟΣ ΜΟΝΟ</h2>
        <img src="{images['olympiacos']}" class="mb-4 rounded">
        <ul class="list-disc ml-6">
            <li><a class="text-blue-600" href="https://www.youtube.com/@sporfm946/videos">SporFM 94.6 (Ολυμπιακός)</a></li>
            <li><a class="text-blue-600" href="https://www.youtube.com/@REDSPORTS7/videos">Red Sports 7</a></li>
        </ul>
    </section>

    {render_schedule()}
</main>

</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)
