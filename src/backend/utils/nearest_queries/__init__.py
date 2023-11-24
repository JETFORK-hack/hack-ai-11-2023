import numpy as np
from pathlib import Path
import fasttext
import faiss
import json

path = Path(__file__).parent.absolute()
path = Path(path, "resources")

class NearestQueries:
    def __init__(self):
        with open(Path(path, "ind2queries_ft.json"), "r") as f:
            self.ind2query_ft = json.load(f)
        self.model = fasttext.load_model(str(Path(path, "00_fasttext_queries.bin")))
        self.index = faiss.read_index(str(Path(path, "faiss_ft_index.index")))


    def get_knn_query(self, query: str) -> list[str]:
        return [
            self.ind2query_ft[str(i)]
            for i in self.index.search(np.array([self.model.get_sentence_vector(query)]), 3)[1][0]
        ]
