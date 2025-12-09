# Structure

## `data/raw_data`
1. `pulmonology_case_synthesized_yonghui.jsonl` contains 10K synthesized medical case
2. `pulmonology_case_real_junkai.jsonl` contains 83 real world medical case (data source: yiigle, human extracted)

## `data/translated_data`

translated results (chinese) from `pulmonology_case_synthesized_yonghui.jsonl`

1.`pulmonology_case_synthesized_yonghui_translated_0_4999.jsonl`

2.`pulmonology_case_synthesized_yonghui_translated_5000_9999.jsonl`

## `scripts/translate_synthesized_data`

1. `translate_synthesized.py` running well
2. `translate_synthesized_xxx_xxx.py` parallel running 

## `scripts/treatment_RAG`

wrapper sdk to use Tairex RAG module 

1. `treatment_guideline_retriever.py` header
2. `usage.py` example usage
3. `tag.txt` all categories of chunks