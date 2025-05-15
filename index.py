from datetime import datetime

html_content = open("index.html", "r", encoding="utf-8").read()

today = datetime.now().strftime("%d/%m/%Y")
html_content = html_content.replace("Ημερήσιο Δελτίο", f"Ημερήσιο Δελτίο - {today}")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
