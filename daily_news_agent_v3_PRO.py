from datetime import datetime
import random

# Ημερομηνία στα ελληνικά
months = {
    1: "Ιανουαρίου", 2: "Φεβρουαρίου", 3: "Μαρτίου",
    4: "Απριλίου", 5: "Μαΐου", 6: "Ιουνίου",
    7: "Ιουλίου", 8: "Αυγούστου", 9: "Σεπτεμβρίου",
    10: "Οκτωβρίου", 11: "Νοεμβρίου", 12: "Δεκεμβρίου"
}
weekdays = {
    0: "Δευτέρα", 1: "Τρίτη", 2: "Τετάρτη",
    3: "Πέμπτη", 4: "Παρασκευή", 5: "Σάββατο", 6: "Κυριακή"
}
now = datetime.now()
today_gr = f"{weekdays[now.weekday()]} {now.day} {months[now.month]} {now.year}"

# Ώρα προκαθορισμένη
refresh_hour = "05:55"

# Random Olympiakos image
olympiakos_images = [
    "https://upload.wikimedia.org/wikipedia/el/2/23/Olympiacos_FC_logo.svg",
    "https://www.olympiacos.org/wp-content/uploads/2023/05/OlympiacosTeam.jpg",
    "https://pbs.twimg.com/media/FtLZWguXgAEjs0D.jpg"
]
olympiakos_image = random.choice(olympiakos_images)

# Δημιουργία HTML
html_content = f"""
<!DOCTYPE html>
<html lang="el">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ημερήσια Αναφορά</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    function updateTime() {{
      const now = new Date();
      const hh = String(now.getHours()).padStart(2, '0');
      const mm = String(now.getMinutes()).padStart(2, '0');
      document.getElementById("refresh-time").innerText = "Τελευταία Ενημέρωση σήμερα στις " + hh + ":" + mm;
    }}
  </script>
</head>
<body class="bg-gray-100 text-gray-900">

<header class="bg-gray-900 text-white py-10 text-center">
  <h1 class="text-4xl font-bold">Ημερήσια Αναφορά</h1>
  <p id="refresh-time" class="text-xl mt-2">{today_gr} - Ανανεώθηκε σήμερα στις {refresh_hour}</p>
  <button onclick="updateTime()" class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded">Ανανέωση</button>
</header>

<main class="max-w-6xl mx-auto py-12 px-4 grid grid-cols-1 md:grid-cols-2 gap-8">

  <section class="bg-white shadow-md rounded-lg p-6">
    <h2 class="text-3xl font-bold mb-6">🌍 Geopolitics & International Relations</h2>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Political_World_Map.jpg/800px-Political_World_Map.jpg" class="w-full mb-4 rounded-lg" alt="Geopolitics">
    <ul class="list-disc list-inside">
      <li><a href="https://www.politico.eu/feed/" target="_blank" class="text-blue-600 hover:underline">Politico</a></li>
      <li><a href="https://www.reuters.com/tools/rss" target="_blank" class="text-blue-600 hover:underline">Reuters</a></li>
      <li><a href="https://www.thestreet.com/feeds/rss/articles" target="_blank" class="text-blue-600 hover:underline">The Street</a></li>
      <li><a href="https://www.lemonde.fr/en/rss" target="_blank" class="text-blue-600 hover:underline">Le Monde</a></li>
      <li><a href="https://www.economist.com/rss" target="_blank" class="text-blue-600 hover:underline">The Economist</a></li>
      <li><a href="https://www.rednews.gr/feed/" target="_blank" class="text-blue-600 hover:underline">Rednews.gr</a></li>
      <li><a href="https://www.foreignaffairs.com/rss.xml" target="_blank" class="text-blue-600 hover:underline">Foreign Affairs</a></li>
    </ul>
  </section>
  
<section class="bg-white shadow-md rounded-lg p-6 mt-10">
  <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">💪</span>Πρόγραμμα Προπονήσεων</h2>
  <ul class="list-disc list-inside">
    <li class="mb-2">
      <strong>Τρίτη 21/05 18:00:</strong> Bodyweight Empowerment<br>
      <span class="text-sm text-gray-700">Push-ups, squats ​:contentReference[oaicite:0]{index=0}​

  <section class="bg-white shadow-md rounded-lg p-6">
    <h2 class="text-3xl font-bold mb-6">📺 YouTube Latest Videos</h2>
    <ul class="list-disc list-inside">
      <li><a href="https://www.youtube.com/@LAMBROSKALARRYTIS/videos" class="text-blue-600 hover:underline" target="_blank">Lambros Kalarritis</a></li>
      <li><a href="https://www.youtube.com/@geostratigiki/videos" class="text-blue-600 hover:underline" target="_blank">Geostratigiki</a></li>
      <li><a href="https://www.youtube.com/@Enimerosi.kai.Skepsi/videos" class="text-blue-600 hover:underline" target="_blank">Enimerosi kai Skepsi</a></li>
    </ul>
  </section>

  <section class="bg-white shadow-md rounded-lg p-6">
    <h2 class="text-3xl font-bold mb-6">⚽ Sports - Ολυμπιακός</h2>
    <img src="{olympiakos_image}" class="w-full mb-4 rounded-lg" alt="Olympiacos">
    <ul class="list-disc list-inside">
      <li><a href="https://www.youtube.com/@sporfm946/videos" class="text-blue-600 hover:underline" target="_blank">SporFM 94.6</a></li>
      <li><a href="https://www.youtube.com/@REDSPORTS7/videos" class="text-blue-600 hover:underline" target="_blank">Red Sports 7</a></li>
    </ul>
  </section>

  <section class="bg-white shadow-md rounded-lg p-6">
    <h2 class="text-3xl font-bold mb-6">📈 Top Market Summary</h2>
    <a href="https://www.bankingnews.gr/" class="text-blue-600 hover:underline" target="_blank">Δείτε τα τελευταία δεδομένα στο Bankingnews.gr</a>
  </section>

  <section class="bg-white shadow-md rounded-lg p-6">
    <h2 class="text-3xl font-bold mb-6">🚢 Shipping Indexes</h2>
    <a href="https://www.seecapitalmarkets.com/ShippingIndexes" target="_blank" class="text-blue-600 hover:underline">Δείτε τα τελευταία Shipping Indexes</a>
  </section>

  <section class="bg-white shadow-md rounded-lg p-6">
    <h2 class="text-3xl font-bold mb-6">💰 Commodities & Forex</h2>
    <a href="https://www.seecapitalmarkets.com/Commodities" target="_blank" class="text-blue-600 hover:underline">Commodities</a> |
    <a href="https://www.seecapitalmarkets.com/Forex" target="_blank" class="text-blue-600 hover:underline">Forex</a>
  </section>

</main>

<footer class="bg-gray-900 text-white py-8 text-center mt-10">
  <p>© 2025 Ημερήσια Αναφορά - GitHub Auto Update 05:55</p>
</footer>

</body>
</html>
"""

# Αποθήκευση του αρχείου
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Το αρχείο index.html δημιουργήθηκε επιτυχώς.")
