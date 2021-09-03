"""Hebrew Letter-Based Numering Identifiers and Quantifiers"""

def remove_chucks(hebrew_word) -> str:
    """ Hebrew numbering systems use 'chuck-chucks' (aka quotation
        marks that aren't being used to signify a quotation) 
        in between letters that are meant as numerics rather 
        than words. To make it easier to interpret their numeric 
        value we may often want to remove the chuck to better read 
        the value of the actual letters. This function does that.
    """
    for chuck in ['״', '׳', '"', "'"]:
        while chuck in hebrew_word:
            hebrew_word = (hebrew_word[:hebrew_word.index(chuck)] 
                           + hebrew_word[hebrew_word.index(chuck)+1:])
    return hebrew_word


def chuck_with(word, prefix) -> str:
    """ This combines a word with a prefix and then readjusts the
        'chuck-chuck' so it is in between the last two letters as
        is standard in hebrew writing.
    """
    word = remove_chucks(word)
    word = prefix + word
    word = word[:-1] + '״' + word[-1]
    return word


def has_chuck(word) -> bool:
    """ Returns True if there is a chuck-chuck in the
        word str. A function is neccesary because different
        ascii characters can represent chuck-chucks in hebrew.
    """
    return ("'" in word
            or '"' in word
            or '״' in word)


def can_be_prefix(letter, place) -> bool:
    """ In hebrew writing, some letters can serve as
        word prefixes, and should be discounted when
        considering the numeric value of the whole word.
        This returns True if the letter in the given
        position of the str can be a prefix.
    """
    first_only = 'בכמלו'
    can_be_seconds = 'השד'
    if place <=2 and letter in can_be_seconds:
        return True
    elif place == 1 and letter in first_only:
        return True
    return False


def is_numeric(hebrew_word, allow_prefix=False, fifty_cap=False,
               allow_hundreds=True) -> bool:
    """ Determines if a hebrew word may actually be not a word at
        all, but just a numeric placeholder.
        
        Args:
            hebrew_word (str): the word in question.
            allow_prefix (bool): if True, will ignore certain
                 letters at the start of the word if they can
                 be assumed as grammatical prefixes.
            fifty_cap (bool): if True, if the word can only form
                 a number over fifty, it will be considered
                 non-numeric.
            allow_hundreds (bool): since it is rare to have values
                 over 100 represented by hebrew letters, pass false
                 to return True if the only possible numeric values
                 are above 100.

        Returns:
            True if it is possible for this word to be a number,
            False otherwise.
    """
    ones = 'אבגדהוזחט'
    tens = 'יכלמנסעפצ'
    hundreds = 'קרשת'
    if fifty_cap:
        tens = 'יכלמנ'
        allow_hundreds=False
    hebrew_word = remove_chucks(hebrew_word)
    current_place = 100
    prev_letter = 'ת'
    for index, letter in enumerate(hebrew_word):
        if allow_prefix and can_be_prefix(letter, index+1):
            continue
        elif letter in hundreds:
            if not allow_hundreds:
                return False
            elif current_place <= 100:
                return False
            elif hundreds.index(prev_letter) < hundreds.index(letter):
                return False
            elif (hundreds.index(prev_letter) == hundreds.index(letter)
                  and letter != 'ת'):
                return False
        elif letter in tens:
            if current_place <= 10:
                return False
            current_place = 10
        elif letter in ones:
            if current_place <= 1:
                return False
            current_place = 1
        else:
            return False
        prev_letter = letter
    return True


def remove_pref(h_str, allowed='מבו') -> str:
    if h_str[0] == 'ו':
        h_str = h_str[1:]
    if h_str[0] in allowed:
        h_str = h_str[1:]
    return h_str


def gematria(letters_str):
    value = 0
    ones = 'אבגדהוזחט'
    for ot in ones:
        if ot in letters_str:
            value += (ones.index(ot)+1)
    tens = 'יכלמנסעפצ'
    for ot in tens:
        if ot in letters_str:
            value += (tens.index(ot)+1) * 10
    hunds = 'קרשת'
    for ot in hunds:
        if ot in letters_str:
            value += (hunds.index(ot)+1) * 100
    return value


def daf_numerical(daf_str):
    value = gematria(daf_str)
    if ':' in daf_str:
        value += .5
    return value


def perek_halacha_numerical(ph_str):
    if ':' in ph_str:
        perek, halacha = ph_str.split(':') 
    else:
        perek = ph_str
        halacha = ''
    perek_value = gematria(perek)
    halacha_value = gematria(halacha)
    total_value = perek_value + halacha_value/100.
    return total_value
