import SeferNames
import SectionNames
import numpy as np
import NumericLettersParsers as nlp

def reorder(these_sfarim, priorities):

    order = np.argsort(priorities)
    these_sfarim = these_sfarim.iloc[order]
    
    # put ordering into big df
    indicies = these_sfarim.index
    these_sfarim.index = range(len(these_sfarim))
    return these_sfarim


def get_summed_priorities(*priorities):
    summed_priority = np.zeros(len(priorities[0]))
    multiplier = 100 ** (len(priorities)-1)
    for priority in priorities:
        priority = np.asarray(priority)
        summed_priority += priority*multiplier
        multiplier /= 100
    return summed_priority


def klal_siman_sif_priority(mekorot_df):
    
    klalim_order = np.array(
        [SectionNames.klalim.index(klal) for klal in mekorot_df['klal']])
    
    simanim_order = np.array(
        [SectionNames.simanim.index(siman) for siman in mekorot_df['siman']])
    
    sifim_order = np.array(
        [SectionNames.sifim.index(siman) for siman in mekorot_df['sif']])
    
    return (klalim_order, simanim_order, sifim_order)


def sort_shas(mekorot_df):
    # get the mesechets out of the big df
    mesechets = mekorot_df[mekorot_df['type'] == 'mesechtot']
    
    # order by order of shas
    mesechets_order = np.array(
        [SeferNames.shas.index(section) for section in mesechets['section']])
    
    # put the commentaries on the rif in the back
    rif_commentaries = ['ר״ן על', 'ספר הזכות', 'מלחמת', 'כתוב שם', 'המאור', 'רי״ף']
    SeferNames.add_alt_chkchk(rif_commentaries)
    rif_priority = np.array(
        [len(rif_commentaries) -
          [*[rishon in sefer for rishon in rif_commentaries], 
            True].index(True)
         for sefer in mesechets['sefer']])
    
    # order by daf
    daf_order = np.array(
        [nlp.daf_numerical(daf_str) for daf_str in mesechets['where']])
    
    # order gemara first then commentaries
    gemara_first_priority = np.array(
        [sefer != 'גמרא' for sefer in mesechets['sefer']]).astype(int)
    
    # order some of the main commentaries first
    main_rishonim = ['רש״י', 'תוס', 'רמב״ן', 'רשב״א', 'ריטב״א']
    SeferNames.add_alt_chkchk(main_rishonim)
    rishonim_priority = np.array(
        [[*[rishon in sefer for rishon in main_rishonim], 
            True].index(True)
         for sefer in mesechets['sefer']])
    
    # alphabetize to group commentaries with same name
    # -> helpful for sorting תוס ראש  and other תוס and such
    a_sorted = np.sort(mesechets['sefer']).tolist()
    alphabetical_priority = np.array(
                [a_sorted.index(sefer) for sefer in mesechets['sefer']])
    
    
    summed_priorities = get_summed_priorities(
        mesechets_order, rif_priority,
        daf_order, gemara_first_priority,
        rishonim_priority, alphabetical_priority
    )
    
    return reorder(mesechets, summed_priorities)


def sort_rambam(mekorot_df):
    
    rambams = mekorot_df[mekorot_df['type'] == 'rambam']
    
    
    # order by section
    halachas_order = np.array(
        [SeferNames.all_sfarim['rambam'].index(section) for section in rambams['section']]) * 100
    
    # order by perek halacha
    halacha_priority = np.array(
                [nlp.perek_halacha_numerical(where) for where in rambams['where']]) * 100
    
    # known ordering of sfarim
    known_sfarim = ['רמב״ם', 'השגות הראב״ד',
                    'מגיד משנה', 'מ״מ', 'כסף משנה', 'כס״מ',
                    'משנה למלך',
                   ]
    SeferNames.add_alt_chkchk(known_sfarim)
    known_priority = np.array(
        [[*[sf in sefer for sf in known_sfarim], 
            True].index(True)
         for sefer in rambams['sefer']])
    
    # alphabetize to group commentaries with same name
    a_sorted = np.sort(rambams['sefer']).tolist()
    alphabetical_priority = np.array(
                [a_sorted.index(sefer) for sefer in rambams['sefer']])
     
    summed_priorities = get_summed_priorities(
        halachas_order, halacha_priority, known_priority, alphabetical_priority
    )
    
    return reorder(rambams, summed_priorities)


def sort_section(mekorot_df, typ):
    if typ == 'mesechtot':
        return sort_shas(mekorot_df)
    elif typ == 'rambam':
        return sort_rambam(mekorot_df)
    
    # get the section out of the big df
    these_sfarim = mekorot_df[mekorot_df['type'] == typ]
    
    # alphabetize to group commentaries with same name
    a_sorted = np.sort(these_sfarim['sefer']).tolist()
    alphabetical_priority = np.array(
                [a_sorted.index(sefer) for sefer in these_sfarim['sefer']])
    
    return reorder(these_sfarim, alphabetical_priority)