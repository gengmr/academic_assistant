import json
import streamlit as st
import copy
from openai import OpenAI
from utils import escape_backslashes_except_newlines, add_section_numbers, get_section_summary
from config.config import (chatgpt_model, paragraph_process_system_prompt,paragraph_process_with_translate_system_prompt,
                           summarize_system_prompt, translate_system_prompt, english_polish_system_prompt,
                           chinese_polish_system_prompt, max_attempts)


def call_openai_api(system_prompt, request_prompt):
    """
    调用OpenAI API，并处理响应。
    :param system_prompt: 系统提示词
    :param request_text: 请求提示词
    """
    api_key = st.session_state["api_key-area"]
    base_url = "https://api.aiguoguo199.com/v1" if not st.session_state["openai_service"] else None
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=chatgpt_model,
        temperature=0,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': request_prompt}
        ]
    )
    response = response.choices[0].message.content
    return response


def test_api():
    """
    测试api调用是否正常
    """
    # 初始化设置为False
    st.session_state['api_flag'] = False
    try:
        system_prompt = "say hello to me"
        request_prompt = "hello"
        _ = call_openai_api(system_prompt=system_prompt, request_prompt=request_prompt)
        st.session_state['api_flag'] = True
    except Exception as e:
        print(e)


def polish_api(text, max_attempts):
    """
    使用OpenAI的API润色论文文本。

    :param text: str, 需要润色的文本。
    :param max_attempts: int, 最大重试次数，以应对API调用可能的失败。
    :return: str, 润色后的文本或在重试次数用尽后的失败信息。
    """
    if not text.strip():
        return text

    # 替换文本中的双引号为单引号，避免在JSON解析时发生错误
    text = text.replace('"', "'")

    # 根据润色的语言选择不同的提示信息
    system_prompt = english_polish_system_prompt if st.session_state[
        "polish_language_is_english"] else chinese_polish_system_prompt

    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}: Polishing text")
        try:
            response = call_openai_api(system_prompt=system_prompt, request_prompt=text)
            response = escape_backslashes_except_newlines(response)
            result = json.loads(response)
            return result.get("polished_text", f"<润色失败>{text}")
        except json.JSONDecodeError:
            print(f"Attempt {attempt} failed with JSON decode error")
        except Exception:
            print(f"Attempt {attempt} failed with error")

    print(f"Failed after {max_attempts} attempts, returning original text with failure notice.")
    return f"<润色失败>{text}"


def paragraph_translate_and_format_processing_api(text, translate_flag, max_attempts):
    """
    调用chatgpt api调整论文段落格式、公式显示及去除引用，并根据translate_flag决定是否翻译为中文
    :param text: 需要处理的论文片段
    :param translate_flag: 是否需要翻译为中文
    :param max_attempts: int, 最大重试次数，以应对API调用可能的失败。
    """
    # 将text中所有"替换为'避免json解析出现问题
    if not text.strip():
        return (text, text) if translate_flag else text

    # 替换文本中的双引号为单引号，避免在JSON解析时发生错误
    text = text.replace('"', "'")

    system_prompt = paragraph_process_with_translate_system_prompt if translate_flag else paragraph_process_system_prompt
    for attempt in range(1, 1 + max_attempts):  # 最多尝试两次
        print(f"Attempt {attempt}: Processing text")
        try:
            response = call_openai_api(system_prompt=system_prompt, request_prompt=text)
            result = escape_backslashes_except_newlines(text=response)

            result_dict = json.loads(result)
            if translate_flag:
                return result_dict.get('en_context'), result_dict.get('zh_context')
            else:
                return result_dict.get('context')
        except json.JSONDecodeError:
            print(f"Attempt {attempt} failed with JSON decode error")
        except Exception as e:
            print(f"Attempt {attempt} failed with error")

    print(f"超过最大测试次数：{max_attempts}，调用失败")
    # 所有尝试失败后的回退，按照输入文本返回
    return (text, text) if translate_flag else text


