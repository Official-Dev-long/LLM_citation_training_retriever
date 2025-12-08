import json
from tqdm import tqdm
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

LIMIT = None
BATCH_SIZE = 5  

INPUT_FILE = "../../data/raw_data/pulmonology_case_synthesized_yonghui.jsonl"
OUTPUT_FILE = "../../data/translated_data/pulmonology_case_synthesized_yonghui_translated_batch.jsonl"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

# --- Helper functions ---

def read_jsonl(file_path, limit=None):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            data.append(json.loads(line.strip()))
    return data

def batch_translate_json_objects(batch):
    batch_str = json.dumps(batch, ensure_ascii=False)
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
                {batch_str}

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

    try:
        translated_list = json.loads(llm_message)
    except json.JSONDecodeError:
        print("JSON decode error for batch, returning empty objects")
        translated_list = [{} for _ in batch]

    results = []
    for translated in translated_list:
        translated_flag = translated != {}
        results.append({
            "translated_flag": translated_flag,
            "translated": translated,
            "message": llm_message,
        })
    return results

# --- Main processing ---

data = read_jsonl(INPUT_FILE, limit=LIMIT)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for i in tqdm(range(0, len(data), BATCH_SIZE)):
        batch = data[i:i+BATCH_SIZE]
        results = batch_translate_json_objects(batch)
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
