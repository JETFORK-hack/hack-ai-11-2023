from configparser import ConfigParser
import os
from pathlib import Path
import traceback

from .preprocess import Preprocessor

# from .keyboard_layer_translation import KeyboardCorrector
from .symspell_checker import SymSpellChecker


local_path = str(Path(__file__).parent.absolute())


class SymSpellRouterServicer:
    def __init__(self):
        """Initialize spelling-checker server and models."""

        self.preprocessor = None
        self.keyboard_inverter = None
        self.model = None
        self.config = ConfigParser()
        print("ConfigParser() DONE")
        self.get_or_create_model()
        print("self.get_or_create_model() DONE")

    def get_or_create_model(self):
        """Function for building pipeline objects: preprocessor, keyboard inverter, spelling corrector.

        Returns:
            (obj, obj, obj) - preprocessor, keyboard inverter, spelling corrector.
        """
        self.config.read(os.path.join(local_path, "config.ini"))

        for k in self.config["DATA_PATH"].keys():
            self.config.set(
                "DATA_PATH",
                k,
                os.path.join(local_path, "mount_files", self.config["DATA_PATH"][k]),
            )

        if self.preprocessor is None:
            self.preprocessor = Preprocessor()

        # if self.keyboard_inverter is None:
        #     self.keyboard_inverter = KeyboardCorrector(self.config)

        if self.model is None:
            self.model = SymSpellChecker(self.config).load()
        print("loaded!")
        return self.preprocessor, self.keyboard_inverter, self.model

    @staticmethod
    def simple_replace(text: str) -> str:
        """Replace russian special characters outside preprocessor.

        Args:
            text (str): source string.
        Returns:
            (str): processed string.
        """
        return text.replace("ё", "е")

    def preprocess_and_correct_single(self, params: dict, use_correction: bool) -> str:
        """Support function for preprocess and correct string.

        Args:
            params (dict): parameters for preprocessing;
            use_correction (bool): use spelling correction.
        Returns:
            (str): processed string.
        """
        res = self.preprocessor.run(**params)
        if use_correction:
            return self.model.suggest(res)
        return res

    def predict_single_correction(
        self,
        request: str,
        use_preprocessing: bool,
        use_keyboard_inverter: bool,
        use_correction: bool,
    ) -> tuple[str, str]:
        """Generate prediction for single input request.

        Args:
            request (str) - input request with preprocessing parameters.
        Returns:
            (str)
        """

        result: str = request

        params = {
            "text": request,
            "inverter": self.keyboard_inverter.translate_sentence
            if use_keyboard_inverter
            else None,
            "use_preprocessing": use_preprocessing,
        }

        try:
            result = self.preprocess_and_correct_single(params, use_correction)
            result = self.simple_replace(result)
        except:
            print(traceback.format_exc())

        return request, result
