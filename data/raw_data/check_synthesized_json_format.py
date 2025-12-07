import json

def validate_jsonl_format(file_path):
    """
    Validate that all JSON items follow the exact format:
    {
        "id": int,
        "name": str,
        "gender": str,
        "age": int,
        "medical_history": list,
        "lifestyle_factor": list,
        "vaccination_history": list,
        "family_history": list,
        "disease": str,
        "level": str,
        "symptom": {
            "symptoms": list,
            "duration": str
        },
        "examination_results": dict
    }
    """
    
    # Expected structure with required keys and value types
    EXPECTED_STRUCTURE = {
        "id": int,
        "name": str,
        "gender": str,
        "age": int,
        "medical_history": list,
        "lifestyle_factor": list,
        "vaccination_history": list,
        "family_history": list,
        "disease": str,
        "level": str,
        "symptom": dict,  # Will check nested structure separately
        "examination_results": dict
    }
    
    # Expected nested structure for "symptom"
    EXPECTED_SYMPTOM_STRUCTURE = {
        "symptoms": list,
        "duration": str
    }
    
    invalid_items = []
    line_numbers = []
    total_items = 0
    
    print("Starting validation of JSONL file...")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_items += 1
            
            # Skip empty lines
            if not line.strip():
                continue
                
            try:
                item = json.loads(line.strip())
                issues = []
                
                # Check 1: All required top-level keys exist
                expected_keys = set(EXPECTED_STRUCTURE.keys())
                actual_keys = set(item.keys())
                
                # Check for missing keys
                missing_keys = expected_keys - actual_keys
                if missing_keys:
                    issues.append(f"Missing keys: {sorted(missing_keys)}")
                
                # Check for extra keys
                extra_keys = actual_keys - expected_keys
                if extra_keys:
                    issues.append(f"Extra keys: {sorted(extra_keys)}")
                
                # Check 2: Value types for top-level keys
                for key, expected_type in EXPECTED_STRUCTURE.items():
                    if key in item:
                        actual_value = item[key]
                        
                        # Special handling for symptom dict
                        if key == "symptom":
                            if not isinstance(actual_value, dict):
                                issues.append(f"Key '{key}' should be dict, got {type(actual_value).__name__}")
                            else:
                                # Check nested symptom structure
                                symptom_keys = set(actual_value.keys())
                                expected_symptom_keys = set(EXPECTED_SYMPTOM_STRUCTURE.keys())
                                
                                missing_symptom_keys = expected_symptom_keys - symptom_keys
                                if missing_symptom_keys:
                                    issues.append(f"Symptom missing keys: {sorted(missing_symptom_keys)}")
                                
                                # Check symptom value types
                                for symptom_key, symptom_expected_type in EXPECTED_SYMPTOM_STRUCTURE.items():
                                    if symptom_key in actual_value:
                                        if not isinstance(actual_value[symptom_key], symptom_expected_type):
                                            issues.append(f"Symptom key '{symptom_key}' should be {symptom_expected_type.__name__}, "
                                                        f"got {type(actual_value[symptom_key]).__name__}")
                        
                        # Check other top-level keys
                        elif not isinstance(actual_value, expected_type):
                            issues.append(f"Key '{key}' should be {expected_type.__name__}, "
                                        f"got {type(actual_value).__name__}")
                
                # Check 3: Specific value constraints
                if "id" in item and not isinstance(item["id"], int):
                    issues.append("'id' must be an integer")
                
                if "age" in item and not isinstance(item["age"], int):
                    issues.append("'age' must be an integer")
                
                if "level" in item and item["level"] not in ["mild", "moderate", "severe"]:
                    issues.append(f"'level' should be 'mild', 'moderate', or 'severe', got '{item.get('level')}'")
                
                # Check list contents (optional, but helpful)
                list_keys = ["medical_history", "lifestyle_factor", "vaccination_history", "family_history"]
                for list_key in list_keys:
                    if list_key in item:
                        if not isinstance(item[list_key], list):
                            issues.append(f"'{list_key}' should be a list")
                        elif list_key == "symptom" and "symptoms" in item["symptom"]:
                            if not isinstance(item["symptom"]["symptoms"], list):
                                issues.append("'symptoms' inside 'symptom' should be a list")
                
                # If any issues found, record this item
                if issues:
                    invalid_items.append({
                        "line_number": line_num,
                        "item_id": item.get("id", "Unknown"),
                        "issues": issues,
                        "data": item  # Include the actual data for reference
                    })
                    line_numbers.append(line_num)
                    
            except json.JSONDecodeError as e:
                invalid_items.append({
                    "line_number": line_num,
                    "item_id": "Invalid JSON",
                    "issues": [f"JSON parsing error: {str(e)}"],
                    "data": line.strip()[:100] + "..." if len(line) > 100 else line.strip()
                })
                line_numbers.append(line_num)
    
    # Print summary report
    print("\n" + "=" * 60)
    print("VALIDATION REPORT")
    print("=" * 60)
    print(f"Total items processed: {total_items}")
    print(f"Valid items: {total_items - len(invalid_items)}")
    print(f"Invalid items: {len(invalid_items)}")
    
    if invalid_items:
        print(f"Line numbers with issues: {line_numbers}")
        print("\n" + "=" * 60)
        print("DETAILED ISSUES:")
        print("=" * 60)
        
        for invalid in invalid_items:
            print(f"\nItem at line {invalid['line_number']} (ID: {invalid['item_id']}):")
            for i, issue in enumerate(invalid['issues'], 1):
                print(f"  {i}. {issue}")
            
            # Show a snippet of the problematic data
            if "data" in invalid and invalid["data"]:
                data_str = json.dumps(invalid["data"], indent=2) if isinstance(invalid["data"], dict) else invalid["data"]
                print(f"\n  Data snippet: {data_str[:200]}..." if len(data_str) > 200 else f"\n  Data: {data_str}")
            
            print("-" * 40)
        
        return False, invalid_items
    else:
        print("\n✓ All items follow the expected format!")
        return True, []


def save_invalid_items_to_file(invalid_items, output_file="invalid_items.json"):
    """Save invalid items to a JSON file for further analysis"""
    if invalid_items:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(invalid_items, f, indent=2, ensure_ascii=False)
        print(f"\nInvalid items saved to: {output_file}")


if __name__ == "__main__":
    # Replace with your actual file path
    file_path = "./pulmonology_case_synthesized_yonghui.jsonl"  # Change this to your actual file path
    
    try:
        is_valid, invalid_items = validate_jsonl_format(file_path)
        
        # Optionally save invalid items to a file
        # if invalid_items:
            # save_invalid_items_to_file(invalid_items)
        
        # Exit with appropriate code for scripting
        exit(0 if is_valid else 1)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        print("Please make sure the file exists and the path is correct.")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        exit(1)