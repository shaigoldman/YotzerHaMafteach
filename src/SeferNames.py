def add_alt_chkchk(str_list):
    """ I want to allow for the two methods of using the
        hebrew 'chuck-chuck' character: " and ״. So lets
        add to our sefer names a copy of every name with
        each kind of chuck.
    """
    old_list = str_list.copy()
    insertions = 0
    for index, word in enumerate(old_list):
        if '״' in word:
            alt = word[:word.index('״')] + '"' + word[word.index('״')+1:]
            str_list.insert(index+insertions, alt)
            insertions += 1


torah = ['בראשית', 'שמות', 'ויקרא', 'במדבר', 'דברים',
            ]
shas = [ 'ברכות', 'פאה', 'דמאי', 'כלאים', 'שביעית', 'תרומות', 'מעשרות',
              'מעשר שני', 'חלה', 'ערלה', 'ביכורים', 'שבת', 'עירובין', 'פסחים',
              'שקלים', 'יומא', 'סוכה', 'ביצה', 'ראש השנה', 'תענית', 'מגילה',
              'מעוד קטן', 'חגיגה', 'יבמות', 'כתובות', 'נדרים', 'נזיר', 'סוטה',
              'גיטין', 'קידושין', 'בבא קמא', 'בבא מציעא', 'בבא בתרא', 'סנהדרין',
              'מכות', 'שבועות', 'עדיות', 'עבודה זרה', 'אבות', 'הוריות', 'זבחים',
              'מנחות', 'חולין', 'בכורות', 'ערכין', 'תמורה', 'כריתות', 'מעילה',
              'תמיד', 'מדות', 'קנים', 'כלים', 'אהלות', 'נגעים', 'פרה',
              'טהרות', 'מקואות', 'נדה', 'מכשירין', 'זבים', 'טבול יום', 'ידים',
              'עוקצין', 'מע״ש', 'ר״ה', 'ב״ק', 'ב״מ', 'ב״ב', 'ע״ז',
              'טב״י'
            ]
mesechtot = [x for x in shas]
add_alt_chkchk(mesechtot)

rambam_sections = [ 'יסודי התורה', 'דעות', 'תלמוד תורה', 'עבודה זרה', 'תשובה', 
           'קריאת שמע', 'תפילה', 'ברכת כהנים', 'תפילין', 'מזוזה', 
           'ספר תורה', 'ציצית', 'ברכות', 'מילה', 'שבת', 'עירובין',
           'שביתת עשור', 'שביתת יום טוב', 'שביתת יו״ט', 'חמץ ומצה', 'חו״מ',
           'שופר', 'סוכה', 'לולב', 'שלקים', 'קידוש החדש', 'תענית',
           'מגילה', 'חנוכה', 'אישות', 'גירושין', 'יבום',
           'חליצה', 'נערה בתולה', 'סוטה', 'שוטה', 'איסורי ביאה', 
           'אי״ב', 'א״ב', 'שחיטה', 'מאכלות אסורות', 'מ״א',
           'מאכ״א', 'שבועות', 'נדרים', 'נזירות', 'ערכים', 
           'חרמים', 'כלאים', 'מתנות עניים', 'תרומות', 'מ״ע', 
           'תרומות', 'מעשרות', 'מעשר שני', 'מע״ש', 'נטע רביעי',
           'נ״ר', 'ביכורים', 'שמיטה', 'יובל', 'שאר מתנות כהונה',
           'בית הבחירה', 'כלי מקדש', 'ביאת מקדש', 'איסורי מזבח', 'אי״מ',
           'מעשה הקרבנות', 'מעה״ק', 'תמידים ומוספין', 'פסולי המוקדשין', 
           'עבודת יום הכפורים', 'מעילה', 'קרבן פסח', 'ק״פ', 'חגיגה',
           'בכורות', 'שגגות', 'מחוסרי כפרה', 'תמורה', 'טומאת מת',
           'פרה אדומה', 'טומאת צרעת', 'מטמאי משכב ומושב', 
           'שאר אבות הטומאות', 'שא״ה', 'טומאת אוכלים', 'כלים', 
           'מקואות', 'נזקי ממון', 'גניבה', 'גזילה ואבידה', 'חובל ומזיק',
           'חובל ומזיק', 'חובל', 'רוצח ושמירת נפש', 'רוצח', 'מכירה',
           'זכייה ומתנה', 'שכנים', 'שלוחין ושותפין', 'שותפין', 'עבדים',
           'שכירות', 'שאלה ופיקדון', 'מלווה ולווה', 'טוען ונטען', 'נחלות', 
           'סנהדרין', 'עדות', 'ממרים', 'אבל', 'מלכים',
         ]
add_alt_chkchk(rambam_sections)

turim = [ 'אורח חיים', 'יורה דעה', 'אבן העזר', 'חושן משפט', 
          'או״ח', 'יו״ד', 'אה״ע', 'חו״מ',
          'א״ח', 'י״ד', 'א״ה', 'ח״מ',
          'חו"מ', 'אה"ע', 'יו"ד', 'או"ח',
          'ח"מ', 'י"ד', 'א"ה', 'ח"מ'
        ]
shutim = ['שו"ת', 'שו״ת']
sfarim_chizonim = [ 'מקדש דוד', 'בה״ג', 'בעל הלכות גדולות', 'הלכות גדולות', 'מנחת חינוך', 
                    'מנ״ח', 'עיטור',
                    'ספר התרומה', 'תורת האדם', 'קונטרס דיני דגרמי', 'קרית ספר', 
                    'אבודרהם', 'כלבו', 'כל בו', 'חינוך',
                    'מחנה אפריים', 'ארץ הצבי', 'מנחת אביב', 'אנציקלופדיה תלמודית', 
                    'ספר הישר לר״ת (חלק החידושים)'
                    'עלון שבות', 'המקח והממכר', 'ספר הישר',
                    'קובץ שיעורים', 'קבצ״ש',
                    'תרומת הדשן',
                    'מכילתא', 'תורת כהנים', 
                   # these shulchan aruch commentaries which are only on
                   # one of the four turim
                    'אבני מילואים', 'קצות החושן', 'קצה״ח', 'אב״מ', 'נתיבות המשפט', 
                    'נתיבות', 'בית שמואל', 'חלקת מחוקק', 'סמ״ע', 'ספר מאירת עיניים',
                    'כרתי', 'פלתי', 'מקור חיים', 'אורים', 'תומים',
                  ]

all_sfarim = {'mesechtot': mesechtot, 
             'rambam': rambam_sections, 
             'turim': turim,
             'shutim': shutim, 
             'sfarim_chizonim': sfarim_chizonim}

cheleks = ['חלק', 'ח״', 'ח\"']
simans = ['סימן', 'סי׳', "'סי"]
siifs = ['סעיף',  'סע\'', 'סע׳']
sifkatans = ['ס״ק', 'ס"ק', 'סעיף קטן']
