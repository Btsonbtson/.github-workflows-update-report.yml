import datetime
import random

# Λίστα με static εικόνες Ολυμπιακού (ποδόσφαιρο σχετικές)
OLYMPIAKOS_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/el/2/23/Olympiacos_FC_logo.svg",
    "https://www.olympiacos.org/wp-content/uploads/2020/10/fans-red-white.jpg",
    "https://media.gazzetta.gr/sites/default/files/styles/article_main/public/2022-11/olympiacos-celebration.jpg",
    "https://www.iefimerida.gr/sites/default/files/styles/in_article/public/2023-05/olympiakos-podosfairo.jpg"
]

# Επιλογή τυχαίας εικόνας
olympiakos_image = random.choice(OLYMPIAKOS_IMAGES)

# Στατικές πηγές για Geopolitics RSS backup mode
GEOPOLITICS_SOURCES = [
    ("Politico Europe", "https://www.politico.eu/feed/"),
    ("Reuters", "https://www.reuters.com/tools/rss"),
    ("The Street", "https://www.thestreet.com/feeds/rss/articles"),
    ("Le Monde", "https://www.lemonde.fr/en/rss"),
    ("The Economist", "https://www.economist.com/rss"),
    ("Rednews.gr", "https://www.rednews.gr/feed/"),
    ("Foreign Affairs", "https://www.foreignaffairs.com/rss.xml"),
]

# Τρέχουσα ημερομηνία για εμφάνιση στο header
today = datetime.datetime.now().strftime('%A %d %B %Y')

# Δημιουργία του HTML με Newspaper-style αισθητική
html_content = f"""
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ημερήσιο Δελτίο</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        // Δυναμική εμφάνιση ώρας τελευταίου refresh με κάθε ανανέωση browser
        window.onload = function() {{
            document.getElementById('refresh-time').innerText = new Date().toLocaleTimeString('el-GR') + ' ' + new Date().toLocaleDateString('el-GR');
        }};
    </script>
</head>
<body class="bg-gray-100 text-gray-900">

    <!-- Header -->
    <header class="bg-gray-900 text-white py-8 text-center">
        <h1 class="text-4xl font-bold">Ημερήσιο Δελτίο</h1>
        <p class="text-xl mt-2">Ημερομηνία Έκδοσης: {today}</p>
        <p class="text-lg mt-1">Τελευταίο Refresh: <span id="refresh-time"></span></p>
    </header>

    <main class="max-w-7xl mx-auto py-12 px-4 grid grid-cols-1 md:grid-cols-2 gap-8">

        <!-- Geopolitics Section -->
        <section class="bg-white shadow-md rounded-lg p-6">
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">🌍</span>Geopolitics & International Relations</h2>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Political_World_Map.jpg/800px-Political_World_Map.jpg" alt="Geopolitics Map" class="w-full mb-6 rounded-lg">
            <ul class="list-disc list-inside">
"""

# Εισαγωγή των στατικών πηγών geopolitics
for name, url in GEOPOLITICS_SOURCES:
    html_content += f'<li><a href="{url}" target="_blank" class="text-blue-600 hover:underline">{name}</a></li>\n'

html_content += """
            </ul>
        </section>

        <!-- Sports Section with dynamic Olympiakos image -->
        <section class="bg-white shadow-md rounded-lg p-6">
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">⚽</span>Sports - Ολυμπιακός</h2>
            <img src="{olympiakos_image}" alt="Olympiacos" class="w-full mb-6 rounded-lg">
            <ul class="list-disc list-inside">
                <li><a href="https://www.youtube.com/@sporfm946/videos" target="_blank" class="text-blue-600 hover:underline">SporFM 94.6 - Ολυμπιακός</a></li>
                <li><a href="https://www.youtube.com/@REDSPORTS7/videos" target="_blank" class="text-blue-600 hover:underline">Red Sports 7</a></li>
            </ul>
        </section>

        <!-- YouTube Latest Videos Section -->
        <section class="bg-white shadow-md rounded-lg p-6">
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">📺</span>YouTube Latest Videos</h2>
            <ul class="list-disc list-inside">
                <li><a href="https://www.youtube.com/@LAMBROSKALARRYTIS/videos" target="_blank" class="text-blue-600 hover:underline">Lambros Kalarritis</a></li>
                <li><a href="https://www.youtube.com/@geostratigiki/videos" target="_blank" class="text-blue-600 hover:underline">Geostratigiki</a></li>
                <li><a href="https://www.youtube.com/@Enimerosi.kai.Skepsi/videos" target="_blank" class="text-blue-600 hover:underline">Enimerosi kai Skepsi</a></li>
            </ul>
        </section>

        <!-- Markets Section -->
        <section class="bg-white shadow-md rounded-lg p-6">
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">📈</span>Top Market Summary</h2>
            <a href="https://www.bankingnews.gr/" target="_blank" class="text-blue-600 hover:underline">Bankingnews.gr - Δείτε τα τελευταία δεδομένα εδώ</a>
        </section>
html_content += """
        <!-- Shipping Indexes Section -->
        <section class="bg-white shadow-md rounded-lg p-6">
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">🚢</span>Shipping Indexes Daily Values</h2>
            <a href="https://www.seecapitalmarkets.com/ShippingIndexes" target="_blank" class="text-blue-600 hover:underline">Δείτε τα τελευταία Shipping Indexes</a>
        </section>

        <!-- Commodities Section -->
        <section class="bg-white shadow-md rounded-lg p-6">
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">💰</span>Commodities & Forex</h2>
            <a href="https://www.seecapitalmarkets.com/Commodities" target="_blank" class="text-blue-600 hover:underline">Δείτε Commodities</a> |
            <a href="https://www.seecapitalmarkets.com/Forex" target="_blank" class="text-blue-600 hover:underline">Δείτε Forex</a>
        </section>

    </main>

    <!-- Footer -->
    <footer class="mt-16 bg-gray-900 text-white py-8 text-center">
        <p>© 2025 Ημερήσια Αναφορά - Ανανεώνεται καθημερινά μέσω GitHub Actions</p>
    </footer>

</body>
</html>
"""

# Αποθήκευση αρχείου index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
