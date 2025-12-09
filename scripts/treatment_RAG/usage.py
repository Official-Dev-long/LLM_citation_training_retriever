from treatment_guideline_retriever import treatment_guideline_retriever

retriever = treatment_guideline_retriever()

# -----------------------------------------------------------------------------
# minimal usage 
# -----------------------------------------------------------------------------


# provide diagnose name and corresponding departments
disease = "哮喘"
departments = ["呼吸科"]

returned_treatment_guidelines = retriever.retrieve_treament(disease_name=disease, department_names=departments)

# return type: list of dicts
# chunk_info = {
#                "content": chunk.content,
#                "department_id": chunk.dataset_id,
#                "department_name": _dataset_name,
#                "document_id": chunk.document_id,
#                "document_name": _document_name,
#                "similarity_score": chunk.similarity
#            }

# print(returned_treatment_guidelines)

# example return
# [{'content': '（4）按哮喘治疗有效', 'department_id': 'bb1007b0b53e11f0a33b626fb91f35f8', 'department_name': '呼吸科', 'document_id': 'b56cc210b55411f090152623b059f19c', 'document_name': '轻度支气管哮喘诊断与治疗中国专家共识（2023）.pdf', 'similarity_score': 0.9651536210894073}, {'content': '10. 其他治疗哮喘药物：第二代抗组胺药物（ \\(\\mathrm{H}_{1}\\) 受体拮抗剂）如氯雷他定、阿司咪唑、 氯卓司丁、特非那丁，其他口服抗变态反应药物如曲尼司特（tranilast）、瑞吡司特（repirinast）等，抗组胺药物在哮喘治疗中作用较弱，主要用于伴有变应性鼻炎的哮喘患者，不建议长期使用抗组胺药物。\n（四）制订治疗方案\n一旦确立了哮喘的诊断，尽早开始规律的控制治疗对于取得最佳的疗效至关重要。对于成人哮喘患者的初始治疗，应根据患者具体情况选择合适的级别，或在两相邻级别之间的建议选择高的级别，以保证初始 治疗的成功率（表7）。\nGINA目前推荐所有成年和青少年哮喘患者接受包含ICS的控制治疗，以降低重度急性发作的风险，ICS可以作为每日常规用药，在轻度哮喘患者中可采用 \\(\\mathrm{ICS + }\\) 福莫特罗按需给药。\n整个哮喘治疗过程中需要连续对患者进行评估、调整并观察治疗反应。控制性药物的升降级应按照阶梯式方案选择。哮喘控制维持至少3个月以上可以考虑降级治疗，以找到维持哮喘控制的最低有效治疗级别。', 'department_id': 'bb1007b0b53e11f0a33b626fb91f35f8', 'department_name': '呼吸科', 'document_id': 'b884a328b55411f090152623b059f19c', 'document_name': '支气管哮喘防治指南（2020年版）.pdf', 'similarity_score': 0.959687822827477}, {'content': '[哮喘的治疗]', 'department_id': 'bb1007b0b53e11f0a33b626fb91f35f8', 'department_name': '呼吸科', 'document_id': 'b8aec45ab55411f090152623b059f19c', 'document_name': '支气管哮喘防治指南（支气管哮喘的定义、诊断、治疗、疗效判断标准及教育和管理方案）.pdf', 'similarity_score': 0.7779891900015486}, {'content': '（3）抗哮喘治疗有效。', 'department_id': 'bb1007b0b53e11f0a33b626fb91f35f8', 'department_name': '呼吸科', 'document_id': 'b56cc210b55411f090152623b059f19c', 'document_name': '轻度支气管哮喘诊断与治疗中国专家共识（2023）.pdf', 'similarity_score': 0.7756873008293682}, ......]

# -----------------------------------------------------------------------------
# sync datasets from RAGflow (updating datasets name and id mapping)
# -----------------------------------------------------------------------------

retriever.sync_datasets()

# -----------------------------------------------------------------------------
# show available departments (datasets in RAGflow)
# -----------------------------------------------------------------------------

available_departments = retriever.get_available_departments()

print(available_departments)

# example - updated 05/12/2025

# ['神经内科[UptoDate]', '眼科[UpToDate]', '呼吸科[UptoDate]', '心血管科', '普通外科[text-embedding-v4]', '耳鼻喉科[text-emedding-v4]', '全科[text-embedding-v4]', '眼科[text-embedding-v4]', '呼吸科[text-embedding-v4]', '耳鼻喉科', '普通外科', '神经科', '消化科', '眼科', '呼吸科', '标签集']

# -----------------------------------------------------------------------------
# setting up top k 
# -----------------------------------------------------------------------------

# default maximum top_k in RAGflow 1024
# default top_k in retriever.retrieve_treament is 32

disease = "哮喘"
departments = ["呼吸科"]

returned_treatment_guidelines = retriever.retrieve_treament(disease_name=disease, department_names=departments, k=2)

# print(returned_treatment_guidelines)

# -----------------------------------------------------------------------------
# metadata filteration (call retriever.retrieve_treament_with_metadata_filteration)
# -----------------------------------------------------------------------------

tag_feas = ["治疗-方式-药物治疗","治疗-方式-手术治疗","治疗-方式-物理治疗","治疗-方式-放射治疗","治疗-方式-化学治疗","治疗-方式-免疫治疗","治疗-方式-基因治疗","治疗-方式-介入治疗","治疗-方式-中医治疗","治疗-方式-营养治疗","治疗-方式-心理治疗","治疗-方式-康复治疗","治疗-方式-姑息/支持治疗","治疗-方式-预防性治疗","治疗-阶段-急性期治疗","治疗-阶段-恢复期治疗","治疗-阶段-长期维持治疗","治疗-阶段-预防性治疗"]
exclude_tags = []

returned_treatment_guidelines_with_metadata_filteration = retriever.retrieve_treament_with_metadata_filteration(
    disease_name=disease,
    department_names=departments,
    tag_feas=tag_feas,
    exclude_tags=exclude_tags,
    k=2
)

# print(returned_treatment_guidelines_with_metadata_filteration)