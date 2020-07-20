############   NATIVE IMPORTS  ###########################
from typing import List,Set,Iterable,Dict
from ujson import load
from json import dump
from os.path import exists
from os import makedirs
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import set_of_semantic_features_for_sentence
##########################################################

class QuranText:
    def __init__(self) -> None:     
        with open("raw_data/mushaf/quran_en.json") as json_file:
            self.ENGLISH = load(json_file) 
        with open("raw_data/quran_aisha_bewley.json") as json_file:
            self.another_english = load(json_file)
        with open("raw_data/mushaf/quran_features.json") as json_file:
            self.FEATURES = load(json_file)
        with open("raw_data/mushaf/quran_ar.json") as json_file:
            self.ARABIC = load(json_file)
        with open("raw_data/mushaf/quran.json") as json_file:
            self.CROSS_REFERENCE_QURAN = load(json_file)
        with open("raw_data/mushaf/quran_biblical_crossreferences.json") as json_file:
            self.CROSS_REFERENCE_BIBLE = load(json_file)
        self.VERSE_NAMES = list(self.ENGLISH.keys())
        self.CHAPTER_NAMES = self._get_surah_names()
        self.CHAPTER_SIZES = self._get_surah_sizes()
        self.KEYWORDS = self._get_keywords()
    
    def _get_keywords(self) -> Dict[str,List[str]]:
        keywords = {}
        for verse_index,features in self.FEATURES.items():
            verse_name = self.VERSE_NAMES[int(verse_index)]
            for feature in features:
                if feature.islower():
                    if feature in keywords:
                        keywords[feature].add(verse_name)
                    else:
                        keywords[feature] = {verse_name}
        return keywords

    def _get_surah_names(self) -> List[str]:
        surah_names = []
        for index in range(1,115):
            with open(f"raw_data/quran_surah_names/surah_{index}.json", encoding='utf-8') as json_file:
                surah_names.append(load(json_file)["name"])
        return surah_names
    
    def _get_surah_sizes(self) -> List[int]:
        prev_chapter = "1"
        prev_verse = None
        surah_sizes = []
        for verse_key in self.VERSE_NAMES:
            chapter,verse = verse_key.split(":")
            if chapter != prev_chapter:
                surah_sizes.append(int(prev_verse))
                prev_chapter = chapter
            prev_verse = verse
        surah_sizes.append(int(prev_verse))
        return surah_sizes

    def arabic_verse(self,verse:str) -> str:
        return self.ARABIC[verse]["ARABIC"]

    def english_verses(self,verse:str) -> str:
        return [self.another_english[verse]] + self.ENGLISH[verse]["ENGLISH"][:-1]

    def semantic_features_for_verse(self, verse:str) -> Set[str]:
        bewley_features = set_of_semantic_features_for_sentence(
            sentence=self.another_english[verse]
        )
        index = str(self.VERSE_NAMES.index(verse))
        return set(self.FEATURES[index]) | bewley_features
    
    def data_packet(self,verse_name:str) -> dict:
        return {
            "VERSE":verse_name,
            "ARABIC":self.arabic_verse(verse_name),
            "ENGLISH": dict(map(
                lambda i_verse:
                (   
                    f"TRANSLATION_{i_verse[0]}",
                    i_verse[1]
                ),
                enumerate(self.english_verses(verse_name))
            )),
            "CROSS_REFERENCE":{
                "QURAN":self.CROSS_REFERENCE_QURAN[verse_name],
                "BIBLE":self.CROSS_REFERENCE_BIBLE[verse_name],
            },
            #"FEATURES":self.semantic_features_for_verse(verse_name),
        }


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
        self.FEATURES = self._load_features()
        self.ENGLISH = self._load(path=self.PATH,language_code="en",book_names=self.BOOKS)
        self.HEBREW = self._load(path=self.PATH,language_code="he",book_names=self.BOOKS)
        self.VERSE_NAMES = list(self._verse_names())
        self.KEYWORDS = self._get_keywords()

    def _get_keywords(self) -> Dict[str,List[str]]:
        keywords = {}
        for cannon,books in self.FEATURES.items():
            for book,chapters in books.items():
                for chapter,verses in enumerate(chapters):
                    chapter = int(chapter)+1
                    for verse,features in enumerate(verses):
                        verse = int(verse)+1

                        verse_name = f"{cannon}:{book}:{chapter}:{verse}"

                        for feature in features:
                            if feature.islower():
                                if feature in keywords:
                                    keywords[feature].add(verse_name)
                                else:
                                    keywords[feature] = {verse_name}
        return keywords

    def data_packet(self,cannon:str,book:str,chapter:int,verse:int) -> dict:
        try:
            return {
                "VERSE":f"{cannon}:{book}:{chapter}:{verse}",
                "HEBREW":self.get_verse(json_dictionary=self.HEBREW,cannon=cannon,book=book,chapter=chapter,verse=verse),
                "ENGLISH":self.get_verse(json_dictionary=self.ENGLISH,cannon=cannon,book=book,chapter=chapter,verse=verse),
                #"FEATURES":self.get_verse(json_dictionary=self.FEATURES,cannon=cannon,book=book,chapter=chapter,verse=verse),            
            }
        except Exception as e:
            print(e)
            print(cannon,book,chapter,verse)

    def _verse_names(self) -> Iterable[str]:
        for cannon,books in self.FEATURES.items():
            for book,chapters in books.items():
                for chapter_index,verses in enumerate(chapters):
                    for verse_index,verse_features in enumerate(verses):
                        yield f"{cannon}:{book}:{chapter_index+1}:{verse_index+1}"

    @staticmethod
    def get_verse(json_dictionary:dict, cannon:str, book:str, chapter:int, verse:int) -> str:
        return json_dictionary[cannon][book][chapter-1][verse-1] 

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

def generate_metadata_files() -> None:
    QURAN = QuranText()
    BIBLE = BibleText()
    with open("bible/metatadata.json","w") as json_file:
        dump({
            "VERSE_NAMES":BIBLE.VERSE_NAMES,
            "KEYWORDS":BIBLE.KEYWORDS
        },json_file,indent=4,default=list)
    with open("quran/metatadata.json","w") as json_file:
        dump({
            "VERSE_NAMES":QURAN.VERSE_NAMES,
            "CHAPTER_NAMES":QURAN.CHAPTER_NAMES,
            "CHAPTER_SIZES":QURAN.CHAPTER_SIZES,
            "KEYWORDS":QURAN.KEYWORDS
        },json_file,indent=4,default=list)


def generate_bible_files() -> None:
    BIBLE = BibleText()
    for verse_name in BIBLE.VERSE_NAMES:
        cannon,book,chapter,verse = verse_name.split(":")
        chapter = int(chapter)
        verse = int(verse)
        if not exists(f"bible/{cannon}/{book}/{chapter}"):
            makedirs(f"bible/{cannon}/{book}/{chapter}")
        with open(f"bible/{cannon}/{book}/{chapter}/{verse}.json","w") as json_file:
            dump(BIBLE.data_packet(cannon,book,chapter,verse),json_file,indent=4,default=list)

def generate_quran_files() -> None:
    QURAN = QuranText()
    for verse_name in QURAN.VERSE_NAMES:  
        chapter,verse = verse_name.split(':')  
        if not exists(f"quran/{chapter}"):
            makedirs(f"quran/{chapter}")
        with open(f"quran/{chapter}/{verse}.json","w") as json_file:
            dump(QURAN.data_packet(verse_name),json_file,indent=4,default=list)
