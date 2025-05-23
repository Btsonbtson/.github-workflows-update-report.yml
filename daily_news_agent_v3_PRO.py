import os
from datetime import datetime
import random

# Δημιουργία HTML αρχείου
now = datetime.now()
today_str = now.strftime("%A %d %B %Y")
today_str_gr = today_str.replace("Monday", "Δευτέρα").replace("Tuesday", "Τρίτη").replace("Wednesday", "Τετάρτη") \
    .replace("Thursday", "Πέμπτη").replace("Friday", "Παρασκευή").replace("Saturday", "Σάββατο").replace("Sunday", "Κυριακή") \
    .replace("January", "Ιανουαρίου").replace("February", "Φεβρουαρίου").replace("March", "Μαρτίου").replace("April", "Απριλίου") \
    .replace("May", "Μαΐου").replace("June", "Ιουνίου").replace("July", "Ιουλίου").replace("August", "Αυγούστου") \
    .replace("September", "Σεπτεμβρίου").replace("October", "Οκτωβρίου").replace("November", "Νοεμβρίου").replace("December", "Δεκεμβρίου")

# Τυχαία εικόνα Ολυμπιακού
olympiakos_images = [
    "https://upload.wikimedia.org/wikipedia/el/2/23/Olympiacos_FC_logo.svg",
    "https://cdn.sport-fm.gr/images/news/2024/05/01/olympiacos_goal.jpg",
    "https://www.olympiacos.org/assets/img/players/logo_fans.png"
]
selected_olympiakos_image = random.choice(olympiakos_images)

# Τυχαία εικόνα για Συνεντεύξεις (YouTube)
youtube_images = [
    "https://img.youtube.com/vi/naoQ40CzmW8/hqdefault.jpg",
    "https://img.youtube.com/vi/kUgCkiGqLho/hqdefault.jpg",
    "https://img.youtube.com/vi/fUN1cw8GbXs/hqdefault.jpg",
    "https://img.youtube.com/vi/V7Q19C2MW2A/hqdefault.jpg"
]
selected_youtube_image = random.choice(youtube_images)

# Προπονήσεις (ενσωματωμένες)
training_schedule_html = """
<ul>
  <li><strong>Τρίτη 21 Μαΐου</strong>: Ενδυνάμωση σώματος - <em>Push-ups, squats, planks & burpees</em></li>
  <li><strong>Πέμπτη 23 Μαΐου</strong>: Running RI 4x4' - <em>10.2 km/h, 1'30" rest. 5.0 km</em></li>
  <li><strong>Σάββατο 25 Μαΐου</strong>: Running RE 6km - <em>9.3 km/h pace, last 1 km at 9.5</em></li>
  <li><strong>Κυριακή 26 Μαΐου</strong>: Ενδυνάμωση σώματος - <em>Push-ups, squats, planks & burpees</em></li>
</ul>
"""

# Δημιουργία αρχείου HTML
html_content = f"""<!DOCTYPE html>
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
  <p class="text-lg">{today_str_gr} - Ανανεώθηκε σήμερα στις 05:55</p>
  <p id="lastRefresh" class="text-sm italic"></p>
  <button onclick="location.reload()" class="mt-2 bg-white text-gray-900 px-4 py-2 rounded shadow hover:bg-gray-200">Ανανέωση</button>
</header>
<main class="max-w-6xl mx-auto py-12 px-4 space-y-10">
# Συνεντεύξεις Section
html_content += f"""
<section>
  <h2 class="text-2xl font-bold mb-4">🎤 Συνεντεύξεις</h2>
  <img src="{selected_youtube_image}" alt="Συνεντεύξεις" class="w-64 mb-4 rounded shadow">
  <ul class="list-disc list-inside space-y-1">
    <li><a href="https://www.youtube.com/@LAMBROSKALARRYTIS/videos" target="_blank" class="text-blue-600 hover:underline">Lambros Kalarrítis</a></li>
    <li><a href="https://www.youtube.com/@geostratigiki/videos" target="_blank" class="text-blue-600 hover:underline">Geostratigiki</a></li>
    <li><a href="https://www.youtube.com/@Enimerosi.kai.Skepsi/videos" target="_blank" class="text-blue-600 hover:underline">Ενημέρωση και Σκέψη</a></li>
  </ul>
</section>
"""

# Geopolitics Section
html_content += """
<section>
  <h2 class="text-2xl font-bold mb-4">🌍 Geopolitics & International Relations</h2>
  <ul class="list-disc list-inside space-y-1">
    <li><a href="https://www.politico.eu/" target="_blank" class="text-blue-600 hover:underline">Politico</a></li>
    <li><a href="https://www.reuters.com/" target="_blank" class="text-blue-600 hover:underline">Reuters</a></li>
    <li><a href="https://www.thestreet.com/" target="_blank" class="text-blue-600 hover:underline">TheStreet</a></li>
    <li><a href="https://www.economist.com/" target="_blank" class="text-blue-600 hover:underline">The Economist</a></li>
    <li><a href="https://www.lemonde.fr/en/" target="_blank" class="text-blue-600 hover:underline">Le Monde</a></li>
    <li><a href="https://flight.com.gr/" target="_blank" class="text-blue-600 hover:underline">Flight.gr</a></li>
  </ul>
</section>
"""

# Markets Summary
html_content += """
<section>
  <h2 class="text-2xl font-bold mb-4">📊 Top Market Summary</h2>
  <p>Δείτε όλες τις αγορές μέσω <a href="https://www.bankingnews.gr/" target="_blank" class="text-blue-600 hover:underline">bankingnews.gr</a></p>
</section>
"""

# Commodities / FX / Shipping
html_content += """
<section>
  <h2 class="text-2xl font-bold mb-4">💱 FX / Commodities / Shipping</h2>
  <ul class="list-disc list-inside space-y-1">
    <li><a href="https://www.seecapitalmarkets.com/Commodities" target="_blank" class="text-blue-600 hover:underline">Commodities Data</a></li>
    <li><a href="https://www.seecapitalmarkets.com/Forex" target="_blank" class="text-blue-600 hover:underline">FX Data</a></li>
    <li><a href="https://www.seecapitalmarkets.com/ShippingIndexes" target="_blank" class="text-blue-600 hover:underline">Shipping Indexes</a></li>
  </ul>
</section>
"""

# ΘΡΥΛΟΣ ΜΟΝΟ Section (Ολυμπιακός)
html_content += f"""
<section>
  <h2 class="text-2xl font-bold mb-4">🔴⚪ ΘΡΥΛΟΣ ΜΟΝΟ</h2>
  <img src="{selected_olympiakos_image}" alt="Ολυμπιακός" class="w-32 mb-4">
  <ul class="list-disc list-inside">
    <li><a href="https://www.youtube.com/@sporfm946/videos" target="_blank" class="text-blue-600 hover:underline">SporFM 94.6</a></li>
    <li><a href="https://www.youtube.com/@REDSPORTS7/videos" target="_blank" class="text-blue-600 hover:underline">Red Sports 7</a></li>
  </ul>
</section>
# Πρόγραμμα Προπονήσεων Section
html_content += f"""
<section>
  <h2 class="text-2xl font-bold mb-4">🏃 Πρόγραμμα Προπονήσεων</h2>
  {training_schedule_html}
</section>
"""

# Footer
html_content += """
</main>
<footer class="mt-16 bg-gray-900 text-white text-center py-6 text-sm">
  <p>© 2025 Ημερήσια Αναφορά - Ανανεώνεται καθημερινά</p>
</footer>
</body>
</html>
"""

# Αποθήκευση αρχείου HTML
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
