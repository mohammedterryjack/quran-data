from bs4 import BeautifulSoup
from requests import get 
from json import dump

URL = "https://quranunlocked.com/en.bewley/text/{chapter_verse}"

HEADERS = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'referrer': 'https://google.com'
}
number_of_verses = [
    7,286,200,176,120,
    165,206,75,129,109,
    123,111,43,52,99,
    128,111,110,98,135,
    112,78,118,64,77,
    227,93,88,69,60,
    34,30,73,54,45,
    83,182,88,75,85,
    54,53,89,59,37,
    35,38,29,18,45,
    60,49,62,55,78,
    96,29,22,24,13,
    14,11,11,18,12,
    12,30,52,52,44,
    28,28,20,56,40,
    31,50,40,46,42,
    29,19,36,25,22,
    17,19,26,30,20,
    15,21,11,8,8,
    19,5,8,8,11,
    11,8,3,9,5,
    4,7,3,6,3,
    5,4,5,6
]


quran = {}
try:
    for chapter in range(1,115):
        for verse in range(1,number_of_verses[chapter-1]+1,3):
            verse_key = f"{chapter}/{verse}"
            url = URL.format(chapter_verse=verse_key)
            html_text = get(url, HEADERS).text
            soup = BeautifulSoup(html_text,"html.parser")
            mydivs = soup.findAll("span", {"class": "ayah-text"})
            for verse in mydivs:
                text = verse.findAll(text=True)
                _,key,english = text
                quran[key] = english.strip()
                print(key)
                print(english.strip())
                print()
except:
    pass 

with open("quran_aisha_bewley.json","w") as f:
    dump(quran,f,indent=4)

