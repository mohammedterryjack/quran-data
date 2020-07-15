############   NATIVE IMPORTS  ###########################
from typing import List
from ujson import load
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
##########################################################

QURAN = QuranText()
PATH = "quran/{chapter}/{verse}"

class QuranText:
    def __init__(self) -> None:               
        self.VERSE_NAMES = list(self.ENGLISH().keys())
    
    def ENGLISH(self) -> dict:
        with open("raw_data/mushaf/quran_en.json") as json_file:
            return load(json_file) 
    
    def FEATURES(self) -> dict:
        with open("raw_data/mushaf/quran_features.json") as json_file:
            return load(json_file)

    def ARABIC(self) -> dict:
        with open("raw_data/mushaf/quran_ar.json") as json_file:
            return load(json_file)
    
    def CHAPTER_NAMES(self) -> List[str]:
        surah_names = []
        for index in range(1,115):
            with open(f"raw_data/quran_surah_names/surah_{index}.json", encoding='utf-8') as json_file:
                surah_names.append(load(json_file)["name"])
        return surah_names

    def CROSS_REFERENCES_QURAN(self) -> dict:
        with open("raw_data/mushaf/quran.json") as json_file:
            return load(json_file)

    def CROSS_REFERENCES_BIBLE(self) -> dict:
        with open("raw_data/mushaf/quran_biblical_crossreferences.json") as json_file:
            return load(json_file)



class Bible:
    def __init__(self) -> None:
        self.BOOKS = {
            "torah/genesis":"01","torah/exodus":"02","torah/leviticus":"03","torah/numbers":"04","torah/deuteronomy":"05",
            "prophets/joshua":"06","prophets/judges":"07","prophets/i%20samuel":"08a","prophets/ii%20samuel":"08b",
            "prophets/i%20kings":"09a","prophets/ii%20kings":"09b","prophets/isaiah":"10","prophets/jeremiah":"11",
            "prophets/ezekiel":"12","prophets/hosea":"13","prophets/joel":"14","prophets/amos":"15","prophets/obadiah":"16",
            "prophets/jonah":"17","prophets/micah":"18","prophets/nahum":"19","prophets/habakkuk":"20",
            "prophets/zephaniah":"21","prophets/haggai":"22","prophets/zechariah":"23","prophets/malachi":"24",
            "writings/i%20chronicles":"25a","writings/ii%20chronicles":"25b","writings/psalms":"26","writings/job":"27",
            "writings/proverbs":"28","writings/ruth":"29","writings/song%20of%20songs":"30","writings/ecclesiastes":"31",
            "writings/lamentations":"32","writings/esther":"33","writings/daniel":"34","writings/ezra":"35a","writings/nehemiah":"35b"
        }


class BibleText(Bible):
    def __init__(self) -> None:
        super().__init__() 
        self.PATH = "raw_data/tanakh/{directory}/{book}_{language_code}.json"
        self.VERSE_NAMES = list(self._verse_names())

    def FEATURES(self) -> dict:
        return self._load_features()

    def ENGLISH(self) -> dict:
        return self._load(path=self.PATH,language_code="en",book_names=self.BOOKS)

    def HEBREW(self) -> dict:
        return self._load(path=self.PATH,language_code="he",book_names=self.BOOKS)

    @staticmethod
    def _load_features() -> dict:
         with open("raw_data/tanakh/bible_features.json") as json_file:
            return load(json_file)

    @staticmethod
    def _load(path:str, language_code:str, book_names:List[str]) -> dict:
        bible = {}
        for book_name in book_names:
            directory,book = book_name.lower().split("/")
            if directory not in bible:
                bible[directory] = {}
            full_path = path.format(
                directory=directory,
                book=book,
                language_code=language_code
            )
            with open(full_path,encoding='utf-8') as json_file:
                bible[directory][book] = load(json_file)["text"]
        return bible 