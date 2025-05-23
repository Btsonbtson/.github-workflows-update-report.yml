from datetime import datetime
import random

# Ημερομηνία & ώρα
now = datetime.now()
today_str = now.strftime("%A %d %B %Y")
refresh_time = "05:55"

# Τυχαία εικόνα Ολυμπιακού
olympiakos_images = [
    "https://upload.wikimedia.org/wikipedia/el/2/23/Olympiacos_FC_logo.svg",
    "https://cdn.sport-fm.gr/images/news/2024/05/01/olympiacos_goal.jpg",
    "https://www.olympiacos.org/assets/img/players/logo_fans.png"
]
selected_image = random.choice(olympiakos_images)

# Πρόγραμμα προπονήσεων
trainings = [
    ("Τρίτη 21 Μαΐου", "Bodyweight Empowerment", "Push-ups, squats, planks & burpees. 45 λεπτά"),
    ("Πέμπτη 23 Μαΐου", "Running RI 4x4'", "10.2 km/h, 1'30\" rest. 5.0 km"),
    ("Σάββατο 25 Μαΐου", "Running RE 6km", "9.3 km/h pace, last 1 km at 9.5"),
]

# HTML
html = f"""<!DOCTYPE html>
<html lang="el">
<head>
  <meta charset="UTF-8">
  <title>Ημερήσια Αναφορά</title>
  <script>
    function updateRefreshTime() {{
      const now = new Date();
      const timeStr = now.toLocaleTimeString("el-GR", {{ hour: '2-digit', minute: '2-digit' }});
      document.getElementById("lastRefresh").innerText = "Τελευταία Ενημέρωση σήμερα στις " + timeStr;
    }}
  </script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body onload="updateRefreshTime()" class="bg-gray-100 text-gray-800">

<header class="bg-gray-900 text-white text-center py-6 shadow">
  <h1 class="text-4xl font-bold">Ημερήσια Αναφορά</h1>
  <p class="text-lg">{today_str} - Ανανεώθηκε σήμερα στις {refresh_time}</p>
  <p id="lastRefresh" class="text-sm italic"></p>
  <button onclick="location.reload()" class="mt-2 bg-white text-gray-900 px-4 py-2 rounded shadow hover:bg-gray-200">Ανανέωση</button>
</header>

<main class="max-w-6xl mx-auto py-12 px-4 space-y-10">

<section>
  <h2 class="text-2xl font-bold mb-4">📺 YouTube Channels</h2>
  <ul class="list-disc list-inside space-y-2">
    <li><a href="https://www.youtube.com/@LAMBROSKALARRYTIS/videos" class="text-blue-600 hover:underline" target="_blank">Lambros Kalarrítis</a></li>
    <li><a href="https://www.youtube.com/@geostratigiki/videos" class="text-blue-600 hover:underline" target="_blank">Geostratigiki</a></li>
    <li><a href="https://www.youtube.com/@Enimerosi.kai.Skepsi/videos" class="text-blue-600 hover:underline" target="_blank">Enimerosi kai Skepsi</a></li>
  </ul>
</section>

<section class="bg-white shadow p-6 rounded">
  <h2 class="text-2xl font-bold mb-4">⚽ SporFM 94.6 (Ολυμπιακός)</h2>
  <img src="{selected_image}" alt="Olympiakos" class="w-40 mb-4">
  <ul class="list-disc list-inside">
    <li><a href="https://www.youtube.com/@sporfm946/videos" target="_blank" class="text-blue-600 hover:underline">SporFM 94.6</a></li>
    <li><a href="https://www.youtube.com/@REDSPORTS7/videos" target="_blank" class="text-blue-600 hover:underline">Red Sports 7</a></li>
  </ul>
</section>

<section>
  <h2 class="text-2xl font-bold mb-4">🌍 Geopolitics & International Relations</h2>
  <ul class="list-disc list-inside">
    <li><a href="https://www.politico.eu/" target="_blank" class="text-blue-600 hover:underline">Politico</a></li>
    <li><a href="https://www.reuters.com/" target="_blank" class="text-blue-600 hover:underline">Reuters</a></li>
    <li><a href="https://www.economist.com/" target="_blank" class="text-blue-600 hover:underline">The Economist</a></li>
    <li><a href="https://www.foreignaffairs.com/" target="_blank" class="text-blue-600 hover:underline">Foreign Affairs</a></li>
  </ul>
</section>

<section>
  <h2 class="text-2xl font-bold mb-4">📈 Commodities</h2>
  <a href="https://www.seecapitalmarkets.com/Commodities" target="_blank" class="text-blue-600 hover:underline">Δείτε τις τελευταίες τιμές Commodities</a>
</section>

<section class="bg-white shadow p-6 rounded">
  <h2 class="text-2xl font-bold mb-4">🏃 Πρόγραμμα Προπονήσεων</h2>
  <ul class="list-disc list-inside">
"""

for day, title, desc in trainings:
    html += f"<li><strong>{day}</strong>: {title} - <em>{desc}</em></li>"

html += """
  </ul>
</section>

</main>

<footer class="mt-16 bg-gray-900 text-white text-center py-6 text-sm">
  <p>© 2025 Ημερήσια Αναφορά - Ανανεώνεται καθημερινά</p>
</footer>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
