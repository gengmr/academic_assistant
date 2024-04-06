import streamlit as st


def initialize_session_state_variables():
    keys_with_default_values = {
        # 文本框key
        "title": "",
        "authors": "",
        "institutes": "",
        "introduction": "",
        "abstract": "",
        "keywords": "",
        # 文本框输入内容
        "title-area": "",
        "authors-area": "",
        "institutes-area": "",
        "introduction-area": "",
        "abstract-area": "",
        "keywords-area": "",
        # 英文论文经过格式化处理内容
        "introduction_processed": "",
        "abstract_processed": "",
        "sections_processed": [],
        # 翻译内容及翻译+格式化处理内容
        "zh_title-area": "",
        "zh_institutes-area": "",
        "zh_introduction_processed": "",
        "zh_abstract_processed": "",
        "zh_keywords-area": "",
        "zh_sections_processed": [],
        # 正文内容
        "sections": [],  # Assuming sections is a list; adjust if it's supposed to be a different type
        # api key
        "api_key-area": "",
        "api_flag": False
    }

    for key, default_value in keys_with_default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value