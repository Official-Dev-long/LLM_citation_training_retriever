from treatment_guideline_retriever import treatment_guideline_retriever
from ragflow_sdk import RAGFlow

import json

JSON_FILE = "./data/translated_data/test_pulmonology_case_synthesized_yonghui_translated.jsonl"
LIMIT = 2

def read_jsonl(file_path, limit=LIMIT):
    data = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            data.append(json.loads(line.strip()))

    return data

data = read_jsonl(JSON_FILE, limit=LIMIT)
medical_case = data[1]['message']

# Convert to JSON string with formatting
medical_case_string = json.dumps(medical_case, indent=2, ensure_ascii=False)

retriever = treatment_guideline_retriever()
retriever.sync_datasets()

from treatment_guideline_retriever import treatment_guideline_retriever
from ragflow_sdk import RAGFlow

import json

JSON_FILE = "./data/translated_data/test_pulmonology_case_synthesized_yonghui_translated.jsonl"
LIMIT = 2

def read_jsonl(file_path, limit=LIMIT):
    data = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            data.append(json.loads(line.strip()))

    return data

data = read_jsonl(JSON_FILE, limit=LIMIT)
medical_case = data[1]['message']

# Convert to JSON string with formatting
medical_case_string = json.dumps(medical_case, indent=2, ensure_ascii=False)

retriever = treatment_guideline_retriever()
retriever.sync_datasets()

retrieved_result = retriever.retrieve_guidelines(query=medical_case_string, department_names=["呼吸科"])
print(retrieved_result)

departments = ["f43bdae2bfba11f0a595924528ddf6e5"]