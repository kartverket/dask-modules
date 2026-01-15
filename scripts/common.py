import re
from typing import List

def replace_special_characters(s):
    replacements = {
        'æ': 'ae',
        'Æ': 'Ae',
        'ø': 'o',
        'Ø': 'O',
        'å': 'aa',
        'Å': 'Aa'
    }

    return re.sub(r'[æåÆØÅ]', lambda match: replacements[match.group(0)], s)

def is_content_in_file(file_path: str, content: str) -> bool:
    with open(file_path) as file:
        file_content = file.read()
        return file_content.find(content) > -1

