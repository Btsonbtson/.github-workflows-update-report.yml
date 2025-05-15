# -*- coding: utf-8 -*-
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

NEWS_DIR = '.'
OUTPUT_FILE = f"{NEWS_DIR}/index.html"

# Πηγές RSS
RSS_SOURCES = {
    "Geopolitics": [
        {"name": "Defence Point", "url": "https://www.defence-point.gr/news/feed"},
        {"name": "Nordic Monitor", "url": "https://nordicmonitor.com/feed/"},
    ],
    "Markets": [
        {"name": "Bankingnews.gr", "url": "https://www.bankingnews.gr/rss"},
    ],
    "Commodities": [
        {"name": "Commodities Table", "url": "https://www.seecapitalmarkets.com/Commodities"},
    ]
}

# YouTube video pages
YOUTUBE_LINKS = [
    {"name": "Lambros Kalarritis", "url": "https://www.youtube.com/@LAMBROSKALARRYTIS/videos"},
    {"name": "Geostratigiki", "url": "https://www.youtube.com/@geostratigiki/videos"},
    {"name": "Enimerosi kai Skepsi", "url": "https://www.youtube.com/@Enimerosi.kai.Skepsi/videos"},
    {"name": "SporFM 94.6", "url": "https://www.youtube.com/@sporfm946/videos"},
    {"name": "RedSports 7", "url": "https://www.youtube.com/@REDSPORTS7/videos"},
]

# Images per section
SECTION_IMAGES = {
    "Geopolitics": "https://www.defence-point.gr/wp-content/uploads/2021/11/defence-point-banner.jpg",
    "Markets": "https://www.bankingnews.gr/assets/bn.png",
    "Commodities": "https://seecapitalmarkets.com/images/logo.png",
    "Shipping": "https://seecapitalmarkets.com/images/logo.png",
    "Sports": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Olympiacos_CFP_logo.svg",
}


def fetch_rss_section(title, feeds):
    section_html = f'<section><h2>{title}</h2>'
    section_html += f'<img src="{SECTION_IMAGES.get(title, "")}" class="mb-4 rounded shadow" width="600"/>'
    for feed in feeds:
        try:
            d = feedparser.parse(feed["url"])
            if d.entries:
                section_html += f'<h3 class="mt-4">{feed["name"]}</h3><ul>'
                for entry in d.entries[:5]:
                    image_tag = ''
                    if 'media_content' in entry:
                        image = entry.media_content[0]['url']
                        image_tag = f'<img src="{image}" width="300" class="mb-2 rounded"/>'
                    section_html += f'<li>{image_tag}<a href="{entry.link}" target="_blank">{entry.title}</a></li>'
                section_html += '</ul>'
        except Exception as e:
            section_html += f"<p>Σφάλμα ανάκτησης από {feed['name']}</p>"
    section_html += '</section>'
    return section_html


def fetch_youtube_section():
    section_html = '<section><h2>YouTube Latest Videos</h2><div class="grid grid-cols-2 md:grid-cols-4 gap-4">'
    for yt in YOUTUBE_LINKS:
        section_html += f'''
        <div class="rounded shadow p-2 bg-white">
            <img src="https://img.youtube.com/vi/naoQ40CzmW8/0.jpg" class="rounded mb-2"/>
            <a href="{yt['url']}" target="_blank" class="font-bold">{yt["name"]}</a>
        </div>
        '''
    section_html += '</div></section>'
    return section_html


def generate_html():
    today = datetime.now().strftime("%A %d %B %Y")
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Daily Report</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 text-gray-900">
        <header class="bg-gray-800 text-white p-8 text-center">
            <h1 class="text-4xl font-bold">Ημερήσιο Δελτίο</h1>
            <p class="text-lg">Ημερομηνία: {today}</p>
        </header>
        <main class="max-w-7xl mx-auto p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
            {fetch_rss_section("Geopolitics", RSS_SOURCES["Geopolitics"])}
            {fetch_rss_section("Markets", RSS_SOURCES["Markets"])}
            {fetch_rss_section("Commodities", RSS_SOURCES["Commodities"])}
            {fetch_youtube_section()}
        </main>
    </body>
    </html>
    '''
    return html


if __name__ == "__main__":
    content = generate_html()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[✔] Το report αποθηκεύτηκε ως {OUTPUT_FILE}")
