"""
Curated sample inputs for the GUI and the Test Cases tab.
Each entry records the expected two-layer outcome per the Behavior Matrix.
"""

SAMPLES = [
    # Canonical accepted inputs
    {"input": "00:00",     "formal": True,  "system": True,  "note": "Earliest 24-hour time"},
    {"input": "12:00",     "formal": True,  "system": True,  "note": "24-hour noon"},
    {"input": "12:49",     "formal": True,  "system": True,  "note": "24-hour time"},
    {"input": "23:59",     "formal": True,  "system": True,  "note": "Latest 24-hour time"},
    {"input": "12:49 AM",  "formal": True,  "system": True,  "note": "12-hour time"},
    {"input": "12:00 PM",  "formal": True,  "system": True,  "note": "12-hour noon"},
    # Human variants: Layer 1 rejects, Layer 2 accepts
    {"input": "9:30 am",   "formal": False, "system": True,  "note": "Normalized to 09:30 AM"},
    {"input": "09:30 pm",  "formal": False, "system": True,  "note": "Normalized to 09:30 PM"},
    {"input": "1:05 PM",   "formal": False, "system": True,  "note": "Normalized to 01:05 PM"},
    # Dead state rejections
    {"input": "24:00",     "formal": False, "system": False, "note": "Hour exceeds 23"},
    {"input": "12:60",     "formal": False, "system": False, "note": "Minute exceeds 59"},
    {"input": "13:00 PM",  "formal": False, "system": False, "note": "13 invalid in 12-hour; suffix invalid in 24-hour"},
    {"input": "00:30 AM",  "formal": False, "system": False, "note": "00 invalid in 12-hour"},
    {"input": "09:30AM",   "formal": False, "system": False, "note": "Missing space before AM"},
    {"input": "09:30  AM", "formal": False, "system": False, "note": "Two spaces before AM"},
    # Alphabet check rejections
    {"input": "09-30",     "formal": False, "system": False, "note": "'-' not in the master alphabet"},
    {"input": "09:30 XM",  "formal": False, "system": False, "note": "'X' not in the master alphabet"},
    {"input": "ab:cd",     "formal": False, "system": False, "note": "Letters not in the master alphabet"},
]

# Quick-input buttons shown in the GUI
SAMPLE_BUTTONS = ["12:49 AM", "23:59", "9:30 am", "09:30AM", "24:00", "13:00 PM"]