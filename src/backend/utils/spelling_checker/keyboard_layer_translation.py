import json
import os
from typing import List


class KeyboardCorrector:
    
    def __init__(self, config):
        json_path = config["DATA_PATH"]["KEYBOARD_DICTS"]
        vocab_path = os.path.join(config["DATA_PATH"]["SC_VOCAB"], "unigrams.txt")
        
        self.eng_ru = json.load(open(os.path.join(
            json_path,
            "eng.json"
        ), encoding="utf-8"))
        self.ru_eng = json.load(open(os.path.join(
            json_path,
            "ru.json"
        ), encoding="utf-8"))

        self.vocab = self.create_vocab_trans(list(set([i.split("$")[0].strip() for i in self.read_vocab(vocab_path)])))
     
    @staticmethod
    def read_vocab(vocab_path: str):
        vocab = []
        with open(vocab_path, "r", encoding="utf-8") as f:
            vocab += f.readlines()
        return vocab

    def create_vocab_trans(self, vocab: List[str]):
        def make_trans(v, d):
            for w in v:
                yield w.translate(w.maketrans(d))

        old_vocab = dict(zip(vocab, range(len(vocab))))
        new_vocab = {}
        for word, er_trans, re_trans in zip(vocab, make_trans(vocab, self.eng_ru), make_trans(vocab, self.ru_eng)):
            if word != er_trans and old_vocab.get(er_trans) is None:
                new_vocab[er_trans] = word
            if word != re_trans and old_vocab.get(re_trans) is None:
                new_vocab[re_trans] = word
        return new_vocab

    def translate(self, word: str):
        return self.vocab.get(word, word)
    
    def translate_sentence(self, sentence: str):
        return " ".join(list(map(self.translate, sentence.split(" "))))
    