from datetime import datetime
import random

def generate_report():
    today = datetime.now().strftime("%A %d %B %Y")
    refresh_time = "05:55"
    olympiakos_images = [
        "https://upload.wikimedia.org/wikipedia/en/thumb/6/64/Olympiacos_FC.svg/1200px-Olympiacos_FC.svg.png",
        "https://www.olympiacos.org/wp-content/uploads/2022/10/Olympiakos-team.jpg",
        "https://img.uefa.com/imgml/TP/teams/logos/140x140/52280.png"
    ]
    olympiakos_image = random.choice(olympiakos_images)

    training_section = """
    <section class="bg-white shadow-md rounded-lg p-6 mt-10">
      <h2 class="text-3xl font-bold mb-6 flex items-center"><span class="mr-3">💪</span>Πρόγραμμα Προπονήσεων</h2>
      <ul class="list-disc list-inside">
        <li class="mb-2">
          <strong>Τρίτη 21/05 18:00:</strong> Bodyweight Empowerment<br>
          <span class="text-sm text-gray-700">Push-ups, squats, planks & burpees. 45 λεπτά.</span>
        </li>
        <li class="mb-2">
          <strong>Πέμπτη 23/05 18:30:</strong> Running RI 4x4'<br>
          <span class="text-sm text-gray-700">10.2 km/h, 1'30" rest. 5.0 km</span>
        </li>
        <li class="mb-2">
          <strong>Σάββατο 25/05 18:30:</strong> Running RE 6km<br>
          <span class="text-sm text-gray-700">9.3 km/h pace, last 1 km at 9.5. Total 6 km</span>
        </li>
        <li class="mb-2">
          <strong>Δευτέρα 27/05 18:30:</strong> Treadmill 8x1'30"<br>
          <span class="text-sm text-gray-700">11.2 km/h, r/1'30". Total 5.0 km</span>
        </li>
        <li class="mb-2">
          <strong>Τετάρτη 29/05 18:00:</strong> Bodyweight Empowerment<br>
          <span class="text-sm text-gray-700">Push-ups, squats, planks & burpees. 45 λεπτά.</span>
        </li>
      </ul>
    </section>
    """

    html = f"""<!DOCTYPE html>
<html lang="el">
<head>
  <meta charset="UTF-8">
  <title>Ημερήσια Αναφορά</title>
  <script>
    function updateRefreshTime() {{
      const now = new Date();
      const formatted = now.toLocaleTimeString([], {{hour: '2-digit', minute: '2-digit'}});
      document.getElementById("lastRefresh").innerText = "Τελευταία Ενημέρωση σήμερα στις " + formatted;
    }}
  </script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body onload="updateRefreshTime()" class="bg-gray-100 text-gray-800">
  <header class="bg-gray-900 text-white text-center py-6 shadow-md">
    <h1 class="text-4xl font-extrabold">Ημερήσια Αναφορά</h1>
    <p class="text-lg mt-2">{today} - Ανανεώθηκε σήμερα στις {refresh_time}</p>
    <p id="lastRefresh" class="text-sm italic"></p>
    <button onclick="location.reload()" class="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-4 rounded text-sm">Ανανέωση</button>
  </header>

  <main class="max-w-6xl mx-auto py-10 px-4 grid gap-10">

    <section>
      <h2 class="text-2xl font-bold mb-4">📺 YouTube Latest Videos</h2>
      <div class="grid md:grid-cols-3 gap-6">
        <div class="bg-white shadow p-4 rounded text-center">
          <img src="https://img.youtube.com/vi/naoQ40CzmW8/0.jpg" class="rounded w-full mb-2">
          <p class="font-semibold">Λάμπρος Καλαρρύτης</p>
          <a href="https://www.youtube.com/@LAMBROSKALARRYTIS" target="_blank" class="text-blue-600 hover:underline">Δείτε το κανάλι</a>
        </div>
        <div class="bg-white shadow p-4 rounded text-center">
          <img src="https://img.youtube.com/vi/kUgCkiGqLho/0.jpg" class="rounded w-full mb-2">
          <p class="font-semibold">Geostratigiki</p>
          <a href="https://www.youtube.com/@geostratigiki" target="_blank" class="text-blue-600 hover:underline">Δείτε το κανάλι</a>
        </div>
        <div class="bg-white shadow p-4 rounded text-center">
          <img src="{olympiakos_image}" class="rounded w-full h-40 object-contain mb-2">
          <p class="font-semibold">SporFM 94.6 (Ολυμπιακός)</p>
          <a href="https://www.youtube.com/@sporfm946/videos" target="_blank" class="text-blue-600 hover:underline">Δείτε το κανάλι</a>
        </div>
      </div>
    </section>

    <section>
      <h2 class="text-2xl font-bold mb-4">🌍 Geopolitics & International Relations</h2>
      <ul class="list-disc ml-6 text-blue-700">
        <li><a href="https://www.politico.eu/" target="_blank">Politico</a></li>
        <li><a href="https://www.reuters.com/" target="_blank">Reuters</a></li>
        <li><a href="https://www.thestreet.com/" target="_blank">TheStreet</a></li>
        <li><a href="https://www.lemonde.fr/en/" target="_blank">Le Monde</a></li>
        <li><a href="https://www.economist.com/" target="_blank">The Economist</a></li>
        <li><a href="https://www.foreignaffairs.com/" target="_blank">Foreign Affairs</a></li>
        <li><a href="https://www.rednews.gr/" target="_blank">Red News</a></li>
      </ul>
    </section>

    <section>
      <h2 class="text-2xl font-bold mb-4">📈 Commod
