import re

pattern_1 = re.compile(r'[А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+') #"Ф И О"
pattern_2 = re.compile(r'[А-Я][а-я]+ [А-Я]\.[А-Я]\.') # "Ф И.О."
pattern_3 = re.compile(r'[А-Я][а-я]+ [А-Я][а-я]+') # "Ф И"

person_patterns = [pattern_1,pattern_2,pattern_2]

def get_person(person):
    for pattern in person_patterns:
        m = pattern.search(person)
        if m:
            return m.group(0)
    return None
