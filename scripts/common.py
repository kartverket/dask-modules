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

    def replace(match):
        return replacements[match.group(0)]

    return re.sub(r'æ|Æ|ø|Ø|å|Å', replace, s)

def is_content_in_file(file_path: str, content: str) -> bool:
    with open(file_path) as file:
        file_content = file.read()
        return file_content.find(content) > -1


def append_content_to_end_of_file(file_path: str, content: str) -> None:
    lines: List[str] = []
    with open(file_path) as file:
        lines = file.readlines()

    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'

    lines.append(content + '\n')

    with open(file_path, 'w') as file:
        file.writelines(lines)
