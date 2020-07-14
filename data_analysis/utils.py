############   NATIVE IMPORTS  ###########################
from typing import Dict, Set
from json import dump
############ INSTALLED IMPORTS ###########################
from pandas import read_csv, concat, DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import (
    set_of_semantic_features_for_sentences,
    set_of_semantic_features_for_sentence,
    cosine_similarity_for_sets
)
from utils import BibleText, Bible, QuranText
##########################################################
class RawQuranArabic:
    _PATH = "raw_data/{filename}.txt"
    _FILENAME = "quran_arabic"
    _DELIMITER = "|"

class RawQuranEnglishParallels:
    _PATH = "raw_data/{filename}.txt"
    _FILENAME = "quran_english_translations"
    _CHAPTER_VERSE_SEPARATOR = "-"

class RawQuranArabicGrammarCSVHeaders:
    _PATH = "raw_data/{filename}.txt"
    _FILENAME = "quran_arabic_grammar"
    _DELIMITER = "\t"
    WORD_INDEX = "LOCATION"
    WORD = "FORM"
    POS_TAG = "TAG"
    FEATURES = "FEATURES"
    _FEATURE_DELIMITER = "|"
    _LEMMA_PREFIX = "LEM:"
    _ROOT_PREFIX = "ROOT:"       

def generate_bible_features() -> None:
    """
    get semantic and syntactic features from bible verses
    """
    FEATURES = {}
    BIBLE_EN = BibleText._load(
        path="data/tanakh/{directory}/{book}_{language_code}.json",
        language_code="en",
        book_names=Bible().BOOKS
    )
    for cannon,books in BIBLE_EN.items():
        print(cannon)
        FEATURES[cannon] = {}
        for book,chapters in books.items():
            print(book)
            chapter_features = []
            for chapter_index,verses in enumerate(chapters):
                print(chapter_index)
                verse_features = []
                for verse_index,verse in enumerate(verses):
                    print(verse_index)
                    feature_set = set_of_semantic_features_for_sentence(verse)
                    verse_features.append(feature_set)
                chapter_features.append(verse_features)
            FEATURES[cannon][book] = chapter_features
    with open('data/tanakh/bible_features.json', 'w') as json_file:
        dump(FEATURES, json_file, default=list)

def analyse_quran_arabic_grammar_file() -> DataFrame:
    """ 
    given the raw datafile 
    containing the quran and its morphological and syntactic features for each word in the quran 
    The most important features are extracted for later analysis
    """
    quran = read_csv(
        filepath_or_buffer=RawQuranArabicGrammarCSVHeaders._PATH.format(
            filename=RawQuranArabicGrammarCSVHeaders._FILENAME
        ), 
        sep=RawQuranArabicGrammarCSVHeaders._DELIMITER, 
        header=0
    )
    pos_tags = quran[RawQuranArabicGrammarCSVHeaders.POS_TAG].apply(
        lambda pos_tag:f"POS:{pos_tag}"
    )
    features = quran[RawQuranArabicGrammarCSVHeaders.FEATURES].apply(
        lambda features_as_string:features_as_string.split(RawQuranArabicGrammarCSVHeaders._FEATURE_DELIMITER)
    )
    words = features.apply(
       lambda features_as_list:features_as_list[2].lstrip(
           RawQuranArabicGrammarCSVHeaders._LEMMA_PREFIX
        ) if len(features_as_list)>2 and features_as_list[2].startswith(
            RawQuranArabicGrammarCSVHeaders._LEMMA_PREFIX
        ) else features_as_list[1]
    )
    roots = features.apply(
       lambda features_as_list:features_as_list[3].lstrip(
           RawQuranArabicGrammarCSVHeaders._ROOT_PREFIX
       ) if len(features_as_list)>3 and features_as_list[3].startswith(
           RawQuranArabicGrammarCSVHeaders._ROOT_PREFIX
       ) else None
    )
    root_ngrams = roots.apply(
        lambda root: CountVectorizer(
            ngram_range=(1,3),
            analyzer="char",
            lowercase=False
        ).fit([root]).get_feature_names() if root else []
    )
    indexes = quran[RawQuranArabicGrammarCSVHeaders.WORD_INDEX].apply(
        lambda index_as_string:list(map(int,index_as_string.strip("()").split(":")))
    )
    chapters = indexes.apply(
        lambda index:index[0]
    )
    verses = indexes.apply(
        lambda index:index[1]
    )
    return concat(
        objs=[
            chapters,
            verses,
            pos_tags,
            words,
            root_ngrams
        ],
        keys=[
            "CHAPTER",
            "VERSE",
            "PART OF SPEECH",
            "WORD",
            "ROOT N-GRAMS"
        ],
        axis=1
    )

def generate_arabic_feature_set(arabic_features:DataFrame) -> dict:
    """ 
    given arabic morphological and syntactic features 
    (e.g. arabic root letters, the word's lemma, part of speech, etc)
    for each word in the quran,
    the features are grouped by verse and 
    a set of morphological and syntactic features are returned for each verse in the quran 
    """
    vector_features = {}

    for chapter,verse,pos,word,ngrams in arabic_features.itertuples(index=False):  
        vector_key = f"{chapter}:{verse}"
        if vector_key not in vector_features:
            vector_features[vector_key] = set()

        vector_features[vector_key].add(word)
        vector_features[vector_key].add(pos)
        vector_features[vector_key] |= set(ngrams)

    return vector_features

