from deeppavlov import configs, build_model
from typing import List, Tuple

import logging
from string import punctuation

ner_model = build_model(configs.ner.ner_rus, download=True)


def predict_ner(text: str) -> List[Tuple[str, str]]:
    logging.info('NER prediction started.')
    try:
        prediction = ner_model([text])
        logging.debug(f'NER prediction succeeded. Result: {prediction}')
        ans = _ner_postprocess(predicted_ner=prediction)
        return ans
    except Exception as e:
        logging.error(f'Error occurred: {e}', exc_info=True)


def _ner_postprocess(predicted_ner: List[List[List[str]]]) -> List[Tuple[str, str]]:
    logging.debug(f'Cleaning NER tags started.')
    persons = []
    person_full_name = ''
    word = ''
    ner_continuation: bool = False
    assert len(predicted_ner[0][0]) == len(predicted_ner[1][0]), 'The number of tokens and their tags must match.'

    # Составление единого токена из следующих друг за другом токенов персон, все остальные токены считаются OTHER
    for i in range(len(predicted_ner[1][0])):
        ner_tag = predicted_ner[1][0][i]
        word = predicted_ner[0][0][i]
        if ner_tag == 'B-PER':
            ner_continuation = True
            person_full_name = word
        elif ner_tag == 'I-PER' and ner_continuation:
            part_of_person = word
            # разделение пробелами только между словами
            if part_of_person not in punctuation:
                part_of_person = ' ' + part_of_person
            person_full_name += f'{part_of_person}'
        elif ner_continuation:
            ner_continuation = False
            persons.append((person_full_name, 'PERSON'))
            logging.debug(f'Person founded. Name: "{person_full_name}"')
            person_full_name = ''
        else:
            persons.append((word, 'OTHER'))
    else:
        if ner_continuation:
            persons.append((person_full_name, 'PERSON'))
        else:
            if word:
                persons.append((word, 'OTHER'))
    logging.debug(f'Cleaning NER tags finished successfully.')

    return persons
