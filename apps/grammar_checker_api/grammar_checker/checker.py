from spellchecker import SpellChecker
import json
from pprint import pprint


class AMSpellChecker:
    def __init__(self, text: str):
        self.text = text
        self.main_config_path = "grammar_checker/config.json"
        self.am_words_path, self.am_config_path = self.get_paths()
        self.endings, self.symbols_to_ignore, self.symbols_to_change = self.read_am_config()

    @staticmethod
    def read_json(path: str) -> dict:
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    def get_paths(self):
        data = self.read_json(self.main_config_path)
        return data["paths"]["am_words"], data["paths"]["am_config"]

    def read_am_config(self):
        data = self.read_json(self.am_config_path)
        return data["endings"], data["symbols_to_ignore"], data["symbols_to_change"]

    def remove_symbols_to_ignore(self):
        for symbol in self.symbols_to_ignore:
            self.text = self.text.replace(symbol, "")

    def change_symbols_to_change(self):
        for symbol in self.symbols_to_change:
            self.text = self.text.replace(symbol[0], symbol[1])

    def check_endings_for_delete(self, word: str, spell) -> bool:
        for endswith in self.endings:
            if word.endswith(endswith):
                root_word = word[:-len(endswith)]
                if not spell.unknown([root_word]):
                    return True
        return False

    def check_endings_for_change(self, word: str, spell) -> bool:
        for endswith in self.endings:
            if word.endswith(endswith):
                root_word = word[:-len(endswith)]
                for new_endswith in self.endings:
                    if new_endswith != endswith:
                        new_word = root_word + new_endswith
                        if not spell.unknown([new_word]):
                            return True
        return False

    def check_words(self, words: list, spell) -> dict:
        unknown_words = {}
        for word in words:
            if spell.unknown([word]):
                if not self.check_endings_for_delete(word, spell) and not self.check_endings_for_change(word, spell):
                    candidates = spell.candidates(word)
                    if candidates is not None:
                        unknown_words[word] = list(candidates)
                    else:
                        unknown_words[word] = None

        return unknown_words

    def main(self):
        spell = SpellChecker(language=None)
        spell.word_frequency.load_text_file(self.am_words_path)

        self.remove_symbols_to_ignore()
        self.change_symbols_to_change()

        words = self.text.split()
        unknown_words = self.check_words(words, spell)

        return unknown_words


if __name__ == '__main__':
    user_text = "Արմենիան հայտն է իր գեղեիկ լեռներով, հնագույն եկեղեցիներով և համեղ խոհանոցով: Մարդիկ այստեղ շատ հյուրընկալ են, իսկ մշակույթը՝ հարուստ և բազմազան:"
    print(len(user_text.split()))
    checker = AMSpellChecker(user_text)
    pprint(checker.main())
