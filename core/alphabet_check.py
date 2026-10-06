SIGMA_TIME = {
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ':', ' ', 'A', 'M', 'P'
}

def check_alphabet(raw_input: str) -> tuple[bool, list[tuple[int, str]]]: 
    invalid_chars = []
    for index, char in enumerate(raw_input):
        if char not in SIGMA_TIME:
            invalid_chars.append((index, char))
            
    is_valid = len(invalid_chars) == 0
    return is_valid, invalid_chars