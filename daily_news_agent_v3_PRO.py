from datetime import datetime

# Get today's date in Greek format
today = datetime.now().strftime('%A %d %B %Y')

# Generate the HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ημερήσια Ενημέρωση</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-900">

    <!-- Header -->
    <header class="bg-gray-900 text-white py-8 text-center">
        <h1 class="text-4xl font-bold">Ημερήσια Αναφορά</h1>
        <p class="mt-2 text-lg">{today} - Ανανεώνεται καθημερινά στις 05:55</p>
    </header>

    <main class="max-w-7xl mx-auto py-12 px-4 grid grid-cols-1 md:grid-cols-2 gap-8">
        <section>
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">🌍</span>Geopolitics & International Relations</h2>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Political_World_Map.jpg/800px-Political_World_Map.jpg" alt="Geopolitics Map" class="w-full mb-6 rounded-lg">
            <ul class="list-disc list-inside">
                <li><a href="https://www.defence-point.gr/news/" target="_blank" class="text-blue-600 hover:underline">Defence Point</a></li>
                <li><a href="https://elisme.gr/" target="_blank" class="text-blue-600 hover:underline">Elisme</a></li>
                <li><a href="https://nordicmonitor.com/" target="_blank" class="text-blue-600 hover:underline">Nordic Monitor</a></li>
                <li><a href="https://foreignaffairs.com/" target="_blank" class="text-blue-600 hover:underline">Foreign Affairs</a></li>
            </ul>
        </section>

        <section>
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">📈</span>Markets Summary</h2>
            <img src="https://www.bankingnews.gr/themes/bankingnews/images/logo.png" alt="Markets" class="w-full mb-6 rounded-lg">
            <a href="https://www.bankingnews.gr/" target="_blank" class="text-blue-600 hover:underline">Bankingnews.gr - Πλήρης αγορά</a>
        </section>

        <section>
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">🚢</span>Shipping Indexes</h2>
            <img src="https://seecapitalmarkets.com/assets/logo.png" alt="Shipping Index" class="w-full mb-6 rounded-lg">
            <a href="https://seecapitalmarkets.com/ShippingIndexes" target="_blank" class="text-blue-600 hover:underline">Δείτε τον πίνακα Shipping Indexes</a>
        </section>

        <section>
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">💰</span>Commodities & Forex</h2>
            <img src="https://seecapitalmarkets.com/assets/logo.png" alt="Commodities" class="w-full mb-6 rounded-lg">
            <a href="https://www.seecapitalmarkets.com/Commodities" target="_blank" class="text-blue-600 hover:underline">Δείτε Commodities</a> |
            <a href="https://www.seecapitalmarkets.com/Forex" target="_blank" class="text-blue-600 hover:underline">Δείτε Forex</a>
        </section>

        <section>
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">⚽</span>Sports</h2>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Olympiakos_Piraeus_logo.svg/1200px-Olympiakos_Piraeus_logo.svg.png" alt="Olympiacos" class="w-full mb-6 rounded-lg">
            <ul class="list-disc list-inside">
                <li><a href="https://www.youtube.com/@sporfm946/videos" target="_blank" class="text-blue-600 hover:underline">SporFM 94.6 - Ολυμπιακός</a></li>
                <li><a href="https://www.youtube.com/@REDSPORTS7/videos" target="_blank" class="text-blue-600 hover:underline">Red Sports 7</a></li>
            </ul>
        </section>

        <section>
            <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">📺</span>YouTube Latest Videos</h2>
            <ul class="list-disc list-inside">
                <li><a href="https://www.youtube.com/@LAMBROSKALARRYTIS/videos" target="_blank" class="text-blue-600 hover:underline">Lambros Kalarritis</a></li>
                <li><a href="https://www.youtube.com/@geostratigiki/videos" target="_blank" class="text-blue-600 hover:underline">Geostratigiki</a></li>
                <li><a href="https://www.youtube.com/@Enimerosi.kai.Skepsi/videos" target="_blank" class="text-blue-600 hover:underline">Enimerosi kai Skepsi</a></li>
            </ul>
        </section>
    </main>

    <footer class="mt-16 bg-gray-900 text-white py-8 text-center">
        <p>© 2025 Ημερήσια Αναφορά - Ανανεώνεται καθημερινά μέσω GitHub Actions</p>
    </footer>
</body>
</html>
"""

# Save as index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
