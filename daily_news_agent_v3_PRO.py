import datetime

# -----------------
# Daily News Agent v3 PRO for GitHub Pages
# -----------------

# Get today's date formatted for Greek
today = datetime.datetime.now().strftime('%A %d %B %Y')

# Create the HTML content (pure static with placeholders)
html_content = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ημερήσια Ενημέρωση</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-serif text-gray-900">
    <header class="bg-gray-800 text-white py-10 text-center">
        <h1 class="text-4xl font-extrabold">Ημερήσιο Δελτίο</h1>
        <p class="mt-2 text-xl">{today}</p>
    </header>

    <main class="max-w-7xl mx-auto py-10 px-4 grid grid-cols-1 lg:grid-cols-2 gap-8">

        <section>
            <h2 class="text-3xl font-bold border-b-4 border-black mb-4">Geopolitics & International Relations</h2>
            <img src="https://www.defence-point.gr/wp-content/uploads/2023/10/geopolitics.jpg" alt="Geopolitics" class="rounded-lg shadow mb-4">
            <ul class="list-disc pl-5">
                <li><a href="https://www.defence-point.gr/news/" class="text-blue-700 hover:underline">Defence Point</a></li>
                <li><a href="https://nordicmonitor.com/" class="text-blue-700 hover:underline">Nordic Monitor</a></li>
            </ul>
        </section>

        <section>
            <h2 class="text-3xl font-bold border-b-4 border-black mb-4">Shipping Indexes</h2>
            <img src="https://seecapitalmarkets.com/logo.png" alt="Shipping Index" class="rounded-lg shadow mb-4">
            <a href="https://seecapitalmarkets.com/ShippingIndexes" class="text-blue-700 hover:underline">Δείτε τον πίνακα Shipping Indexes</a>
        </section>

        <section>
            <h2 class="text-3xl font-bold border-b-4 border-black mb-4">Markets Summary</h2>
            <img src="https://www.bankingnews.gr/themes/bankingnews/images/logo.png" alt="Markets" class="rounded-lg shadow mb-4">
            <a href="https://www.bankingnews.gr/" class="text-blue-700 hover:underline">Bankingnews.gr - Πλήρης αγορά</a>
        </section>

        <section>
            <h2 class="text-3xl font-bold border-b-4 border-black mb-4">Commodities</h2>
            <img src="https://seecapitalmarkets.com/logo.png" alt="Commodities" class="rounded-lg shadow mb-4">
            <a href="https://seecapitalmarkets.com/Commodities" class="text-blue-700 hover:underline">Δείτε τον πίνακα Commodities</a>
        </section>

        <section>
            <h2 class="text-3xl font-bold border-b-4 border-black mb-4">Sports</h2>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Olympiakos_Piraeus_logo.svg/1200px-Olympiakos_Piraeus_logo.svg.png" alt="Olympiacos" class="rounded-lg shadow mb-4">
            <ul class="list-disc pl-5">
                <li><a href="https://www.youtube.com/@sporfm946/videos" class="text-blue-700 hover:underline">SporFM 94.6 - Ολυμπιακός</a></li>
                <li><a href="https://www.youtube.com/@REDSPORTS7/videos" class="text-blue-700 hover:underline">Red Sports 7</a></li>
            </ul>
        </section>

        <section>
            <h2 class="text-3xl font-bold border-b-4 border-black mb-4">YouTube Latest Videos</h2>
            <ul class="list-disc pl-5">
                <li><a href="https://www.youtube.com/@LAMBROSKALARRYTIS/videos" class="text-blue-700 hover:underline">Lambros Kalarritis</a></li>
                <li><a href="https://www.youtube.com/@geostratigiki/videos" class="text-blue-700 hover:underline">Geostratigiki</a></li>
                <li><a href="https://www.youtube.com/@Enimerosi.kai.Skepsi/videos" class="text-blue-700 hover:underline">Enimerosi kai Skepsi</a></li>
            </ul>
        </section>

    </main>

    <footer class="bg-gray-800 text-white text-center py-6 mt-10">
        &copy; 2025 Ημερήσιο Δελτίο
    </footer>
</body>
</html>
"""

# Save as index.html (overwrite)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
