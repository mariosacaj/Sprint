class Concept:
    def __init__(self, concept: str, score: int):
        self.concept = concept
        self.score = score

    def get_concept(self):
        return self.concept

    def set_type(self, type_: str):
        self.type = type_

    def get_type(self):
        return self.type

    def get_score(self):
        return self.score
