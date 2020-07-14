############   NATIVE IMPORTS  ###########################f
from typing import Set, Tuple, List
from itertools import chain
############ INSTALLED IMPORTS ###########################
from nltk.corpus import wordnet, stopwords
from nltk import pos_tag, word_tokenize
from nltk.util import ngrams
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
############   LOCAL IMPORTS   ###########################
##########################################################
parent_synsets_for_synset = lambda synset:[synset] + list(synset.closure(lambda parent_synset:parent_synset.hypernyms()))
parent_synsets_for_synsets = lambda synsets: list(chain.from_iterable(map(parent_synsets_for_synset, synsets)))
STOPWORDS = set(stopwords.words('english')) | ENGLISH_STOP_WORDS

def tokenise(sentence:str) -> List[str]:
    """
    tokenise string but maintain compound phrases
    e.g. the couple were in love -> ["the","couple","were","in love"] 
    """
    tokens = word_tokenize(sentence)
    token_found = list(map(lambda _:False,tokens))

    ngram_range = range(len(tokens),0,-1)

    for ngram_size in ngram_range:
        for index_start,ngram_string in enumerate(
            map('_'.join,ngrams(sequence=tokens,n=ngram_size))
        ):
            if all(token_found):
                break
            index_end = index_start+ngram_size
            contains_word_included_in_another_ngram = any(token_found[index_start:index_end])
            if wordnet.synsets(ngram_string) and not contains_word_included_in_another_ngram:
                token_found[index_start:index_end] = [ngram_string.replace("_"," ")] + ["PAD"]*(ngram_size-1)

    if not all(token_found):
        for index,found in enumerate(token_found):
            if not found:
                token_found[index] = tokens[index]

    for index,found in enumerate(token_found):
        if found == "PAD":
            token_found.pop(index)

    return token_found


def part_of_speech(tokens:List[str]) -> List[Tuple[str,str]]:
    """ 
    tags tokens using nltk and then converts tag format to wordnet's format
    ignoring irrelevant tags like DET
    """
    WORDNET_POS_MAP = {
        "VERB":wordnet.VERB,
        "ADJ":wordnet.ADJ,
        "ADV":wordnet.ADV,
        "NOUN":wordnet.NOUN
    }
    return list(
        filter(
            lambda token_pos: token_pos[1] is not None,
            map(
                lambda token_pos: (
                    token_pos[0].replace(" ","_"),
                    WORDNET_POS_MAP.get(token_pos[1])
                ),
                pos_tag(tokens,tagset="universal")
            )
        )
    )

def set_of_morphological_features_for_word(word:str) -> Set[str]:
    """
    returns the word and various sized ngrams of it
    """
    return {word.upper()} | set(
        map(
            lambda ngram:ngram.upper(),
            CountVectorizer(
                ngram_range=(2,4),
                analyzer="char_wb"
            ).fit([word]).get_feature_names()
        )
    )


def set_of_semantic_features_for_word(word:str, part_of_speech:str) -> Set[str]:
    """ 
    uses wordnet to return a semantic concepts related to a given word
    stopwords are only encoded morphologically but not semantically
    """
    features = set_of_morphological_features_for_word(word)
    if word not in STOPWORDS:
        root_synsets = wordnet.synsets(word,pos=part_of_speech)
        if not any(root_synsets):
            root_synsets = wordnet.synsets(word)
        features |= set(
            map(
                lambda synset:synset.name(), 
                parent_synsets_for_synsets(root_synsets)
            )
        )
    return features

def set_of_semantic_features_for_sentence(sentence:str) -> Set[str]:
    """
    returns a set of semantic features for a given sentence 
    """
    return set(
        chain.from_iterable(
            map(
                lambda token_pos:set_of_semantic_features_for_word(*token_pos),
                part_of_speech(tokenise(sentence))
            )
        )
    )

def set_of_semantic_features_for_sentences(sentences:List[str]) -> Set[str]:
    """
    returns a single set of semantic features for a synonymous group of sentences 
    """
    return set(chain.from_iterable(map(set_of_semantic_features_for_sentence,sentences)))


def similarity_of_two_sets_of_features(features_a:set, features_b:set) -> float:
    """ 
    returns a simple similarity score given two sets. 
    1.0=Identical. 0.0=Nothing in Common
    """
    features_in_common = features_a.intersection(features_b)
    features_in_total = features_a | features_b
    return  len(features_in_common) / len(features_in_total)


def cosine_similarity_for_sets(features_a:set, features_b:set) -> float: 
    """
    returns the cosine similarity of two sets
    1.0=Identical. 0.0=Nothing in Common
    """
    features_in_common = features_a.intersection(features_b)
    denominator = len(features_a)**.5 * len(features_b)**.5
    return len(features_in_common)/denominator if denominator else .0