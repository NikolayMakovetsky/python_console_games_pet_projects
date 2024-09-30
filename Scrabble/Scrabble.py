# Игра "Эрудит"

# ПРАВИЛА ИГРЫ
# Играют 2 игрока (пользователь "user" против компьютера "carl")
# Задача состоит в том,
# чтобы составлять как можно более длинные слова из букв заданного слова.
# В игре участвуют только слова - существительные в единственном числе.
# За каждую букву правильно составленного слова начисляется 1 балл.
# Игра состоит из 3-х раундов, по итогу которых нужно обойти соперника по баллам.

from random import choice
from collections import Counter
import json

with open("rus_nouns.json", "r", encoding="utf-8") as file:
    W = json.loads(file.read())


def color(col: str, text: str) -> tuple:
    """
        Вывести цветной текст на экран
        "".join(color('red', 'example 1')
        print(*color('red', 'example 2'))
    
    """
    if col == "blue":
        return "\033[34m{}".format(text), "\033[0m{}".format("")
    elif col == "red":
        return "\033[31m{}".format(text), "\033[0m{}".format("")
    elif col == "yellow":
        return "\033[33m{}".format(text), "\033[0m{}".format("")
    elif col == "green":
        return "\033[32m{}".format(text), "\033[0m{}".format("")


class Player:
    def __init__(self, name: str):
        self.name = name
        self.words = []

    def set_words(self, start_word) -> None:
        """Исключить возможность использования стартового слова в игре"""
        self.words.append({start_word, len(start_word)})

    def get_score(self) -> int:
        """Получить счет игрока"""
        return sum([sum(d.values()) for d in self.words[1:]])


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.start_word = ""
        self.game_words = []

    def flip_coin(self) -> None:
        """Определить очередность первого хода"""
        flip = choice([0, 1])
        if flip == 1:
            self.player1, self.player2 = self.player2, self.player1

    def set_start_word(self) -> None:
        """Случайным образом выбрать стартовое слово длиной более 6 букв"""
        s = [x for x in W if len(x) > 6]
        self.start_word = choice(s)

    def set_game_words(self) -> None:
        """Выбрать все слова, которые могут быть составлены из стартового слова"""

        stw = self.start_word

        set_stw = set(stw)
        dict_stw = dict(Counter(stw))

        game_words = []
        for w in W:
            if w != stw and len(set_stw & set(w)) == len(set(w)):
                set_w = set(w)
                dict_w = dict(Counter(w))
                for ch in set_w:
                    if dict_w.get(ch) > dict_stw.get(ch):
                        break
                else:
                    game_words.append(w)

        self.game_words = game_words

    def initial_game(self) -> None:
        """Инициализировать игру"""
        print("".join(color("yellow", "------- Э Р У Д И Т -------")))
        self.set_start_word()
        self.player1.set_words(self.start_word)
        self.player2.set_words(self.start_word)
        self.set_game_words()
        self.flip_coin()

    def print_used_words(self) -> None:
        """Вывести слова, которые уже были использованы игроками в процессе игры"""
        pl1_words = ["".join(d.keys()) for d in self.player1.words[1:]]
        pl2_words = ["".join(d.keys()) for d in self.player2.words[1:]]
        if pl1_words + pl2_words:
            print(*color('yellow', "/".join(sorted(pl1_words + pl2_words))))

    def print_game_status(self) -> None:
        """Вывести информацию о текущем статусе игры"""
        print(*f"{self.start_word.upper()}|", sep=" ", end=" ")
        print("".join(color("red", f"{self.player1.name}")), f"{self.player1.get_score()}", ":",
              "".join(color("blue", f"{self.player2.name}")), f"{self.player2.get_score()}")
        self.print_used_words()

    def print_game_result(self) -> None:
        """Вывести на экран результаты игры"""
        self.print_used_words()
        print("".join(color('yellow', "ИГРА ЗАВЕРШЕНА ")), "|", sep="", end=" ")
        print("".join(color("red", f"{self.player1.name}")), f"{self.player1.get_score()}", ":",
              "".join(color("blue", f"{self.player2.name}")), f"{self.player2.get_score()}")

        if self.player1.get_score() > self.player2.get_score():
            print("".join(color("red", "ПОБЕДИЛ")),
                  "".join(color("red", f"{self.player1.name.upper()}")))
        elif self.player1.get_score() < self.player2.get_score():
            print("".join(color("blue", "ПОБЕДИЛ")),
                  "".join(color("blue", f"{self.player2.name.upper()}")))
        else:
            print("".join(color("green", "НИЧЬЯ")))


def run_game() -> None:
    player1 = Player("user")
    player2 = Player("carl")

    g = Game(player1, player2)
    g.initial_game()

    i = 0
    while i < 3 and len(g.game_words) > 1:

        g.print_game_status()

        if g.player1.name == "user":
            word = input(f"{g.player1.name}: ").lower()
            if word not in g.game_words or word in g.player1.words or word in g.player2.words:
                g.player1.words.append({word: 0})
            else:
                g.game_words.remove(word)
                g.player1.words.append({word: len(word)})

            pc_word = choice(g.game_words)
            print(f"{g.player2.name}: {pc_word}")

            g.game_words.remove(pc_word)
            g.player2.words.append({pc_word: len(pc_word)})

        elif g.player1.name == "carl":
            pc_word = choice(g.game_words)
            print(f"{g.player1.name}: {pc_word}")

            g.game_words.remove(pc_word)
            g.player1.words.append({pc_word: len(pc_word)})

            word = input(f"{g.player2.name}: ").lower()

            if word not in g.game_words or word in g.player1.words or word in g.player2.words:
                g.player2.words.append({word: 0})
            else:

                g.game_words.remove(word)
                g.player2.words.append({word: len(word)})

        i += 1

    g.print_game_result()


if __name__ == '__main__':
    run_game()