def analyse_quran_english_parallels_file() -> DataFrame:
    with open(RawQuranEnglishParallels._PATH.format(
            filename=RawQuranEnglishParallels._FILENAME,
        ),
        encoding="utf8",
    ) as english_parallels_file:
        raw_lines = english_parallels_file.readlines()
    
    verse_name = None
    verse_translation = []
    verse_names = []
    verse_translations = []
    for raw_line in raw_lines:
        line =raw_line.strip("\'\" ")
        try:
            chapter_verse = line.split(RawQuranEnglishParallels._CHAPTER_VERSE_SEPARATOR)
            chapter,verse = map(int,chapter_verse)
            verse_name = f"{chapter}:{verse}"
            verse_names.append(verse_name)
            verse_translations.append([])
            line = ""
        except:
            pass

        if line and verse_name:
            verse_translations[-1].append(line)
    
    data = DataFrame(
        {
            "VERSE":verse_names,
            "ENGLISH":verse_translations
        }
    )
    return data.set_index("VERSE")


def analyse_quran_arabic_file() -> DataFrame:
    with open(RawQuranArabic._PATH.format(
            filename=RawQuranArabic._FILENAME,
        ),
        encoding="utf-8",
    ) as arabic_quran_file:
        raw_lines = arabic_quran_file.readlines()
    
    verse_names = []
    quran_ar = []
    for line in raw_lines:
        try:
            chapter,verse,arabic = line.split(RawQuranArabic._DELIMITER)
            verse_names.append(f"{chapter}:{verse}")
            quran_ar.append(arabic.strip())
        except:
            pass
    data = DataFrame(
        {
            "VERSE":verse_names,
            "ARABIC":quran_ar
        }
    )
    return data.set_index("VERSE")

def save_crossreference_quran_bible_to_file(path:str, top_n_search_results:int) -> None:
    """ this stores the quran with cross-references to biblical verses """
    BIBLE = BibleText()
    QURAN = QuranText()
    QURAN_CROSSREFERENCES_TO_BIBLE = {}
    for quran_verse,quran_feature_set in zip(QURAN.VERSE_NAMES,QURAN.FEATURES.values()):
        print(quran_verse)
        semantic_scores = list(
            map(
                lambda bible_feature_set: cosine_similarity_for_sets(
                    features_a=bible_feature_set,
                    features_b=set(quran_feature_set)
                ),
                BIBLE._semantic_features()
            )
        )
        verse_indexes = argsort(semantic_scores)[:-top_n_search_results-1:-1]
        related_bible_verses = list(map(lambda index:BIBLE.VERSE_NAMES[index], verse_indexes))
        QURAN_CROSSREFERENCES_TO_BIBLE[quran_verse] = related_bible_verses
    with open(f'{path}/quran_biblical_crossreferences.json', 'w') as json_file:
        dump(QURAN_CROSSREFERENCES_TO_BIBLE, json_file, default=list)


def save_searchable_quran_to_file(path:str, arabic_feature_sets:Dict[str,Set[str]], top_n_search_results:int) -> None:
    """ this stores the quran in a format that can be queried for similar verses to json files (verse similarities are pre-computed) """
    analyse_quran_arabic_file().to_json(f"{path}/quran_ar.json",orient="index")
    english_quran = analyse_quran_english_parallels_file()
    english_quran.to_json(f"{path}/quran_en.json", orient='index')
    quran = DataFrame(
        arabic_feature_sets.items(),
        columns = ["VERSE","MORPHOLOGICAL FEATURES"]
    )
    quran["SEMANTIC FEATURES"] = [
        set_of_semantic_features_for_sentences(
            sentences=sentences[:-3]
        ) for sentences in english_quran["ENGLISH"].to_list()
    ]    
    quran["SEMANTIC FEATURES"].to_json(f"{path}/quran_features.json", orient='index')
    quran = quran.set_index('VERSE')
    quran["FEATURES"] = [
        morphological_features | semantic_features for morphological_features,semantic_features in zip(
            quran["MORPHOLOGICAL FEATURES"].to_list(),
            quran["SEMANTIC FEATURES"].to_list()
        )
    ]
    quran["CROSS-REFERENCE SCORES"] = quran["FEATURES"].apply(
        lambda feature_set_a: list(
            map(
                lambda feature_set_b: cosine_similarity_for_sets(
                    features_a=feature_set_b,
                    features_b=feature_set_a
                ),
                arabic_feature_sets.values()
            )
        )
    )
    quran["CROSS-REFERENCE INDICES"] = quran["CROSS-REFERENCE SCORES"].apply(
        lambda scores:argsort(scores)[:-top_n_search_results-1:-1]
    )
    verse_names = list(arabic_feature_sets.keys())
    quran["CROSS-REFERENCE"] = quran["CROSS-REFERENCE INDICES"].apply(
        lambda verse_indexes: list(map(lambda index:verse_names[index],verse_indexes))
    )
    quran["CROSS-REFERENCE"].to_json(f"{path}/quran.json", orient='index')