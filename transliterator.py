class Transliterate():
    """
    Transliterate class to transliterate text from Cyrillic to Latin

    Ruleset: http://www.eki.ee/books/ekk09/index.php?id=37&p=2&p1=6
    'Vene keele tähestikust eesti tähestikku' 2005.

    Usage:
        Initialize the class:
            foo = Transliterate()
        Call with a list of sentences you'd like to transliterate:
            foo(['Дженни играет с мяц.', 'Яне говорит на телефоне.', 'Рассекречены планы выпуска дешевого iPhone Читать далее'])
            # This Returns -- ['Дженни играет с мяц.', 'Яне говорит на телефоне.', 'Рассекречены планы выпуска дешевого iPhone Читать далее']
    """

    def __call__(self, sentences):
        return self._transliterate(sentences)

    def _transliterate(self, sentences):
        new_sentences = []
        for sentence in sentences:
            converted_sentence = []
            sentence = sentence.split(' ')
            for word in sentence:
                converted_word = ''
                for char_index, char in enumerate(word):
                    transchar = ''
                    if char in self._translit_table:
                        transchar = self._translit_table[char]
                    elif char in self._chars_with_rules:
                        transchar = self._check_rules(word, char, char_index)
                    else:
                        transchar = char

                    converted_word += transchar
                converted_sentence.append(converted_word)
            new_sentences.append(' '.join(converted_sentence))

        return new_sentences

    def _check_rules(self, word, char, char_index):
        """Checks for specific rules for the given transliteration

        Arguments:
            word {string} -- The word in which the character originated from.
            char {string} -- The character about to be transliterated.
            char_index {int} -- The index of the character in the word.
        """
        if char in 'Ее':
            return self._rules_for_e(word, char, char_index)
        elif char in 'Ёё':
            return self._rules_for_jo(word, char, char_index)
        elif char in 'ИиЙй':
            return self._rules_for_i(word, char, char_index)
        elif char in 'Хх':
            return self._rules_for_h(word, char, char_index)
        elif char in 'Ьь':
            return self._rules_for_soft(word, char, char_index)

    def _rules_for_soft(self, word, char, char_index):
        """Checks rules for the cyr softening character
            Returns: [string] -- Returns 'J/j//' based on the rules
        """
        if len(word[char_index+1:]) > 0 and word[char_index+1] not in 'еЕёЁюЮяЯ' and word[char_index+1] in self._vocals_rus:
            char_to_return = self._check_if_upper_and_return(char, 'J')
        else:
            return self._chars_with_rules[char]

        return char_to_return

    def _rules_for_e(self, word, char, char_index):
        """Checks rules for the cyr character 'e'
            Returns: [string] -- Returns 'Je/je/E/e' based on the rules
        """
        if char_index == 0:
            char_to_return = self._check_if_upper_and_return(char, 'Je')
        elif word[char_index - 1] in self._vocals_rus or word[char_index - 1] in 'ЬьЪъ':
            char_to_return = self._check_if_upper_and_return(char, 'Je')
        else:
            char_to_return = self._chars_with_rules[char]

        return char_to_return

    def _rules_for_jo(self, word, char, char_index):
        """Checks rules for the cyr character 'jo'
            Returns: [string] -- Returns 'O/o/Jo/jo' based on the rules
        """
        char_to_return = ''
        if char_index != 0:
            if word[char_index-1] in 'ЖжЧчШшЩщ':
                char_to_return = self._check_if_upper_and_return(char, 'O')

        if char_to_return == '':
            char_to_return = self._chars_with_rules[char]

        return char_to_return

    def _rules_for_i(self, word, char, char_index):
        """Checks rules for the cyr character 'i'
        Returns: [string] -- Returns 'J/j/I/i' based on the rules
        """
        char_to_return = ''
        if len(word) > 1:
            if char_index == 0 and word[char_index + 1] in self._vocals_rus:
                char_to_return = self._check_if_upper_and_return(char, 'J')

        if char_to_return == '':
            char_to_return = self._chars_with_rules[char]

        return char_to_return

    def _rules_for_h(self, word, char, char_index):
        """Checks rules for the cyr character 'h'
        Returns: [string] -- Returns 'Hh/hh/H/h' based on the rules
        """
        char_to_return = ''
        if char_index > 0:
            if word[char_index-1] in self._vocals_rus:
                if len(word) == 2:
                    char_to_return = self._check_if_upper_and_return(
                        char, 'Hh')
                # To avoid keyerror use len(word[char_index+1:])
                elif len(word[char_index+1:]) > 0 and word[char_index+1] in self._vocals_rus:
                    char_to_return = self._check_if_upper_and_return(
                        char, 'Hh')
                elif word[-1] == char:
                    char_to_return = self._check_if_upper_and_return(
                        char, 'Hh')

        if char_to_return == '':
            char_to_return = self._chars_with_rules[char]

        return char_to_return

    @staticmethod
    def _check_if_upper_and_return(char_in_index, char):
        """Checks wheter the character is supposed to be lower or upper case

        Arguments:
            char_in_index {string} -- [The value of the char index in the word]
            char {string} -- [The character to return, should be first letter uppercase, ex: 'Je']

        Returns:
            [string] -- [Upper or lower case version of the character]
        """
        if char_in_index.isupper():
            return char
        else:
            return char.lower()

    # Ugly constants too big for init method
    _vocals_est = ['i', 'ü', 'u', 'e', 'ö', 'õ', 'o', 'ä', 'a']
    _vocals_rus = ['а', 'э', 'ы', 'у', 'о', 'я', 'е', 'ё', 'ю', 'и']
    _translit_table = {
        'А': 'A', 'а': 'a',
        'Б': 'B', 'б': 'b',
        'В': 'V', 'в': 'v',
        'Г': 'G', 'г': 'g',
        'Д': 'D', 'д': 'd',
        #'Е': 'E', 'е': 'e',
        #'Ё': 'Jo', 'ё': 'jo',
        'Ж': 'Ž', 'ж':  'ž',
        'З': 'Z', 'з': 'z',
        #'И': 'I', 'и': 'i',
        #'Й': 'J', 'й': 'j',
        'К': 'K', 'к': 'k',
        'Л': 'L', 'л': 'l',
        'М': 'M', 'м': 'm',
        'Н': 'N', 'н': 'n',
        'О': 'O', 'о': 'o',
        'П': 'P', 'п': 'p',
        'Р': 'R', 'р': 'r',
        'С': 'S', 'с': 's',
        'Т': 'T', 'т': 't',
        'У': 'U', 'у': 'u',
        'Ф': 'F', 'ф': 'f',
        #'Х': 'Kh', 'х':  'kh',
        'Ц': 'Ts', 'ц':  'ts',
        'Ч': 'Ch', 'ч':  'ch',
        'Ш': 'Sh', 'ш':  'sh',
        'Щ': 'Shch', 'щ': 'shch',
        #'Ь': "'", 'ь': "'",
        'Ы': 'õ', 'ы': 'õ',
        'Ъ': "", 'ъ': "",
        'Э': 'E', 'э': 'e',
        'Ю': 'Ju', 'ю': 'ju',
        'Я': 'Ja', 'я': 'ja'}
    _chars_with_rules = {
        'Е': 'E', 'е': 'e',
        'Ё': 'Jo', 'ё': 'jo',
        'И': 'I', 'и': 'i',
        'Й': 'I', 'й': 'i',
        'Х': 'H', 'х':  'h',
        'Ь': "", 'ь': "",
    }


