from ragflow_sdk import RAGFlow

import os
from dotenv import load_dotenv

load_dotenv()

import json
from typing import Any, List, Dict, Optional

import requests

class treatment_guideline_retriever:
    """A module for interacting with RAGFlow API for medical department data retrieval."""
    
    def __init__(self):
        """
        Initialize the RAGFlow module.
        
        Args:
            api_key: RAGFlow API key
            base_url: RAGFlow base URL
            json_path: Path to the datasets JSON file
        """
        self.rag_object = RAGFlow(api_key=os.getenv("RAGFLOW_API_KEY"),                     
                                  base_url=os.getenv("RAGFLOW_BASE_URL")
                                  )
        self.json_path = "./datasets_full.json" 
        self.department_mapping = self._load_department_mapping()
    
    def _dataset_to_dict(self, dataset: Any) -> dict:
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
            result[attr] = val

        # Remove avatar if present (can be a very large base64 string)
        if "avatar" in result:
            try:
                del result["avatar"]
            except Exception:
                result.pop("avatar", None)

        return result

    def sync_datasets(self) -> None:
        """
        Fetch list of dataset objects from the RAGflow server side 
        and write each dataset as a JSON object in an array.
        This should be called periodically to update the department mapping.
        """
        full_list = []
        for dataset in self.rag_object.list_datasets():
            full_list.append(self._dataset_to_dict(dataset))

        with open(self.json_path, "w", encoding="utf-8") as jf:
            json.dump(full_list, jf, default=str, ensure_ascii=False, indent=2)
        
        # Reload the mapping after saving
        self.department_mapping = self._load_department_mapping()

    def _load_department_mapping(self) -> Dict[str, str]:
        """
        Load department name to ID mapping from JSON file.
        
        Returns:
            Dictionary mapping department names to their IDs
        """
        try:
            with open(self.json_path, "r", encoding="utf-8") as jf:
                datasets = json.load(jf)
            
            mapping = {}
            for dataset in datasets:
                name = dataset.get("name", "")
                dataset_id = dataset.get("id", "")
                if name and dataset_id:
                    mapping[name] = dataset_id
            
            return mapping

        except FileNotFoundError:
            print(f"Warning: JSON file {self.json_path} not found. Please call sync_datasets() first.")
            return {}
        except Exception as e:
            print(f"Error loading department mapping: {e}")
            return {}

    def get_department_ids(self, department_names: List[str]) -> List[str]:
        """
        Get department IDs for given department names.
        
        Args:
            department_names: List of department names (e.g., ["呼吸科", "眼科", "神经科"])
            
        Returns:
            List of department IDs
        """
        department_ids = []
        missing_departments = []
        
        for dept_name in department_names:
            dept_id = self.department_mapping.get(dept_name)
            if dept_id:
                department_ids.append(dept_id)
            else:
                missing_departments.append(dept_name)
        
        if missing_departments:
            print(f"Warning: The following departments were not found: {missing_departments}")
            print(f"Available departments: {list(self.department_mapping.keys())}")
        
        return department_ids

    def get_department_name(self, department_id: str) -> Optional[str]:
        """
        Get department name for a given department ID.
        
        Args:
            department_id: Department ID
        
        Returns:
            Department name or None if not found
        """
        for name, dept_id in self.department_mapping.items():
            if dept_id == department_id:
                return name
        return None

    def retrieve_guidelines(self, query: str, department_names: List[str], k: int = 100) -> List[Dict]:
        """
        Retrieve information based on a medical record.
        
        Args:
            department_names: List of department names to search in
            query: Medical record content as query
            
        Returns:
            List of dictionaries containing chunk information
        """
        department_ids = self.get_department_ids(department_names)
        
        if not department_ids:
            print("Error: No valid department IDs found.")
            return []
        
        retrieve_chunks = self.rag_object.retrieve(question=query, dataset_ids=department_ids, page_size=k)

        results = []
        for idx, chunk in enumerate(retrieve_chunks):

            _dataset_name = self.get_department_name(chunk.dataset_id)

            _dataset = self.rag_object.list_datasets(id=chunk.dataset_id)
            _document = _dataset[0].list_documents(id=chunk.document_id)
            _document_name = _document[0].name if _document else " "

            chunk_info = {
                "content": chunk.content,
                "department_id": chunk.dataset_id,
                "department_name": _dataset_name,
                "document_id": chunk.document_id,
                "document_name": _document_name,
                "similarity_score": chunk.similarity
            }
            results.append(chunk_info)
        
        return results

    def retrieve_treament(self, disease_name: str, department_names: List[str]  , query_type: str = "治疗", k: int = 32) -> List[Dict]:
        """
        Retrieve information about a disease from specified departments.
        
        Args:
            disease_name: Name of the disease (e.g., "哮喘")
            department_names: List of department names to search in
            query_type: Type of information to retrieve (e.g., "治疗", "症状", "诊断")
            
        Returns:
            List of dictionaries containing chunk information
        """
        department_ids = self.get_department_ids(department_names)
        
        if not department_ids:
            print("Error: No valid department IDs found.")
            return []
        
        query = f"{disease_name}{query_type}"

        retrieve_chunks = self.rag_object.retrieve(question=query, dataset_ids=department_ids, page_size=k)

        results = []
        for idx, chunk in enumerate(retrieve_chunks):

            _dataset_name = self.get_department_name(chunk.dataset_id)

            _dataset = self.rag_object.list_datasets(id=chunk.dataset_id)
            _document = _dataset[0].list_documents(id=chunk.document_id)
            _document_name = _document[0].name if _document else " "

            chunk_info = {
                "content": chunk.content,
                "department_id": chunk.dataset_id,
                "department_name": _dataset_name,
                "document_id": chunk.document_id,
                "document_name": _document_name,
                "similarity_score": chunk.similarity
            }
            results.append(chunk_info)
        
        return results

    def retrieve_treament_with_metadata_filteration(self, disease_name: str, department_names: List[str], tag_feas: List[str], exclude_tags: List[str], k: int = 32) -> List[Dict]:
        """
        Retrieve information about a disease from specified departments with metadata filtering.
        
        Args:
            disease_name: Name of the disease (e.g., "哮喘")
            department_names: List of department names to search in
            tag_feas: List of tags to include
            exclude_tags: List of tags to exclude
            k: Number of top results to retrieve
        Returns:
            List of dictionaries containing chunk information
        """

        department_ids = self.get_department_ids(department_names)

        base_url = os.getenv("RAGFLOW_BASE_URL")
        url = f"{base_url}/api/v1/retrieval"
        api_key = os.getenv("RAGFLOW_API_KEY")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }

        data = {
            "question": disease_name,
            "dataset_ids": department_ids,
            "tag_feas": tag_feas,
            "exclude_tags": exclude_tags,
            "page_size": k,
        }

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                retrieved_result = response.json()

            else:
                print(f"Error: Received status code {response.status_code}")
                retrieved_result = {}

        except Exception as e:
            print(f"Exception occurred: {e}")
            retrieved_result = {}

        result = []
        for idx, chunk in enumerate(retrieved_result.get('data', {}).get('chunks', [])):

            _dataset_name = self.get_department_name(chunk["dataset_id"])

            chunk_info = {
                "content": chunk["content"],
                "department_id": chunk["dataset_id"],
                "department_name": _dataset_name,
                "document_id": chunk["document_id"],
                "document_name": chunk["document_keyword"],
                "similarity_score": chunk["similarity"],
            }
            result.append(chunk_info)

        return result

    def get_available_departments(self) -> List[str]:
        """
        Get list of available department names.
        
        Returns:
            List of available department names
        """
        return list(self.department_mapping.keys())