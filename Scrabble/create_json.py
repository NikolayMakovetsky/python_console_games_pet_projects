in_path = 'russian_nouns.txt'
out_path = 'rus_nouns.json'

try:
    with open(in_path, 'r', encoding="utf-8") as infile, open(out_path, 'w', encoding="utf-8") as outfile:

        outfile.write("[")
        while True:
            f_str = infile.readline().strip()
            outfile.write(f'"{f_str}"')
            if f_str == 'ящурка':
                outfile.write("]")
                break
            else:
                outfile.write(", ")
except FileNotFoundError:
    print("Ошибка при работе с файловой системой")