def summarize_api(text, max_attempts):
    """
    ChatGPT API分析整篇文章
    :param 待总结文章数据
    :param max_attempts: int, 最大重试次数，以应对API调用可能的失败。
    """
    system_prompt = summarize_system_prompt
    for attempt in range(1, 1 + max_attempts):
        print(f"Attempt {attempt}: Summarizing article")
        try:
            response = call_openai_api(system_prompt=system_prompt, request_prompt=text)
            result = escape_backslashes_except_newlines(response)
            return json.loads(result)
        except json.JSONDecodeError:
            print(f"Attempt {attempt} failed with JSON decode error")
        except Exception:
            print(f"Attempt {attempt} failed with error")

    print(f"超过最大测试次数：{max_attempts}，调用失败")
    return {"flag": "调用失败"}


def translate_api(text, max_attempts):
    """
    调用chatgpt api翻译文本
    :param text: 文本
    :param max_attempts: int, 最大重试次数，以应对API调用可能的失败。
    """
    if not text.strip():
        return text

    system_prompt = translate_system_prompt
    for attempt in range(1, 1 + max_attempts):  # 最多尝试两次
        print(f"Attempt {attempt}: Translating text")
        try:
            response = call_openai_api(system_prompt=system_prompt, request_prompt=text)
            result = json.loads(response)
            return result.get('zh_text', text)  # 如果没有'zh_text'键，则返回原文本
        except json.JSONDecodeError:
            print(f"Attempt {attempt} failed with JSON decode error")
        except Exception:
            print(f"Attempt {attempt} failed with error")

    print(f"超过最大测试次数：{max_attempts}，调用失败")
    return text  # 所有尝试失败后，返回原文本


def format_processing(max_attempts):
    """
    处理论文格式(段落格式、公式)，并根据translate_flag确定是否需要翻译为中文
    :param max_attempts: int, 最大重试次数，以应对API调用可能的失败。
    """
    # 1. 翻译论文标题、论文机构、论文关键词
    print("step 1.1: 翻译论文标题、论文机构、论文关键词...")
    if st.session_state["translate_flag"]:
        st.session_state['zh_title-area'] = translate_api(text=st.session_state['title-area'], max_attempts=max_attempts)
        st.session_state['zh_institutes-area'] = translate_api(text=st.session_state['institutes-area'], max_attempts=max_attempts)
        st.session_state['zh_keywords-area'] = translate_api(text=st.session_state['keywords-area'], max_attempts=max_attempts)
    # 2. 处理论文通用章节: abstract, introduction
    print("step 1.2: 处理论文通用章节...")
    if st.session_state["translate_flag"]:
        st.session_state['abstract_processed'], st.session_state['zh_abstract_processed'] = paragraph_translate_and_format_processing_api(text=st.session_state["abstract-area"], translate_flag=st.session_state["translate_flag"], max_attempts=max_attempts)
        st.session_state['introduction_processed'], st.session_state['zh_introduction_processed'] = paragraph_translate_and_format_processing_api(text=st.session_state["introduction-area"], translate_flag=st.session_state["translate_flag"], max_attempts=max_attempts)
    else:
        st.session_state['abstract_processed'] = paragraph_translate_and_format_processing_api(text=st.session_state["abstract-area"], translate_flag=st.session_state["translate_flag"], max_attempts=max_attempts)
        st.session_state['introduction_processed'] = paragraph_translate_and_format_processing_api(text=st.session_state["introduction-area"], translate_flag=st.session_state["translate_flag"], max_attempts=max_attempts)

    def sections_process(en_section, zh_section, level=0, translate_flag=False):
        if translate_flag:
            # 翻译章节标题为中文
            zh_section['title'] = translate_api(text=en_section['title'], max_attempts=max_attempts)
            # 调整论文段落格式、公式显示及去除引用，并翻译为中文
            en_section['texts'], zh_section['texts'] = paragraph_translate_and_format_processing_api(text=en_section['texts'], translate_flag=st.session_state["translate_flag"], max_attempts=max_attempts)
            # 如果当前章节有子章节，则递归遍历子章节
            for en_subsection, zh_subsection in zip(en_section['sections'], zh_section['sections']):
                sections_process(en_subsection, zh_subsection, level + 1, translate_flag=translate_flag)
        else:
            # 调整论文段落格式、公式显示及去除引用
            en_section['texts'] = paragraph_translate_and_format_processing_api(text=en_section['texts'], translate_flag=st.session_state["translate_flag"], max_attempts=max_attempts)
            # 如果当前章节有子章节，则递归遍历子章节
            for subsection in en_section['sections']:
                sections_process(subsection, None, level + 1, translate_flag=translate_flag)

    # 3. 处理论文正文'
    # 创建sections的深拷贝，避免指向同一数据
    if st.session_state["translate_flag"]:
        st.session_state['sections_processed'] = copy.deepcopy(st.session_state['sections'])
        st.session_state['zh_sections_processed'] = copy.deepcopy(st.session_state['sections'])
        # 遍历并处理 en_sections 和 zh_sections 的每个章节
        for en_section, zh_section in zip(st.session_state['sections_processed'], st.session_state['zh_sections_processed']):
            sections_process(en_section, zh_section, translate_flag=st.session_state["translate_flag"])
    else:
        st.session_state['sections_processed'] = copy.deepcopy(st.session_state['sections'])
        # 遍历并处理 en_sections 和 zh_sections 的每个章节
        for section in st.session_state['sections_processed']:
            sections_process(section, None, translate_flag=st.session_state["translate_flag"])


