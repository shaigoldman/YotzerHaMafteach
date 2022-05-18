# YotzerHaMafteach
A "Mafteach" (Hebrew for "index") creator tool for talmudic notes and articles.

To use, first convert the notes into a .txt file, as in the example files. Then use the path to generate an automated mafteach using the python script "YotzerHamafteach.py" like so:

        python YotzerHamafteach.py NOTES_NAME.txt OUTPUT_NAME.txt

In order for the processor to work, the notes must fufill two conditions:

(1) all sources are labeled using the standardized Bar Ilan Responsa Project source labeling system. This source label should exist in the notes as its own line, above or below the source. This isn't hard to come by in notes, because generally when you copy+paste a source from the Responsa Project it automatically pastes the source label on its own line above the source.

(2) the notes must be seperated into some form of chapters/sections + subsections so the mafteach knows where to pinpoint your sources to. The system I personally use is Klal (א, ב, ג) Siman (I, II, III...) Sif (א, ב, ג). But this can be adjusted within the source code to fit your needs. In the future I will implement an API so the section indicators won't be directly in the source code. 
