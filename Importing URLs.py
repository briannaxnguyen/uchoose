import requests
from bs4 import BeautifulSoup
import pandas as ps

York_url = "https://www.ouinfo.ca/programs/universities/york"
Uni = [York_url, "https://www.ouinfo.ca/programs/universities/windsor", "https://www.ouinfo.ca/programs/universities/laurier-waterloo", "https://www.ouinfo.ca/programs/universities/western","https://www.ouinfo.ca/programs/universities/waterloo", "https://www.ouinfo.ca/universities/trent", "https://www.ouinfo.ca/programs/universities/toronto-metropolitan","https://www.ouinfo.ca/universities/toronto-st-george", "https://www.ouinfo.ca/programs/universities/rmc", "https://www.ouinfo.ca/programs/universities/queens", "https://www.ouinfo.ca/programs/universities/ottawa", "https://www.ouinfo.ca/programs/universities/ontario-tech", "https://www.ouinfo.ca/programs/universities/uof", "https://www.ouinfo.ca/programs/universities/ocad-u", "https://www.ouinfo.ca/programs/universities/nipissing", "https://www.ouinfo.ca/programs/universities/mcmaster", "https://www.ouinfo.ca/programs/universities/laurentian", "https://www.ouinfo.ca/programs/universities/lakehead", "https://www.ouinfo.ca/programs/universities/hearst", "https://www.ouinfo.ca/programs/universities/guelph", "https://www.ouinfo.ca/programs/universities/carleton", "https://www.ouinfo.ca/programs/universities/brock", "https://www.ouinfo.ca/programs/universities/algoma"]

my_header = {
    "User-Agent":"Mozilla/5.0"
}
links = []
for link in Uni:
    response = requests.get(link, headers=my_header)

    html_extraction = response.text
    soup = BeautifulSoup(html_extraction, "html.parser")

    main = soup.find_all("article", class_="result result-program")
    
    for i in main: 
        for a in i.find_all("a"):
            href = a.get("href")
            if href.startswith("/programs"):
                links.append(href)

all_data = []  # this will be a list of dicts

for f in links:
    response = requests.get("https://www.ouinfo.ca" + f, headers=my_header)
    soup = BeautifulSoup(response.text, "html.parser")

    definitions = soup.find("dl")
    if not definitions:
        continue  # skip if nothing found

    dt_tags = definitions.find_all("dt")
    dd_tags = definitions.find_all("dd")

    program_data = {}
    for i, j in zip(dt_tags, dd_tags):
        label = i.text.strip()
        value = j.text.strip()
        program_data[label] = value
    
    # Optionally add program URL too
    program_data["Program URL"] = "https://www.ouinfo.ca" + f

    all_data.append(program_data)

with open("program_data.txt", "w", encoding="utf-8") as f:
    for entry in all_data:
        for key, value in entry.items():
            f.write(f"{key}: {value}\n")
        f.write("\n" + "-"*60 + "\n\n")  # separator between programs

print(f"\n✅ Done! Saved {len(all_data)} program entries to 'program_data.txt'")

