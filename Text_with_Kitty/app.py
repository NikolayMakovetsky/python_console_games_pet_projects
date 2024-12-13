import glob
import time
from collections import namedtuple
from operator import attrgetter
from pprint import pprint
from random import randint, random

LOGO = """
░░░░░░░░░░░░░░░░░░░░░▄▀░░▌
░░░░░░░░░░░░░░░░░░░▄▀▐░░░▌
░░░░░░░░░░░░░░░░▄▀▀▒▐▒░░░▌
░░░░░▄▀▀▄░░░▄▄▀▀▒▒▒▒▌▒▒░░▌
░░░░▐▒░░░▀▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒█
░░░░▌▒░░░░▒▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
░░░░▐▒░░░░░▒▒▒▒▒▒▒▒▒▌▒▐▒▒▒▒▒▀▄
░░░░▌▀▄░░▒▒▒▒▒▒▒▒▐▒▒▒▌▒▌▒▄▄▒▒▐
░░░▌▌▒▒▀▒▒▒▒▒▒▒▒▒▒▐▒▒▒▒▒█▄█▌▒▒▌
░▄▀▒▐▒▒▒▒▒▒▒▒▒▒▒▄▀█▌▒▒▒▒▒▀▀▒▒▐░░░▄       _           _            _ _   _      _   _ _   _        
▀▒▒▒▒▌▒▒▒▒▒▒▒▄▒▐███▌▄▒▒▒▒▒▒▒▄▀▀▀▀        | |_ _____ _| |_  __ __ _(_) |_| |_   | |_(_) |_| |_ _  _ 
▒▒▒▒▒▐▒▒▒▒▒▄▀▒▒▒▀▀▀▒▒▒▒▄█▀░░▒▌▀▀▄▄       |  _/ -_) \ /  _| \ V  V / |  _| ' \  | / / |  _|  _| || |
▒▒▒▒▒▒█▒▄▄▀▒▒▒▒▒▒▒▒▒▒▒░░▐▒▀▄▀▄░░░░▀       \__\___/__\_\__|  \_/\_/|_|\__|_||_| |_\_\_|\__|\__|\_, |
▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▄▒▒▒▒▄▀▒▒▒▌░░▀▄                                                              |__/ 
▒▒▒▒▒▒▒▒▀▄▒▒▒▒▒▒▒▒▀▀▀▀▒▒▒▄▀
"""
LOAD_MESSAGES = ["application is getting started...",
                 "loading vocabulary files...",
                 "anylyzing ratings...",
                 "structuring words and phrases..."]

Category = namedtuple("Category", ["rate", "quantity", "weight"])


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


class Vocab:
    BASE_DIR = '.\\data\\'
    FILE_PATTERN = '_vocab.txt'

    def __init__(self, base_dir: str = BASE_DIR, file_pattern: str = FILE_PATTERN):
        self.base_dir: str = base_dir
        self.file_pattern: str = file_pattern
        self.files: list = self.get_list_of_files()
        self.cards: dict[int:[WordCard]] = self.get_dict_with_cards()
        self.categories_with_weights: list[Category] = self.get_categories_with_weights()
        self.success_cards: [WordCard] = []
        self.fail_cards: [WordCard] = []

    def get_list_of_files(self):
        lst = []
        for filename in glob.glob(f'{self.base_dir}*{self.file_pattern}'):
            lst.append(filename)
        return lst

    def get_dict_template(self):
        rate_dict = {0: []}

        for file in self.files:
            with open(file, mode='r', encoding='utf-8') as f:
                for index, line in enumerate(f):
                    if '*' in line:
                        card_rate = line.count('*')

                        if not rate_dict.get(card_rate):
                            rate_dict[card_rate] = []
        return rate_dict

    def get_dict_with_cards(self):

        card_dict = self.get_dict_template()

        for file in self.files:
            category_name = file.rstrip(self.file_pattern).lstrip(self.base_dir)

            with open(file, mode='r', encoding='utf-8') as f:
                for index, line in enumerate(f):
                    line = line.strip()
                    if line and '-' in line:
                        card_rate = line.count('*')

                        line = line.replace('*', '')
                        card_face, card_back = [x.strip() for x in line.split('-')]

                        w_card = WordCard(filename=file,
                                          line_idx=index,
                                          category=category_name,
                                          face=card_face,
                                          back=card_back,
                                          rate=card_rate)

                        card_dict[card_rate].append(w_card)
        return card_dict

    def get_categories_with_weights(self) -> list[Category]:
        # Category = namedtuple("Category", ["rate", "quantity", "weight"])

        sum_ = sum(len(v) for v in self.cards.values())

        category_list = []
        for k, v in self.cards.items():
            category_list.append(Category(rate=k, quantity=len(v), weight=len(v) / sum_))
            print(category_list[-1])  #

        return sorted(category_list, key=attrgetter('weight'))

    def take_card(self) -> WordCard:
        random_weight = random()
        print(random_weight)

        sum_weight = 0
        pprint(self.categories_with_weights)  #
        for category in self.categories_with_weights:
            sum_weight += category.weight
            if random_weight <= sum_weight:
                print(f'Choosen category: {category=}')
                rnd = randint(0, len(self.cards[category.rate]) - 1)
                return self.cards[category.rate][rnd]

    def make_a_move(self) -> bool:
        hand_card = self.take_card()
        print("Open menu: 1")
        print(f'-> Translate the text: {hand_card.get_card_face()}')
        text = input("-> Your version here: ").strip()
        if text.isdigit():
            return False
        if text == hand_card.get_card_back():
            print("Correct! =)")
            self.success_cards.append(hand_card)
        else:
            print(f"Incorrect! The right answer is: {hand_card.get_card_back()}")
            self.fail_cards.append(hand_card)
        return True

    def print_statistic(self):
        print(f'Правильных ответов: {len(self.success_cards)}')
        print(f' Ошибочных ответов: {len(self.fail_cards)}')

    def update_files_with_statistic(self):

        for file in self.files:
            old_file_lines = []
            with open(file, mode='r', encoding='utf-8') as f:
                for index, line in enumerate(f):
                    old_file_lines.append(line)

            line_changing_list = []
            for word_card in self.success_cards:
                if word_card.filename == file:
                    line_changing_list.append(word_card.line_idx)

            with open(file, mode='w', encoding='utf-8') as f:
                for index, line in enumerate(old_file_lines):
                    if index in line_changing_list:
                        print(f"Line {index} before: {line}")
                        line = line.replace('\n', '*\n')  #
                        print(f"Line {index} after: {line}")
                    f.write(line)


class Game:
    def __init__(self):
        self.vocab = Vocab()
        Game.print_start_message()

    @classmethod
    def print_start_message(cls):
        print(LOGO)
        delay = 0
        for i in LOAD_MESSAGES:
            # delay = randint(1, 3)
            time.sleep(delay)
            print(i)
        time.sleep(0)

    def start(self):
        while True:
            res = self.vocab.make_a_move()
            if not res:
                print(f'=== РЕЗУЛЬТАТ ИГРЫ ===')
                self.vocab.print_statistic()
                self.vocab.update_files_with_statistic()
                break


if __name__ == '__main__':
    game = Game()
    game.start()
