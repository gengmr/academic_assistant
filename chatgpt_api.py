import json
import streamlit as st
import copy
from openai import OpenAI
from utils import escape_backslashes_except_newlines, add_section_numbers, get_section_summary
from config.config import chatgpt_model, base_url, paragraph_process_system_prompt, summarize_system_prompt, translate_system_prompt


def api_test():
    """
    测试api调用是否正常
    """
    client = OpenAI(
        api_key=st.session_state["api_key-area"],
        base_url=base_url
    )
    # 初始化设置为False
    st.session_state['api_flag'] = False
    try:
        response = client.chat.completions.create(
            model=chatgpt_model,
            temperature=0,
            messages=[
                {"role": "user", "content": "hello"}
            ]
        )
        _ = response.choices[0].message.content
        st.session_state['api_flag'] = True
    except Exception as e:
        print(e)


def paragraph_process_api(api_key, text):
    """
    通过第三方平台调用chatgpt api调整论文段落格式、公式显示及去除引用，并翻译为中文
    :param api_key: api key
    :param text: 需要处理的论文片段
    """
    # 将text中所有"替换为'避免json解析出现问题
    text = text.replace('"', "'")
    attempts = 0
    max_attempts = 1  # 最大尝试次数
    while attempts < max_attempts:
        try:
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            system_prompt = paragraph_process_system_prompt
            response = client.chat.completions.create(
                model=chatgpt_model,
                temperature=0,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {"role": "user", "content": text}
                ]
            )
            result = response.choices[0].message.content
            result = escape_backslashes_except_newlines(text=result)
            try:
                result = json.loads(result)
                en_context, zh_context = result['en_context'], result['zh_context']
                return en_context, zh_context
            except json.JSONDecodeError as e:  # 捕获json解析错误
                print(f"Attempt {attempts + 1} failed with error: {e}")
                attempts += 1
                continue
        except Exception as e:  # 捕获其他异常
            print(f"Attempt {attempts + 1} failed with error: {e}")
            attempts += 1

    # 所有尝试失败后的回退，按照输入文本返回
    en_context, zh_context = text, text
    return en_context, zh_context


def summarize_api(api_key, text):
    """
    ChatGPT API分析整篇文章
    """
    print(text)
    attempts = 0
    max_attempts = 1  # 最大尝试次数
    while attempts < max_attempts:
        try:
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            system_prompt = summarize_system_prompt
            response = client.chat.completions.create(
                model=chatgpt_model,
                temperature=0,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {"role": "user", "content": text}
                ]
            )
            result = response.choices[0].message.content
            print(result)
            result = escape_backslashes_except_newlines(text=result)
            try:
                result = json.loads(result)
                return result
            except json.JSONDecodeError as e:  # 捕获json解析错误
                print(f"Attempt {attempts + 1} failed with error: {e}")
                attempts += 1
                continue
        except Exception as e:  # 捕获其他异常
            print(f"Attempt {attempts + 1} failed with error: {e}")
            attempts += 1

    result = {"flag": "调用失败"}
    return result


def translate_api(api_key, text):
    """
    通过第三方平台调用chatgpt api翻译文本
    :param api_key: api key
    :param text: 文本
    """
    attempts = 0
    max_attempts = 1  # 最大尝试次数
    if text:
        while attempts < max_attempts:
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )
                system_prompt = translate_system_prompt
                response = client.chat.completions.create(
                    model=chatgpt_model,
                    temperature=0,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': text}
                    ]
                )
                result = response.choices[0].message.content
                try:
                    result = json.loads(result)
                    translation = result['zh_text']
                    return translation
                except json.JSONDecodeError as e:  # 捕获json解析错误
                    print(f"Attempt {attempts + 1} failed with error: {e}")
                    attempts += 1
                    continue
            except Exception as e:  # 捕获其他异常
                print(f"Attempt {attempts + 1} failed with error: {e}")
                attempts += 1

        # 所有尝试失败后的回退，按照输入文本返回
        translation = text
    else:
        translation = text
    return translation


