from ragflow_sdk import RAGFlow

import json
import requests
from typing import Any, List, Dict, Optional 

DEPARTMENT_REQUIRED_list = ["呼吸科"]

rag_object = RAGFlow(api_key="ragflow-I1MTljMDQ0YzA2ZTExZjBiMzA1OTI0NT", base_url="http://39.97.162.192/")

def _dataset_to_dict(dataset: Any) -> dict:
    """Convert a ragflow dataset object to a plain dict for JSON serialization."""

    result = {}
    for attr in dir(dataset):
        if attr.startswith("_"):
            continue
        try:
            val = getattr(dataset, attr)
        except Exception:
            continue
        if callable(val):
            continue
        # avoid heavy descriptors like modules
        result[attr] = val

    # Remove avatar if present (can be a very large base64 string)
    if "avatar" in result:
        try:
            del result["avatar"]
        except Exception:
            # ensure we don't fail serialization for unexpected reasons
            result.pop("avatar", None)

    return result


def fetch_and_save_datasets(json_path: str = "datasets_full.json") -> None:
    """Fetch list of dataset objects and write each dataset as a JSON object in an array.

    The file will contain a JSON array where each element is the dataset serialized to a dict.
    Non-JSON-serializable values are converted to strings by json.dump's default=str fallback.
    """
    full_list = []
    for dataset in rag_object.list_datasets():
        full_list.append(_dataset_to_dict(dataset))

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(full_list, jf, default=str, ensure_ascii=False, indent=2)

def retrieve_metadata_filteration(disease_name: str, department_id: List[str], k: int=32) -> List[Dict]:

    url = "http://39.97.162.192/api/v1/retrieval"
    api_key = "ragflow-I1MTljMDQ0YzA2ZTExZjBiMzA1OTI0NT"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        "question": disease_name,
        "dataset_ids": department_id,
        "tag_feas": ["诊断-手段-功能检查"],
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()

        else:
            print(f"Error: Received status code {response.status_code}")
            result = {}

    except Exception as e:
        print(f"Exception occurred: {e}")
        result = {}

    return result



if __name__ == "__main__":
    # Only write the full dataset objects (avatar removed). 
    # fetch_and_save_datasets()

    #呼吸科 神经科 眼科
    departments = ["f43bdae2bfba11f0a595924528ddf6e5"]

    disease_name = "哮喘"
    query = disease_name + "治疗"

    retrieve_chunks = rag_object.retrieve(question=query, dataset_ids=departments, page_size=2)

    for idx, chunk in enumerate(retrieve_chunks):
        # print(chunk)

        print(f"==== Chunk {idx} ====")
        print(f"Content: {chunk.content}")
        print(f"Source Document ID: {chunk.document_id}")
        print(f"Source Document name: {chunk.document_name}")
        print(f"Source Dataset ID: {chunk.dataset_id}")
        print(f"Score: {chunk.similarity}")

    retrieve_chunks_with_metadata_filteration = retrieve_metadata_filteration(disease_name=disease_name, department_id=departments)

    print("==== Metadata Filteration Results ====")
    print(retrieve_chunks_with_metadata_filteration)

        