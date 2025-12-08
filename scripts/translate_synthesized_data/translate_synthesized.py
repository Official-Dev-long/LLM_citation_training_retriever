import json
from tqdm import tqdm
from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

LIMIT = None
INPUT_FILE = "../../data/raw_data/pulmonology_case_synthesized_yonghui.jsonl"
OUTPUT_FILE = "../../data/translated_data/pulmonology_case_synthesized_yonghui_translated.jsonl"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

def read_jsonl(file_path, limit=None):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            data.append(json.loads(line.strip()))
    return data

def translate_json_object(obj):
    obj_str = json.dumps(obj, ensure_ascii=False)
    prompt = f"""
                You are a professional medical translator. 
                Translate the following JSON object from English to Chinese. 
                Keep the JSON structure exactly the same.
                Translating each key into Chinese too.
                e.g. "name" -> "名字", "age" -> "年龄", etc.

                Only return a valid JSON object without any extra explanation.

                Your output will be passed to a python json.loads() function, 
                so ensure it is adaptable for that.
                Your return should not start with ```json and not containing 
                excape nextline excharacters.

                JSON:
                {obj_str}

                """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who translates JSON data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    
    llm_message = response.choices[0].message.content.strip()
    
    # Try parsing the returned JSON
    try:
        translated_obj = json.loads(llm_message)
    except json.JSONDecodeError:
        translated_obj = {}
    
    if translated_obj == {}:
        translated_flag = False
    else:
        translated_flag = True

    # Include the raw LLM message and scheme_followed
    result = {
        "translated_flag": translated_flag,
        "translated": translated_obj,
        "message": llm_message,
    }
    return result

# --- Main processing ---

input_file = INPUT_FILE
output_file = OUTPUT_FILE

data = read_jsonl(input_file, limit=LIMIT)

with open(output_file, 'w', encoding='utf-8') as f:
    for obj in tqdm(data):
        result = translate_json_object(obj)
        f.write(json.dumps(result, ensure_ascii=False) + "\n")