def api_process():
    """
    通过chatgpt api处理论文信息，包括以下流程
    """
    # 1. 处理论文各章节格式、翻译
    # 1.1 翻译论文标题、论文机构、论文关键词
    st.session_state['zh_title-area'] = translate_api(api_key=st.session_state[f"api_key-area"],
                                                      text=st.session_state['title-area'])
    st.session_state['zh_institutes-area'] = translate_api(api_key=st.session_state[f"api_key-area"],
                                                      text=st.session_state['institutes-area'])
    st.session_state['zh_keywords-area'] = translate_api(api_key=st.session_state[f"api_key-area"],
                                                      text=st.session_state['keywords-area'])
    # 1.2 处理论文通用章节: abstract, introduction
    st.session_state['abstract_processed'], st.session_state['zh_abstract_processed'] = paragraph_process_api(
        api_key=st.session_state[f"api_key-area"], text=st.session_state["abstract-area"])
    st.session_state['introduction_processed'], st.session_state['zh_introduction_processed'] = paragraph_process_api(
        api_key=st.session_state[f"api_key-area"], text=st.session_state["introduction-area"])

    # 1.3 处理论文正文'
    def sections_process(en_section, zh_section, level=0):
        # 翻译章节标题为中文
        zh_section['title'] = translate_api(api_key=st.session_state[f"api_key-area"], text=en_section['title'])
        # 调整论文段落格式、公式显示及去除引用，并翻译为中文
        en_section['texts'], zh_section['texts'] = paragraph_process_api(api_key=st.session_state[f"api_key-area"], text=en_section['texts'])
        # 如果当前章节有子章节，则递归遍历子章节
        for en_subsection, zh_subsection in zip(en_section['sections'], zh_section['sections']):
            sections_process(en_subsection, zh_subsection, level + 1)

    # 1.4 创建sections的深拷贝，以分别处理英文和中文sections，直接赋值会指向同一数据，导致中英文正文结果相同
    st.session_state['sections_processed'] = copy.deepcopy(st.session_state['sections'])
    st.session_state['zh_sections_processed'] = copy.deepcopy(st.session_state['sections'])

    # 1.5 遍历并处理 en_sections 和 zh_sections 的每个章节
    for en_section, zh_section in zip(st.session_state['sections_processed'], st.session_state['zh_sections_processed']):
        sections_process(en_section, zh_section)

    # 2. 汇总英文论文的标题、摘要、导言、正文各部分内容，利用chatgpt api总结论文
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
    st.session_state["summary_result"] = summarize_api(api_key=st.session_state[f"api_key-area"], text=paper_data)
    if "section_summaries" in st.session_state["summary_result"]:
        st.session_state["section_summaries"] = copy.deepcopy(get_section_summary(sections=st.session_state["summary_result"]["section_summaries"]))
    if "summary" in st.session_state["summary_result"]:
        st.session_state["summary"] = copy.deepcopy(st.session_state["summary_result"]["summary"])
    if "overall_assessment" in st.session_state["summary_result"]:
        st.session_state["overall_assessment"] = copy.deepcopy(st.session_state["summary_result"]["overall_assessment"])


if __name__ == '__main__':
    api_key = 'sk-HuTWQZvHSLfgi3l51dB78851B4Da46Ba89796dFf565688Ca'
    text = """
Since our model contains no recurrence and no convolution, in order for the model to make use of the
order of the sequence, we must inject some information about the relative or absolute position of the
tokens in the sequence. To this end, we add "positional encodings" to the input embeddings at the
bottoms of the encoder and decoder stacks. The positional encodings have the same dimension dmodel
as the embeddings, so that the two can be summed. There are many choices of positional encodings,
learned and fixed [9].
In this work, we use sine and cosine functions of different frequencies:
P E(pos,2i) = sin(pos/100002i/dmodel)
P E(pos,2i+1) = cos(pos/100002i/dmodel)
where pos is the position and i is the dimension. That is, each dimension of the positional encoding
corresponds to a sinusoid. The wavelengths form a geometric progression from 2π to 10000 · 2π. We
chose this function because we hypothesized it would allow the model to easily learn to attend by
relative positions, since for any fixed offset k, P Epos+k can be represented as a linear function of
P E
pos.
We also experimented with using learned positional embeddings [9] instead, and found that the two
versions produced nearly identical results (see Table 3 row (E)). We chose the sinusoidal version
because it may allow the model to extrapolate to sequence lengths longer than the ones encountered
during training.
    """
    en_context, zh_context = paragraph_process_api(api_key=api_key, text=text)
    # print(en_context)
    # print()
    # print(zh_context)

    # text = "Google Brain, Google Research, University of Toronto"
    # translation = translate_api(api_key=api_key, text=text)
    # print(translation)

