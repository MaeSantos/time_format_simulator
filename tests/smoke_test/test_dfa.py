from core.automaton import simulate
from core.trace import format_trace_table, get_trace_summary

test_inputs = [
    "23:45",       # Accepted (24-hour)
    "09:30 AM",    # Accepted (12-hour)
    "12:00",       # Accepted (24-hour)
    "09:30AM",     # Rejected (Missing space, hits dead state)
    "25:00",       # Rejected (Invalid hour, hits dead state)
    "12:60",       # Rejected (Invalid minute tens, hits dead state)
]

for text in test_inputs:
    print(f"Testing: '{text}'")
    result = simulate(text)
    
    print(f"  Accepted: {result['accepted']}")
    print(f"  Final State: {result['final_state']}")
    print(f"  Summary: {get_trace_summary(result['final_state'], result['accepted'])}")
    
    # Print the last 3 steps of the trace to see where it failed/succeeded
    table = format_trace_table(result['trace'])
    for row in table[-3:]:
        print(f"    Step {row['Step']}: Read {row['Read Symbol']} -> {row['Current State']} to {row['Next State']}")
    print("-" * 50)