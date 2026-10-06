from core.alphabet_check import check_alphabet
from core.normalizer import normalize

test_cases = [
    "23:45",       # Perfect canonical
    "9:30 am",     # Needs N2 and N1
    "09:30 pm",    # Needs N1
    "12:00",       # Perfect canonical
    "09:30AM",     # Missing space (Normalizer should ignore, DFA will reject later)
    "ab:cd"        # Alphabet check should catch 'a', 'b', 'c', 'd'
]

for raw in test_cases:
    print(f"Raw: '{raw}'")
    
    # Layer 1 on Raw
    is_valid_raw, invalids = check_alphabet(raw)
    print(f"  Layer 1 (Raw): {'PASS' if is_valid_raw else 'FAIL'} {invalids}")
    
    # Layer 2
    norm = normalize(raw)
    print(f"  Normalized: '{norm}'")
    
    # Layer 1 on Normalized
    is_valid_norm, invalids_norm = check_alphabet(norm)
    print(f"  Layer 1 (Norm): {'PASS' if is_valid_norm else 'FAIL'} {invalids_norm}")
    print("-" * 40)