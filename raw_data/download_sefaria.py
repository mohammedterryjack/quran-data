############   NATIVE IMPORTS  ###########################f
from os import system
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
##########################################################
PATH_TO_SAVE = "data/tanakh/{cannon}/{book}_{language_code}.json"
LANGUAGES = ("English","Hebrew")
CANNON_BOOKS_MAP = {
    "Torah":["Deuteronomy","Exodus","Genesis","Leviticus","Numbers"],
    "Prophets":[
        "Amos","Ezekiel","Habakkuk","Haggai","Hosea",
        "I%20Kings","I%20Samuel","II%20Kings","II%20Samuel",
        "Isaiah","Jeremiah","Joel","Jonah","Joshua",
        "Judges","Malachi","Micah","Nahum","Obadiah",
        "Zechariah","Zephaniah"
    ],
    "Writings":[
        "Daniel","Ecclesiastes","Esther","Ezra",
        "I%20Chronicles","II%20Chronicles","Job",
        "Lamentations","Nehemiah","Proverbs",
        "Psalms","Ruth","Song%20of%20Songs"
    ]
}
URL = "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/json/Tanakh/{cannon}/{book}/{language}/merged.json"

for cannon,books in CANNON_BOOKS_MAP.items():
    for book in books:
        for language in LANGUAGES:
            url = URL.format(
                cannon=cannon,
                book=book,
                language=language
            )
            path_to_save = PATH_TO_SAVE.format(
                cannon=cannon.lower(),
                book=book.lower(),
                language_code = language[:2].lower()
            )
            system(f"curl {url} --output {path_to_save}")