def paper_analysis(max_attempts):
    """
    总结论文，汇总论文的标题、摘要、导言、正文各部分内容，并评估论文的创新性等内容
    :param max_attempts: int, 最大重试次数，以应对API调用可能的失败。
    """
    # 重新整理论文格式，去掉无用信息
    body = copy.deepcopy(st.session_state['sections_processed'])  # 论文正文，深度复制防止修改sections_processed
    body = add_section_numbers(body=body)  # 增加章节号，去掉无效的id和flag字段
    # 将摘要和引言部分合并
    paper_body = [
        {
            "title": "abstract",
            "texts": st.session_state["abstract-area"],
            "sections": [],
            "section_number": 1,
        },
        {
            "title": "introduction",
            "texts": st.session_state["introduction-area"],
            "sections": [],
            "section_number": 2,
        }
    ]
    paper_body.extend(body)
    # 论文数据
    paper_data = {
        "paper_title": st.session_state["title-area"],
        "body": paper_body
    }
    paper_data = json.dumps(paper_data, indent=4)
    st.session_state["summary_result"] = summarize_api(text=paper_data, max_attempts=max_attempts)
    if "section_summaries" in st.session_state["summary_result"]:
        st.session_state["section_summaries"] = copy.deepcopy(get_section_summary(sections=st.session_state["summary_result"]["section_summaries"]))
    if "summary" in st.session_state["summary_result"]:
        st.session_state["summary"] = copy.deepcopy(st.session_state["summary_result"]["summary"])
    if "overall_assessment" in st.session_state["summary_result"]:
        st.session_state["overall_assessment"] = copy.deepcopy(st.session_state["summary_result"]["overall_assessment"])


def paper_polishing(max_attempts):
    """
    润色论文
    :param max_attempts: 最大重试次数
    """
    # 1. 润色论文标题, introduction, abstract
    st.session_state['polished_title'] = polish_api(text=st.session_state['title-area'], max_attempts=max_attempts)
    st.session_state["polished_introduction"] = polish_api(text=st.session_state["introduction-area"], max_attempts=max_attempts)
    st.session_state["polished_abstract"] = polish_api(text=st.session_state["abstract-area"], max_attempts=max_attempts)
    # 2. 润色论文正文
    st.session_state["polished_sections"] = copy.deepcopy(st.session_state["sections"])
    # 遍历正文，润色标题和正文

    def section_polish(section, max_attempts):
        """
        遍历章节及子章节，润色标题和论文
        :param section: 论文章节
        :param max_attempts: 最大重试次数
        """
        section['texts'] = polish_api(text=section['texts'], max_attempts=max_attempts)
        # 如果当前章节有子章节，则递归遍历子章节
        for subsection in section['sections']:
            section_polish(subsection, max_attempts=max_attempts)

    for section in st.session_state["polished_sections"]:
        section_polish(section=section, max_attempts=max_attempts)


def api_processing():
    """
    处理论文格式(段落格式、公式)，分析，润色
    """
    # 处理论文格式，根据st.session_state["translate_flag"]决定是否需要翻译
    # 论文润色：
    if st.session_state["polish_flag"]:
        print("paper polishing...")
        paper_polishing(max_attempts=max_attempts)
        print("finished.")
    # 论文翻译总结：
    else:
        print("paper translating...")
        print("step 1: 处理论文格式...")
        format_processing(max_attempts=max_attempts)
        print("step 2: 总结、评审论文...")
        # 总结、评审论文
        paper_analysis(max_attempts=max_attempts)
        print("finished.")



