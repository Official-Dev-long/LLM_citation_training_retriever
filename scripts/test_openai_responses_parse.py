import os
from dotenv import load_dotenv

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from openai import OpenAI

# Load variables from .env into environment
load_dotenv()

class MedicalRecord(BaseModel):
    id: int
    name: str
    gender: str
    age: int 
    medical_history: List[str]
    lifestyle_factor: List[str]
    vaccination_history: List[str]
    family_history: List[str]
    disease: str
    level: str 
    symptom: Dict
    examination_results: List[str]

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

prompt = """Translate the following medical record into JSON format according to the given schema.
The medical record is originally in english, json-formatted, and containing such information:
Schema:
{
    id: int
    name: str
    gender: str
    age: int 
    medical_history: List[str]
    lifestyle_factor: List[str]
    vaccination_history: List[str]
    family_history: List[str]
    disease: str
    level: str 
    symptom: Dir
    examination_results: List[str],
},

Your return should strictly follow the schema and be in valid JSON format. Only translate the content of each values (of the keys), do not change the keys (remains in English as I given to you). Here is the medical record in english:
"""

json_medical_record = """{"id": 0, "name": "Carlos Mendoza", "gender": "Male", "age": 52, "medical_history": ["History of heart failure", "Previous pneumonia"], "lifestyle_factor": ["Non-smoker", "Works in construction with occasional exposure to asbestos", "Moderate alcohol use"], "vaccination_history": ["Incomplete BCG vaccination history"], "family_history": ["Mother had tuberculosis", "Father had heart disease"], "disease": "Pleural Effusion", "level": "mild", "symptom": {"symptoms": ["dyspnea", "breathing difficulty", "low fever", "cough", "night sweats"], "duration": "Symptoms have been present for the past 2 weeks, with gradual worsening."}, "examination_results": {"physical_examination": "The examination reveals a diminished breath sound on the left side with dullness to percussion. There is a slight decrease in tactile fremitus, suggesting fluid accumulation.", "imaging_tests": "Chest X-ray shows a mild blunting of the left costophrenic angle with a small crescent-shaped opacity. No significant lung compression is visible.", "laboratory_tests": "Pleural fluid analysis shows clear yellow fluid with a normal protein level and low white blood cell count. There are no signs of infection or malignancy in the fluid.", "pleural_biopsy": "Biopsy results are pending, but preliminary findings do not suggest malignancy or tuberculosis. Further investigation may be needed based on clinical progression.", "thoracoscopy": "Not performed at this stage due to the mild severity of symptoms. It may be considered if symptoms worsen or diagnosis remains unclear."}}"""

#responses.parse to limit LLM response in JSON format
response = client.responses.parse(
    model="gpt-4o-mini",
    input=[
        {"role": "system", "content": "You are a good translator in medical field."},
        {"role": "user", "content": prompt + json_medical_record},
    ],
    text_format=MedicalRecord
)

medical_record_translated = response.output_parsed
print(medical_record_translated)