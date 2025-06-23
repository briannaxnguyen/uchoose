import requests
from bs4 import BeautifulSoup
import pandas as ps

url = "https://www.ouinfo.ca/programs"
test_url = "https://www.ouinfo.ca/programs/trent/rij"

my_header = {
    "User-Agent":"Mozilla/5.0"
}

response = requests.get(test_url, headers=my_header)

html_extraction = response.text
soup = BeautifulSoup(html_extraction, "html.parser")


definitions = soup.find("dl")

#the dt tags is the template section like "program name" and "University" etc.
dt_tags = definitions.find_all("dt")
#the dd tags are the answers to the dt tags, like the actual names of the uni etc.
dd_tags = definitions.find_all("dd")

Test_data = {}

for i, j in zip(dt_tags, dd_tags):
    label = i.text.strip()
    value = j.text.strip()
    Test_data[label] = value

for a, b in Test_data.items():
    print(a, ":", b)





#df1 = ps.DataFrame([Test_data])

#path = r"C:\Users\affan\Documents\Coding Projects\Uni.xlsx"
#df1.to_excel(path)

#with ps.ExcelWriter(path) as engine:
