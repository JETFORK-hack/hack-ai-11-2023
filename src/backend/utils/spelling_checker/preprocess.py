from typing import List, Union
from unicodedata import normalize, category

from .blank import *


class Preprocessor:

    @staticmethod
    def remove_accents(text: str) -> str:
        """ Replace diacritic symbols from string into latin alphabet and turn into lower case.
        
        Args:
            text (str): input string.
        Returns:
            (str): processed string.
        """
        text = text.lower()
        text = char2idx_1.sub(idx2char_1.pattern, text)
        text = char2idx_2.sub(idx2char_2.pattern, text)
        text = "".join(c for c in normalize("NFD", text)
                       if category(c) != "Mn")
        text = idx2char_1.sub("й", text)
        text = idx2char_2.sub("ё", text)
        return text.strip()
    
    @staticmethod
    def remove_greek(text: str) -> str:
        """ Replace greek symbols to latin alphabet.
        
        Args:
            text (str): input string.
        Returns:
            (str): processed string.
        """
        for k, v in greek_replacer.items():
            if k in text:
                text = re.sub(k, v, text)
        text = text.translate(text.maketrans(greek_mapper))
        return text.strip()
    
    @staticmethod
    def process_string(text: str) -> str:
        """ Postprocessing string method. Replace slashes, split concatenated sentences, normalize apostrophes,
        save only valid characters in string and delete duplicated spaces.
        
        Args:
            text (str): input string.
        Returns:
            (str): processed string.
        """
        text = concatenated_sent.sub(" ", text)
        text = apostrophe.sub("'", text)
        text = multiple_in_one.sub("в", text)
        text = colon_regex.sub(" ", text)
        text = amp_regex.sub(" & ", text)
        text = final_regex.sub(" ", text)
        text = ends_regex.sub("", text)
        text = multiple_dots.sub(" ", text)
        text = space_regex.sub(" ", text)
        return text.strip()
    
    def preprocess(self, text: str) -> str:
        """ Simple preprocessing. Using remove_accents and remove_greek methods.
        Remove hyphen from string, if it is in start or in the end of word;
        remove single hyphen, replace suffix 's to s.
        
        Args:
            text (str): input string.
        Returns:
            (str): processed string.
        """
        text = self.remove_accents(text)
        text = self.remove_greek(text)
        text = broken_hyphen.sub(" ", text)
        return text.strip()

    def run_single(
            self, text: str, inverter=None, use_preprocessing: bool=True
    ) -> str:
        """ String normalization pipeline.
        
        Args:
            text (str): input single string;
            inverter (obj): object of keyboard inverter (default=None);
            use_preprocessing (bool): use custom string processing (default=True).
        Returns:
            (str): normalized single string.
        """
        text = self.preprocess(text)
        if inverter is not None:
            text = inverter(text)
        if use_preprocessing:
            text = self.process_string(text)
        return text
            
    def run(
        self, text: Union[str, List[str]], inverter=None, use_preprocessing: bool=True
    ) -> Union[str, List[str]]:
        """ String normalization pipeline.
        
        Args:
            text (Union[str, List[str]]): input documents or single string;
            inverter (obj): object of keyboard inverter (default=None);
            use_preprocessing (bool): use replacing for diacritic and greek symbols (default=True).
        Returns:
            (Union[str, List[str]]): normalized single string or array of strings.
        """
        local_params = {k: v for k, v in locals().items() if k != "self"}
        return self.run_single(**local_params)
