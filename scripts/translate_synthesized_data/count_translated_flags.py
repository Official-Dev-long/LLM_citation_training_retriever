import json
from collections import Counter

JSON_DIR = "./data/translated_data/pulmonology_case_synthesized_yonghui_translated_7200_9999.jsonl"

def count_translation_flags(jsonl_file):
    """Count true/false values for translated_flag key."""
    counter = Counter()
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                obj = json.loads(line.strip())
                if isinstance(obj, dict) and 'translated_flag' in obj:
                    value = obj['translated_flag']
                    # Convert to string for counting, but preserve boolean
                    counter[bool(value)] += 1
                else:
                    print(f"Warning: Line {line_num} missing 'translated_flag' key")
                    counter['missing'] += 1
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                counter['parse_error'] += 1
                continue
    
    return counter

# Usage
counter = count_translation_flags(JSON_DIR)
print(f"True count: {counter[True]}")
print(f"False count: {counter[False]}")
print(f"Total objects: {counter[True] + counter[False]}")
print(f"Missing flag: {counter['missing']}")
print(f"Parse errors: {counter['parse_error']}")