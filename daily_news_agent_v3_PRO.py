import feedparser
import random
from datetime import datetime, timedelta
from pathlib import Path
import os

# Προετοιμασία ημερομηνίας
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
greek_date = now.strftime("Παρασκευή %d Μαΐου %Y")
refresh_time = "05:55"
report_title = f"Ημερήσια Αναφορά"
header_line = f"{greek_date} - Ανανεώθηκε σήμερα στις {refresh_time}"

# Στατικές πηγές (fallback)
geopolitics_sources = [
    ("Defence Point", "https://www.defence-point.gr/news/"),
    ("Elisme", "https://elisme.gr/"),
    ("Nordic Monitor", "https://nordicmonitor.com/"),
    ("Foreign Affairs", "https://foreignaffairs.com/")
]

# Εικόνες Ολυμπιακού
olympiakos_images = [
    "https://upload.wikimedia.org/wikipedia/el/2/23/Olympiacos_FC_logo.svg",
    "https://cdn.sport-fm.gr/images/news/2024/05/01/olympiacos_goal.jpg",
    "https://www.olympiacos.org/assets/img/players/logo_fans.png"
]
olympiakos_image_url = random.choice(olympiakos_images)

# YouTube Sections
youtube_links = {
    "Lambros Kalarrítis": "https://www.youtube.com/@LAMBROSKALARRYTIS/videos",
    "Geostratigiki": "https://www.youtube.com/@geostratigiki/videos",
    "Enimerosi kai Skepsi": "https://www.youtube.com/@Enimerosi.kai.Skepsi/videos",
}

sports_youtube_links = {
    "SporFM 94.6 (Ολυμπιακός)": "https://www.youtube.com/@sporfm946/videos",
    "Red Sports 7": "https://www.youtube.com/@REDSPORTS7/videos",
}

# Δεδομένα από ημερολόγιο προπονήσεων
training_sessions = [
    ("Τρίτη 21 Μαΐου", "Ενδυνάμωση σώματος", "Push-ups, squats, planks & burpees."),
    ("Τετάρτη 22 Μαΐου", "Ενδυνάμωση σώματος", "Push-ups, squats, planks & burpees."),
    ("Πέμπτη 23 Μαΐου", "Running RHR 4x4'", "7.5+4% for 4x4', 2' rest. 3.2/4.0 km"),
    ("Παρασκευή 24 Μαΐου", "Ενδυνάμωση σώματος", "Push-ups, squats, planks & burpees."),
    ("Σάββατο 25 Μαΐου", "Running RE 6km", "9.3 km/h pace, last 1 km at 9.5."),
    ("Κυριακή 26 Μαΐου", "Ενδυνάμωση σώματος", "Push-ups, squats, planks & burpees."),
]

# HTML αρχείο
html = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <title>{report_title}</title>
    <script>
        function updateTimestamp() {{
            const now = new Date();
            const timeStr = now.toLocaleTimeString("el-GR", {{ hour: '2-digit', minute: '2-digit' }});
            document.getElementById("lastUpdate").textContent = "Τελευταία ενημέρωση σήμερα στις " + timeStr;
        }}
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans leading-normal tracking-normal">

<!-- Header -->
<header class="bg-gray-900 text-white py-6 text-center">
    <h1 class="text-4xl font-bold">{report_title}</h1>
    <p id="lastUpdate" class="text-lg mt-2">{header_line}</p>
    <button onclick="updateTimestamp()" class="mt-4 bg-white text-gray-900 px-4 py-2 rounded shadow hover:bg-gray-200">Ανανέωση</button>
</header>

<!-- YouTube Latest Videos -->
<section class="max-w-6xl mx-auto py-12 px-4">
    <h2 class="text-2xl font-bold mb-6">📺 YouTube Latest Videos</h2>
    <div class="grid md:grid-cols-3 gap-6">
"""
for name, link in youtube_links.items():
    html += f"""
        <div class="bg-white p-4 shadow-md rounded-lg">
            <h3 class="text-lg font-semibold">{name}</h3>
            <a href="{link}" target="_blank" class="text-blue-600 hover:underline">Δείτε το κανάλι</a>
        </div>
    """

html += f"""
    </div>
</section>

<!-- Sports Section -->
<section class="max-w-6xl mx-auto py-12 px-4 bg-white shadow-md rounded-lg">
    <h2 class="text-2xl font-bold mb-6">⚽ SporFM 94.6 (Ολυμπιακός)</h2>
    <img src="{olympiakos_image_url}" alt="Olympiacos" class="w-32 mb-4 rounded">
    <ul class="list-disc list-inside">
"""
for name, link in sports_youtube_links.items():
    html += f'<li><a href="{link}" class="text-blue-600 hover:underline" target="_blank">{name}</a></li>'
html += "</ul></section>"

# Geopolitics
html += """
<section class="max-w-6xl mx-auto py-12 px-4">
    <h2 class="text-2xl font-bold mb-6">🌍 Geopolitics & International Relations</h2>
    <ul class="list-disc list-inside">
"""
for name, url in geopolitics_sources:
    html += f'<li><a href="{url}" target="_blank" class="text-blue-600 hover:underline">{name}</a></li>'
html += "</ul></section>"

# Προπονήσεις
html += """
<section class="max-w-6xl mx-auto py-12 px-4 bg-white shadow-md rounded-lg">
    <h2 class="text-2xl font-bold mb-6">🏃 Πρόγραμμα Προπονήσεων</h2>
    <ul class="list-disc list-inside">
"""
for day, title, desc in training_sessions:
    html += f'<li><strong>{day}</strong>: {title} - <em>{desc}</em></li>'
html += "</ul></section>"

# Footer
html += """
<footer class="mt-12 bg-gray-900 text-white text-center py-6">
    <p>© 2025 Ημερήσια Αναφορά - Powered by GPT & GitHub Actions</p>
</footer>
</body></html>
"""

# Αποθήκευση
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
