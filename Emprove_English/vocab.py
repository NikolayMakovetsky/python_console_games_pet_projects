import glob

from category import Category
from wordcard import WordCard


class Vocab:
    BASE_DIR = '.\\data\\'
    FILE_PATTERN = '_vocab.txt'

    def __init__(self, base_dir: str = BASE_DIR, file_pattern: str = FILE_PATTERN):
        self.base_dir: str = base_dir
        self.file_pattern: str = file_pattern
        self.topics: list[str] = self.get_topics()
        self.files: list = self.get_list_of_files()
        self.cards_is_empty: bool = True
        self.cards: dict[int:[WordCard]] = self.get_dict_with_cards()
        self.categories_with_weights: list[Category] = self.get_categories_with_weights()
        self.success_cards: [WordCard] = []
        self.fail_cards: [WordCard] = []

    def get_list_of_files(self):
        lst = []
        for filename in glob.glob(f'{self.base_dir}*{self.file_pattern}'):
            cut_filename, _ = filename.split('_')
            *_, topic = cut_filename.split('\\')
            if topic in self.topics:
                lst.append(filename)
        return lst

    def get_topics(self) -> list[str]:
        topics = []
        for filename in glob.glob(f'{self.base_dir}*{self.file_pattern}'):
            cut_filename, _ = filename.split('_')
            *_, topic = cut_filename.split('\\')
            topics.append(topic)
        print("--------------------------")
        print(f'SELECT TOPICS')
        for idx, t in enumerate(topics):
            print(f'Topic({idx}): {t}')

        print(f'Input topic numbers or keyword "all" to select all topics at once')
        available_topic_nums = [x for x in range(len(topics))]
        while True:
            user_input = input("Input: ")
            if user_input.strip().lower() == "all":
                checked_topic_nums = available_topic_nums
                break
            chosen_topic_nums = user_input.split()
            checked_topic_nums = []
            for t_num in chosen_topic_nums:
                if t_num.isdigit():
                    if int(t_num) in available_topic_nums and int(t_num) not in checked_topic_nums:
                        checked_topic_nums.append(int(t_num))

            if checked_topic_nums:
                break

        checked_topic_nums.sort()
        print('= ' + ', '.join([str(x) for x in checked_topic_nums]))

        lst = []
        for checked_num in checked_topic_nums:
            lst.append(topics[checked_num])
        res = ', '.join(lst)

        output_topics = []
        for idx, tpc in enumerate(topics):
            if idx in checked_topic_nums:
                output_topics.append(tpc)

        return output_topics

    def get_dict_with_cards(self):

        card_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

        for file in self.files:
            category_name = file.rstrip(self.file_pattern).lstrip(self.base_dir)

            with open(file, mode='r', encoding='utf-8') as f:
                for index, line in enumerate(f):
                    line = line.strip()
                    if line and '-' in line:
                        if line.count('*') > 5:
                            card_rate = 5
                        else:
                            card_rate = line.count('*')

                        line = line.replace('*', '')
                        card_face, card_back = [x.strip().lower() for x in line.split('-')]

                        topic = ""
                        for t in self.topics:
                            if t in f.name:
                                topic = t
                                break

                        w_card = WordCard(filename=file,
                                          line_idx=index,
                                          category=category_name,
                                          topic=topic,
                                          face=card_face,
                                          back=card_back,
                                          rate=card_rate)

                        card_dict[card_rate].append(w_card)
                        self.cards_is_empty = False
        return card_dict

    def get_categories_with_weights(self) -> list[Category]:

        category_list = []
        for k, v in self.cards.items():
            category_list.append(Category(rate=k, quantity=len(v), weight=0.1666666666666666666666666))

        return category_list
