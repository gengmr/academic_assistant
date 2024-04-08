import streamlit as st
import json


def initialize_session_state_variables():
    # 读取ChatGPT图标可选列表
    with open('config/ChatGPT_icons.json', "r", encoding='utf8') as file:
        chatgpt_icon_options = json.load(file)
    # 读取字体可选列表
    with open('config/fonts.json', "r", encoding='utf8') as file:
        font_options = json.load(file)

    keys_with_default_values = {
        # ChatGPT图标可选列表
        "chatgpt_icon_options": chatgpt_icon_options,
        # 显示界面字体设置
        "font_options": font_options,
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
        "api_flag": False,
        # ChatGPT API对整篇论文分析结果汇总
        "summary_result": {},
        # ChatGPT API对整篇论文概述
        "summary": "",
        # ChatGPT API生成的论文分章节总结
        "section_summaries": [],
        # ChatGPT API对论文整体评估
        "overall_assessment": []
    }

    for key, default_value in keys_with_default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value