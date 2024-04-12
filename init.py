import streamlit as st
import json
from component_style import component_style


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
        # 显示界面字体可选列表
        "font_options": font_options,
        # 文本框key
        "publish_time": "",  # 论文发表日期
        "title": "",
        "authors": "",
        "institutes": "",
        "publication": "",
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
        "overall_assessment": [],
        # 润色结果
        "polished_title-area": "",
        "polished_introduction_processed": "",
        "polished_abstract_processed": "",
        "polished_sections_processed": [],
    }

    for key, default_value in keys_with_default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def init():
    """
    变量初始化、组件样式、页面样式、侧边栏样式等
    """
    # 初始化变量
    initialize_session_state_variables()
    # 设置为宽屏模式
    st.set_page_config(layout="wide")
    # 定义通用CSS样式来减少上方空白
    custom_css = """
        <style>
            /* 隐藏Streamlit的顶部导航栏 */
            .stApp { margin-top: -100px; }
        </style>
    """
    # 将自定义CSS添加到页面
    st.markdown(custom_css, unsafe_allow_html=True)
    # 设置组件样式为自定义样式，符合苹果风格
    component_style()
    # 设置侧边栏样式
    st.markdown('<style>' + open('sidebar.css').read() + '</style>', unsafe_allow_html=True)