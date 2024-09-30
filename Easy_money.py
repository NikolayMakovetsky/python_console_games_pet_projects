from random import choice

"""
Игровой автомат 'Easy money'

ПРАВИЛА:
В начале игры вам даётся 100 монет
Автомат демонстрирует на экране три карты (две рубашкой вниз, одну рубашкой вверх)
Выигрывает комбинация, при которой карты располагаются слева-направо по возрастанию 
Ваша задача оценить вероятность выпадения выигрышной комбинации и сделать ставку
"""

print("\n----E A S Y  M O N E Y----")

HOTKEYS = "/ СДАТЬ ЗАНОВО: Enter / ВЫХОД: -1 /"
CARDS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
wallet = 100

while True:
    if wallet < 1:
        break
    elif wallet > 0:
        cards = list(CARDS)

        card1 = choice(cards)
        cards.remove(card1)
        card2 = choice(cards)
        cards.remove(card2)
        card3 = choice(cards)

        print(f"У вас {wallet} монет")
        print(f"Сдаю карты...[ {card1}, {card2}, *** ]...карты расположены по-возрастанию? {HOTKEYS}")

        bet = input("Ваша ставка: ")
        try:
            bet = int(bet)
        except ValueError:
            bet = 0
        if bet < 0 or bet > wallet:
            break

        win_message = ""
        if CARDS.index(card1) < CARDS.index(card2) < CARDS.index(card3):
            wallet += bet
            win_message = " ------> ВЫИГРЫШНАЯ КОМБИНАЦИЯ! =)"
        else:
            wallet -= bet

        print(f"Результат...[ {card1}, {card2}, {card3} ]{win_message}")

    print("--------------------------")

print("--------------------------")
print(f"У ВАС В КАРМАНЕ {wallet} монет! =)")