if __name__ == '__main__':
    trans = Transliterate()
    transcribed = trans(['Дженни играет с мяц.', 'Яне говорит на телефоне.',
                         'Рассекречены планы выпуска дешевого iPhone Читать далее',
                         'FOR E: Сергей = Sergei, Петропавловск = Petropavlovsk; aga Егоров = Jegorov, Алексеев = Aleksejev, Мясоедов = Mjassojedov, Васильев = Vassiljev, Подъездов = Podjezdov',
                         'FOR JO: Орёл = Orjol, Пётр = Pjotr; aga Жёлтый = Žoltõi, Пугачёв = Pugatšov, Шёлков = Šolkov, Щёкино = Štšokino',
                         'FOR I: Исаев = Issajev, Филин =Filin; aga Иосиф = Jossif, Иовлев = Jovlev',
                         'FOR H: Хабаровск = Habarovsk, Мохнатый = Mohnatõi, Верхоянск = Verhojansk; aga Чехов = Tšehhov, Тихонов = Tihhonov, Мономах = Mono­mahh, Черных = Tšernõhh, Долгих = Dolgihh',
                         'FOR SOFT: Юрьевец = Jurjevets, Тотьма = Totma, Нинель = Ninel, aga Ильич = Iljitš, Почтальон = Potštaljon, also Иль'])
    for i in transcribed:
        print(i)
