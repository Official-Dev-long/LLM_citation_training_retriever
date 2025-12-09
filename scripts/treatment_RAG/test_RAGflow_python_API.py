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

    retrieve_chunks = rag_object.retrieve(question=query, dataset_ids=departments, page_size=100)

    query = """
                {
            "id": 1,
            "名字": "约翰·史密斯",
            "性别": "男性",
            "年龄": 60,
            "病史": [
                "慢性阻塞性肺病 (COPD)",
                "10年前曾被诊断为肺癌",
                "吸烟40年"
            ],
            "生活方式因素": [
                "主动吸烟者",
                "工作中接触石棉",
                "身体活动有限",
                "饮食不良"
            ],
            "疫苗接种史": [
                "常规疫苗接种未更新",
                "没有与肺癌预防相关的疫苗接种"
            ],
            "家族史": [
                "父亲死于肺癌",
                "母亲患有乳腺癌"
            ],
            "疾病": "肺癌",
            "级别": "严重",
            "症状": {
                "症状": [
                "咳嗽",
                "阵发性刺激性干咳，伴有少量或无痰",
                "不规则的钝痛胸痛",
                "咳嗽加重时疼痛",
                "咯血",
                "咳血",
                "呼吸困难",
                "声音嘶哑",
                "高音调金属咳嗽",
                "窒息性咳嗽",
                "气短",
                "喘息",
                "发热",
                "阻塞性肺炎",
                "肺不张",
                "胸腔积液",
                "上腔静脉综合症",
                "颈部和面部水肿",
                "头痛",
                "嗜睡",
                "视力模糊",
                "霍纳综合症",
                "眼睑下垂",
                "瞳孔缩小",
                "眼球内陷",
                "无汗症",
                "感觉障碍",
                "吞咽困难",
                "心包积液",
                "中枢神经系统症状",
                "恶心",
                "呕吐",
                "癫痫发作",
                "偏瘫",
                "失语",
                "站立不稳",
                "共济失调步态",
                "骨骼症状",
                "骨痛",
                "病理性骨折",
                "黄疸",
                "腹痛",
                "血尿",
                "淋巴结肿大",
                "肥厚性骨关节病",
                "杵状指",
                "骨赘",
                "肢端疼痛",
                "虚弱",
                "心动过速",
                "潮红",
                "心血管症状",
                "局部肢体红肿",
                "血栓性静脉炎"
                ],
                "持续时间": "症状在过去6个月逐渐加重，最近3周显著恶化。"
            },
            "检查结果": {
                "影像学检查": "胸部X光显示右上叶有一个大而不规则的肿块，伴有胸腔积液和可能的淋巴结受累证据。CT扫描确认存在大肿瘤，伴有淋巴结转移和上腔静脉综合症的迹象。",
                "内窥镜检查": "支气管镜检查显示中心位置的肿块导致显著的气道阻塞，并确认活检组织中存在恶性细胞。纵隔镜检查显示淋巴结肿大，与转移一致。",
                "病理检查": "组织学检查确认为非小细胞肺癌，肿瘤分级为高等级。免疫组化染色显示特定癌症标志物的阳性结果。",
                "基因检测": "基因检测识别出EGFR基因的突变，表明适合使用EGFR抑制剂的靶向治疗。",
                "实验室检查": "肿瘤标志物水平升高，包括CEA和CYFRA21-1。常规血液检查显示贫血和肝功能障碍，提示系统性受累。"
            }
    """

    retrieve_chunks = rag_object.retrieve(question=query, dataset_ids=departments, page_size=100)

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

        