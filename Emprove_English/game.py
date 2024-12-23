import time
from random import randint, random

from logo import LOGO_LINES, LOGO, CORRECT
from vocab import Vocab
from wordcard import WordCard


class Game:
    MODE = (
        (), (0.45, 0.25, 0.15, 0.05, 0.05, 0.05), (0.2, 0.16, 0.16, 0.16, 0.16, 0.16),
        (0.05, 0.05, 0.05, 0.15, 0.25, 0.45))

    def __init__(self):
        Game.print_start_message()
        self.vocab = Vocab()

    @staticmethod
    def print_start_message():
        print(LOGO)
        # for line in LOGO_LINES:
        #     print(line)
        #     time.sleep(0.5)
        time.sleep(2)


    def set_game_mode(self):
        print("--------------------------")
        print('SET GAME MODE')
        print(f'Learning (1), Repetition (2), Memorization (3)')

        while True:
            user_choice = input("Input number: ").strip()
            if user_choice in ['1', '2', '3']:
                mode_number = int(user_choice)
                break

        print(f'= {mode_number}')

        for category, new_weight in zip(self.vocab.categories_with_weights, Game.MODE[mode_number]):
            category.weight = new_weight

    def take_card(self, vocab: Vocab) -> WordCard:

        while True:
            random_weight = random()
            sum_weight = 0
            for category in vocab.categories_with_weights:
                sum_weight += category.weight
                if random_weight <= sum_weight:
                    if not vocab.cards[category.rate]:
                        break
                    rnd = randint(0, len(vocab.cards[category.rate]) - 1)
                    return vocab.cards[category.rate][rnd]

    def make_a_move(self, vocab: Vocab) -> bool:
        if vocab.cards_is_empty is True:
            print('No cards in files.')
            return False
        hand_card = self.take_card(vocab)
        print("--------------------------")
        print("To exit, enter any number.")
        x = randint(0, 1)
        if x == 1:
            hand_card.face, hand_card.back = hand_card.back, hand_card.face
        print(f'-> Translate the text [{hand_card.topic}]: {hand_card.get_card_face()}')
        text = input(f"-> Your version here [{hand_card.topic}]: ").strip().lower()
        if text.isdigit():
            return False
        if text == hand_card.get_card_back():
            print(CORRECT)
            vocab.success_cards.append(hand_card)
        else:
            print(f"WRONG! The right answer: {hand_card.get_card_back().upper()}")
            vocab.fail_cards.append(hand_card)
        return True

    def print_game_result(self, vocab: Vocab):
        print("--------------------------")
        print(f'TOTAL RESULT')
        print(f'Right answers: {len(vocab.success_cards)}')
        print(f'Wrong answers: {len(vocab.fail_cards)}')

    def update_files_with_statistic(self, vocab: Vocab):

        # read old data from files
        for file in vocab.files:
            old_file_lines = []
            with open(file, mode='r', encoding='utf-8') as f:
                for index, line in enumerate(f):
                    old_file_lines.append(line)

            # find line numbers for adding '*'
            line_changing_list = []
            for word_card in vocab.success_cards:
                if word_card.filename == file:
                    line_changing_list.append(word_card.line_idx)

            # rewrite files with old data + add '*' using line_changing_list
            with open(file, mode='w', encoding='utf-8') as f:
                for index, line in enumerate(old_file_lines):
                    if index in line_changing_list:
                        if line.count('*') < 5:
                            line = line.replace('\n', '*\n')
                    f.write(line)

    def start(self):
        self.set_game_mode()
        while True:
            res = self.make_a_move(self.vocab)
            if not res:
                self.print_game_result(self.vocab)
                self.update_files_with_statistic(self.vocab)
                break


if __name__ == '__main__':
    game = Game()
    game.start()
