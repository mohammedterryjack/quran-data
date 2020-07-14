############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
from data_analysis.utils import (
    save_searchable_quran_to_file,
    generate_arabic_feature_set,
    analyse_quran_arabic_grammar_file,
    save_crossreference_quran_bible_to_file,
    generate_bible_features
)
##########################################################

# save_searchable_quran_to_file(
#     arabic_feature_sets = generate_arabic_feature_set(
#         arabic_features=analyse_quran_arabic_grammar_file()
#     ),
#     top_n_search_results=10,
#     path = "data/mushaf"
# )

# generate_bible_features()

# save_crossreference_quran_bible_to_file(
#     path="data/mushaf",
#     top_n_search_results=10,
# )