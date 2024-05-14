from typing import List, Tuple


def read_code_block(lines: List[str], start_index: int = 0) -> Tuple[str, int]:
    index = start_index
    line = lines[index]
    next_line = lines[index + 1] if index + 1 < len(lines) else ''
    block_lines = [line]

    if '{' in line or next_line.strip(' \n') == '{':
        opened_brackets = line.count('{') - line.count('}') + next_line.count('{') - next_line.count('}')
        while opened_brackets != 0:
            index += 1
            current_line = lines[index]
            block_lines.append(current_line)
            opened_brackets = opened_brackets + current_line.count('{') - current_line.count('}')
            if opened_brackets == 0:
                break
    block_text = '\n'.join(block_lines)

    return block_text, index - start_index
