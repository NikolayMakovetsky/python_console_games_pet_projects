class WordCard:

    def __init__(self, filename: str, line_idx: int, category: int, face: str, back: str, rate: int):
        self.filename: str = filename
        self.line_idx: int = line_idx
        self.category: int = category
        self.face: str = face
        self.back: str = back
        self.rate: int = rate

    def __repr__(self):
        return f'WordCard({self.face} - {self.back})'

    def get_card_face(self):
        return self.face

    def get_card_back(self):
        return self.back
