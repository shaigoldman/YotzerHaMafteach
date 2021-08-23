import numpy as np
import SeferNames
import NumericLettersParsers as nlp

MEKOR_STR_MAXLEN=40 # lines with more characters than this won't be considered for mekor marking


#----------DAF NUMBER AND AMUD----------#
def get_amud_str(amud):
    if amud == 'א':
        return '.'
    elif amud == 'ב':
        return ':'
    return ''


def get_dafs(mekor_str):
    words = mekor_str.split(' ')
    dafs = []
    pairs = []
    if 'דף' in words:
        # prob form of דף ה עמוד ב, etc
        where = words.index('דף')
        
    for index, word in enumerate(words):
        if word == 'דף':
            dafs.append(nlp.remove_chucks(words[index+1]))
        elif word == 'עמוד':
            amud = get_amud_str(words[index+1])
            if dafs and amud != '':
                pairs.append(dafs.pop()+amud)
        elif 'ע״' in word or ('ע' + '"') in word:
            amud = get_amud_str(word[-1])
            if amud == '':
                continue
            daf = words[index-1]
            if 'ד' in daf and ('״' in daf or '"' in daf):
                daf = daf[1:]
            pairs.append(nlp.remove_chucks(daf)+amud)
    for lonely_daf in dafs:
        pairs.append(lonely_daf)
    return pairs

#----------RAMBAM PEREK HALACHA----------#
def rambam_perk_halacha(mekor_str):
    words = mekor_str.split(' ')
    pereks = []
    pairs = []
    
    for index, word in enumerate(words):
        if ('״' in word or '"' in word):
            cut = nlp.remove_pref(word, allowed='מבו')
            if cut[0] == 'פ':
                cut = nlp.remove_pref(cut, allowed='פ')
                if nlp.is_numeric(cut, fifty_cap=True):
                    pereks.append(nlp.chuck_with(cut, 'פ'))
            if cut[0] == 'ה': 
                cut = nlp.remove_pref(cut, allowed='ה')
                if nlp.is_numeric(cut, fifty_cap=True):
                    halacha = nlp.chuck_with(cut, 'ה')
                    if pereks:
                        pairs.append(f'{pereks.pop()} {halacha}')
        elif word == 'פרק':
            pereks.append(words[index+1])
        elif word == 'הלכה':
            halacha = words[index+1]
            if pereks:
                pairs.append(f'{pereks.pop()}:{halacha}')
        
    for lonely_perek in pereks:
        pairs.append(lonely_perek)
    return pairs

#----------SHUTIM AND TURIM----------#
def shutim_section(mekor_str):
    
    if len(mekor_str) > MEKOR_STR_MAXLEN:
        return '?'
    
    sect_str = ''
    words = mekor_str.split(' ')
    for index, word in enumerate(words):
        for sign in [*SeferNames.cheleks, *SeferNames.simans,
                     *SeferNames.siifs, *SeferNames.sifkatans]:
            if sign in word:
                if sign == 'סעיף' and words[index+1] == 'קטן':
                    word = 'סעיף קטן'
                    index += 1
                if sect_str:
                    sect_str += ' '
                sect_str += word
                if not nlp.has_chuck(word) or sign in SeferNames.sifkatans:
                    sect_str += ' '
                    sect_str += words[index+1]
    return sect_str


def tur_is_really_a_shut(mekor_str, tur_str):
    for shut in SeferNames.all_sfarim['shutim']:
        if (shut in mekor_str and np.abs(
             mekor_str.index(shut) -  mekor_str.index(tur_str)) < 30):
            return True
    return False


#----------GENERAL IDENTIFIER----------#
def get_sefer_name(mekor_str):
    
    # this is a basic inconsistency i have that should be fixed
    mekor_str = mekor_str.replace('השגת', 'השגות')
    
    for label, sefer_names in SeferNames.all_sfarim.items():
        for sefer in sefer_names:
             if sefer in mekor_str:
                if label == 'sfarim_chizonim':
                    return sefer
                elif label == 'turim':
                    if tur_is_really_a_shut(mekor_str, sefer):
                        continue
                    return mekor_str[:mekor_str.index(sefer)]
                elif label == 'shutim':
                    for sectioner in [*SeferNames.cheleks, *SeferNames.simans]:
                        if sectioner in mekor_str:
                            return mekor_str[:mekor_str.index(sectioner)]
                elif label == 'rambam':
                    for halacha_str in [' הלכות ',"הל' ", 'הל׳',]:
                        if halacha_str in mekor_str:
                            mekor_str = mekor_str.replace(halacha_str, '')
                    return mekor_str[:mekor_str.index(sefer)]
                elif label == 'mesechtot':
                    if 'מסכת' in mekor_str:
                        name = mekor_str[:mekor_str.index('מסכת')]
                    elif sefer == mekor_str.split(' ')[0]:
                        name = 'תלמוד בבלי'
                    else:
                        name = mekor_str[:mekor_str.index(sefer)]
                    if 'תלמוד בבלי' in name:
                        name = 'גמרא'
                    if 'חידושי' in name:
                        name = name.replace('חידושי ה', '')
                    return name
    return '?'