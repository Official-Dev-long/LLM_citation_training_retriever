import json
from collections import defaultdict, Counter

JSON_DIR = "./data/translated_data/pulmonology_case_synthesized_yonghui_translated_0_4999.jsonl"

position_key_counts = defaultdict(Counter)
all_positions = set()
total_objects = 0

with open(JSON_DIR, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line.strip())
            if not obj:
                continue

            obj = obj["translated"]
                
            total_objects += 1
            keys = list(obj.keys())
            
            # Record maximum positions found
            all_positions.update(range(len(keys)))
            
            # Count each key at its position
            for pos, key in enumerate(keys):
                position_key_counts[pos][key] += 1
                
        except json.JSONDecodeError:
            continue

# Print comprehensive statistics
print(f"Total JSON objects: {total_objects}")
print(f"Maximum depth found: {max(all_positions) + 1 if all_positions else 0}")
print(f"Total positions analyzed: {len(position_key_counts)}")

for pos in sorted(position_key_counts.keys()):
    counter = position_key_counts[pos]
    total = sum(counter.values())
    unique_keys = len(counter)
    
    print(f"\n{'='*80}")
    print(f"Position {pos} Statistics:")
    print(f"  Total occurrences: {total}")
    print(f"  Unique keys: {unique_keys}")
    print(f"  Coverage: {total}/{total_objects} objects ({total/total_objects*100:.1f}%)")
    print(f"\n  All keys at position {pos}:")
    
    # Sort by count in descending order
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    
    for key, count in sorted_items:
        percentage = (count / total) * 100
        print(f"    {key}: {count} ({percentage:.1f}%)")