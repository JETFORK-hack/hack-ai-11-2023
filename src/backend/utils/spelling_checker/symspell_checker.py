import os
from symspellpy import SymSpell
from typing import Union
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


class SymSpellChecker:
    
    def __init__(self, config):
        self.config = config
        
        self.max_edit = int(self.config["SYMSPELL_PARAMS"]["MAX_DICTIONARY_EDIT_DISTANCE"])

        self.model = SymSpell(
            max_dictionary_edit_distance=self.max_edit,
            prefix_length=int(self.config["SYMSPELL_PARAMS"]["PREFIX_LENGTH"])
        )

    def load(
        self, term_index: int = 0,
        count_index: int = 1,
        separator: str = "$",
        filepath_unigrams: Union[str, None] = None,
        filepath_bigrams: Union[str, None] = None
    ):
        """ Load model pre-trained dictionary.
        
        Args:
            term_index (int): columns position of the term in dictionary;
            count_index (int): columns position of the weight in dictionary;
            separator (str): separator between term and weight in dictionary;
            filepath_unigrams (str): path to uni-gram dictionary;
            filepath_bigrams (str): path to bi-gram dictionary.
        Returns:
            (self)
        """
        params = {
            "term_index": term_index,
            "count_index": count_index,
            "separator": separator,
            "encoding": "utf-8"
        }

        # self.model.load_dictionary(
        #     filepath_unigrams if filepath_unigrams is not None
        #     else os.path.join(self.config["DATA_PATH"]["SC_VOCAB"], "unigrams.txt"),
        #     **params
        # )
        # self.model.load_bigram_dictionary(
        #     filepath_bigrams if filepath_bigrams is not None
        #     else os.path.join(self.config["DATA_PATH"]["SC_VOCAB"], "bigrams.txt"),
        #     **params
        # )
        return self
        
    def suggest(self, text: str) -> str:
        """ Generate correction for query string.
        
        Args:
            text (str): input string.
        Returns:
            (str): corrected string.
        """
        return self.model.lookup_compound(
            phrase=text,
            max_edit_distance=self.max_edit,
            ignore_non_words=True,
            ignore_term_with_digits=False,
            transfer_casing=False
        )[0].term
