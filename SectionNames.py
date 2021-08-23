""" This Python file defines the character patterns that are used in the 
    notes to denote article/section/subsections. It can be adjusted as needed.
    In my system: Klal=article, siman=section, sif=subsection.
"""
import numpy as np

klalim = [f'כלל {כ}' for כ in 'אבגדהוזחטי']
klalim.extend([f'כלל י{כ}' for כ in 'אבגד'])
klalim.extend([f'כלל ט{כ}' for כ in 'וז'])
klalim.extend([f'כלל י{כ}' for כ in 'זחט'])
klalim.extend([f'כלל כ{כ}' for כ in ' אבגדהוזחט'])

simanim = np.asarray([[f'I{x}.', f'{x}.', f'{x}I.', f'{x}II.', f'{x}III.'] 
                      for x in ['I', 'V', 'X', 'XV']]).flatten().tolist()
simanim.append('XIV.')
simanim.insert(4, 'נספח')

sifim = [f'{x}.' for x in 'אבגדהוזחטי']
sifim.extend([f'י{x}.' for x in 'אבגדזחט'])
sifim.extend([f'ט{x}.' for x in 'וז'])
sifim.extend([f'כ{x}.' for x in ' אבגדהוזחט'])

# this just evens out the lengths for loopings
while len(simanim) < len(klalim):
    simanim.append(simanim[-1])
simanim = np.asarray(simanim)
simanim = simanim[np.argsort([len(siman) for siman in simanim])]