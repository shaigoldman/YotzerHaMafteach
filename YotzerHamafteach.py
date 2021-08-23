import argparse
import numpy as np
import pandas as pd
# my stuff
import LoadTxt
import SourceParsers as sp
import SeferSort as ss
import SeferNames
from SectionNames import klalim, simanim, sifim

def build_mafteach(text):
    """ Builds a Mafteach based on the given hebrew text.

        Args:
            text (list of str): List of strings where each
                item is a line of text.

        Returns:
            list of pd.DataFrames, each including a different
            kind of mafteach.
    """
    #------Variables for the tracking
    this_klal = None
    this_siman = None
    this_sif = None
    mekorot = []
    #-------Find the mekorot
    for line in text:
        #------Check if it is a new klal, siman or sif
        for klal in klalim:
            if klal in line:
                if (len(line) <= line.index(klal)+len(klal)
                        or line[line.index(klal)+len(klal)] == '.'):
                    this_klal = klal
        for siman in simanim:
            if siman in line:
                if '.' in siman:
                    siman = siman[:-1]
                this_siman = siman # take off the period
                this_sif = '-'

        for sif in sifim:
            if sif in line and len(line)<50:
                this_sif = sif[:-1] # take off the period

        if len(line) > sp.MEKOR_STR_MAXLEN:
            continue
        #------Check if there is a mekor here
        for label, sefer_names in SeferNames.all_sfarim.items():
            # ^ "sefer_names" is not a super accurate variable descript
            #   unfortunately, because for example חידושי הריטב״א סוכה is
            #   being identified under the "sefer_name" סוכה with this alg.
            for sefer in sefer_names:
                if sefer in line:

                    where = ['']
                    section = []

                    if label == 'mesechtot':
                        where = sp.get_dafs(line)
                        if where == ['']:
                            # This is probably not a real mekor, just the notes
                            # mention something general about מסכת מעילה etc.
                            continue
                        section = sefer#sefer[sefer.index(' ')+1:]
                    if label == 'rambam':
                        where = sp.rambam_perk_halacha(line)
                        section = sefer
                    elif label == 'turim':
                        if sp.tur_is_really_a_shut(line, sefer):
                            continue
                    elif label == 'shutim':
                        where = sp.shutim_section(line)
                    elif label == 'sfarim_chizonim':
                        shut_sect = sp.shutim_section(line)
                        if shut_sect:
                            where = shut_sect
                        else:
                            where = line[line.index(sefer)+len(sefer)+1:]

                    text_start = line.index(sefer) - 15
                    if text_start < 0: text_start = 0
                    text = line[text_start:line.index(sefer) + 35]

                    sefer_name = sp.get_sefer_name(line).replace('״', '"')
                    while len(sefer_name)>1 and sefer_name[-1] == ' ':
                        sefer_name = sefer_name[:-1]

                    if type(where) != list: where = [where]
                    if type(section) != list: section = [section]
                    while len(section) < len(where):
                        section.append('')

                    for w, s in zip(where, section):
                        mekor = pd.DataFrame({
                                    'text': [text], 'type': [label],
                                    'sefer': [sefer_name],
                                    'section': [s],
                                    'klal': [this_klal], 'siman': [this_siman],
                                    'sif': [this_sif],
                                    'where': [w]})
                        mekorot.append(mekor)
    #-------Turn it into a DataFrame
    key = pd.concat(mekorot)
    key.index = range(len(key))
    #-------Sort
    type_sort = np.argsort([list(SeferNames.all_sfarim.keys()).index(typ) for typ in key['type']])
    key = key.loc[type_sort]
    key.index = range(len(key))

    keys = []
    for typ in key['type'].unique():
        keys.append(ss.sort_section(key, typ))

    for key_num, key in enumerate(keys):
        keys[key_num] = key[['sif', 'siman', 'klal', 'sefer', 'where', 'section', 'type']]
        # blank repeated refrences
        for rownum, (index, row) in enumerate(keys[key_num].iterrows()):
            row = row[['klal', 'siman', 'sif', 'sefer', 'where', 'section']]
            for label, item in row.iteritems():
                go_backs = 1
                while rownum-go_backs>0 and keys[key_num].iloc[rownum-go_backs][label] == '':
                    go_backs += 1

                if (rownum-go_backs>=0
                    and (item == keys[key_num].iloc[rownum-go_backs][label])
                    and item != '-'):
                    # dont blank repeat siman/sif unless
                    # its a repeat klal etc
                    if label == 'siman' or label == 'sif':
                        if not keys[key_num].loc[index, 'klal'] == '':
                            continue
                    if label == 'sif':
                        if not keys[key_num].loc[index, 'siman'] == '':
                            continue
                    # do the blanking
                    keys[key_num].loc[index, label] = ''

    return keys


def save_mafteach(keys, savename='mafteach'):
    """" Saves the outputted Mafteach from build_mafteach to an xcel sheet."""
    if not '.' in savename:
         savename += '.xlsx'
    with pd.ExcelWriter(savename) as writer:
         for key in keys:
            typ = key.pop('type').unique()[0] 
            key.to_excel(excel_writer=writer, sheet_name=typ)
    print(f'Saved Mafteach to {savename}')

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input_file', metavar='f.txt', type=str,
                        default='', nargs='?',
                        help='The input notes file to create a mafteach from')
    parser.add_argument('output_file', metavar='f.xlsx', type=str,
                        default='', nargs='?',
                        help='The output xlsx file to send the mafteach into')
    args = parser.parse_args()

    
    if args.input_file == '':
        text = LoadTxt.load_sample(1)
    else:
        text = LoadTxt.load_txt(args.input_file)

    keys = build_mafteach(text)

    if args.output_file == '':
        save_mafteach(keys)
    else:
        save_mafteach(keys, args.output_file)


