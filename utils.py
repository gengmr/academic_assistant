import streamlit as st
import streamlit_nested_layout  # ！！注意，此代码虽然没有调用，但支持嵌套的展开器（expander），不能删除
import uuid
import tiktoken
import re
import json


def escape_backslashes_except_newlines(text):
    """
    除了文本中的换行符 `\n` 之外，将所有单独的反斜线 `\` 转换为双反斜线 `\\`。

    :param text: 需要进行处理的原始文本字符串。
    :type text: str
    :return: 处理后的字符串，其中除了换行符 `\n` 外的所有反斜线都被转换成双反斜线。
    :rtype: str
    """
    # 使用正则表达式替换不是换行符一部分的反斜线
    # 正则表达式 `\\\\(?!\n)` 匹配所有不紧跟着 `n` 的反斜线，并将其替换为双反斜线
    # 这里使用了负向前瞻断言 (?!\n)，确保不匹配换行符的反斜线
    return re.sub(r'\\(?!n)', r'\\\\', text)


def save_session_state():
    """
    保存st.session_state到JSON文件中
    """
    # 将 st.session_state 转换为标准字典
    keys_to_save = [
        "title-area",
        "authors-area",
        "institutes-area",
        "publication",
        "publish_time",
        "introduction_processed",
        "abstract_processed",
        "keywords-area",
        "sections",
        "sections_processed",
        "summary",
        "section_summaries",
        "overall_assessment",
        "zh_title-area",
        "zh_institutes-area",
        "zh_introduction_processed",
        "zh_abstract_processed",
        "zh_keywords-area",
        "zh_sections_processed",
        "introduction-area",
        "abstract-area",
        "sections",
        "polish_language_is_english",
        "polished_title",
        "polished_introduction",
        "polished_abstract",
        "polished_sections"
    ]
    session_state_dict = {key: st.session_state[key] for key in keys_to_save if key in st.session_state}    # 序列化转换后的字典
    session_state_json = json.dumps(session_state_dict, indent=4, ensure_ascii=False)
    return session_state_json


def run_chapter_editor():
    """
    运行章节编辑器应用。该应用允许用户通过图形界面添加、编辑、删除文档的章节。

    st.session_state['sections']结构说明：
    - id (str): 章节的唯一标识符，使用UUID生成。
    - title (str): 章节的标题。
    - texts (str): 章节的文本内容。
    - sections (list): 子章节列表，每个元素遵循章节的结构。

    示例：
    [
        {
            "id": "uuid1",
            "title": "章节 1",
            "texts": "章节 1 的内容",
            "sections": [
                {
                    "id": "uuid2",
                    "title": "子章节 1.1",
                    "texts": "子章节 1.1 的内容",
                    "sections": []
                }
            ]
        }
    ]

    应用逻辑：
    1. 初始化章节数据或从session_state获取现有数据。
    2. 使用递归函数展示所有章节及其操作按钮。
    3. 支持动态地通过按钮添加同级章节、子章节，或删除章节。
    """
    if 'sections' not in st.session_state or st.session_state['sections'] == []:
        init_id = str(uuid.uuid4())
        st.session_state['sections'] = [{"flag": True, "id": init_id, "title": "", "texts": "", "sections": []}]

    display_sections(st.session_state['sections'], parent_id=None, chapter_number="")

    if st.checkbox("显示数据预览"):
        st.json(st.session_state['sections'])


def display_sections(sections, parent_id, chapter_number):
    """
    用于显示论文正文内容，允许用户编辑章节标题和内容，并提供添加、删除章节的功能。该函数递归调用自身以处理嵌套章节。

    :param sections: 包含章节信息的列表，每个章节为一个字典，包含章节ID、标题、正文内容和子章节列表。
    :param parent_id: 当前章节列表的父章节ID。如果当前章节为顶级章节，则为None。
    :param chapter_number: 当前章节的编号。用于显示章节层级和顺序，顶级章节为""，子章节以"1.1", "1.2"等形式表示。
    """
    sections_to_remove = []
    for index, section in enumerate(sections):
        current_chapter_number = f"{chapter_number}.{index + 1}" if chapter_number else str(index + 2)

        if section['flag']:
            st.session_state[f"{section['id']}_title_change"] = section['title']
            title_key = f"{section['id']}_title_change"
            with st.expander(f"Chapter {current_chapter_number} {st.session_state[title_key]}", expanded=True):
                # 定义标题变化时的回调函数
                def on_title_change():
                    st.session_state[f"{section['id']}_title_change"] = st.session_state[f"{section['id']}_title"]

                # 定义正文内容变化时的回调函数
                def on_texts_change():
                    st.session_state[f"{section['id']}_texts_change"] = st.session_state[f"{section['id']}_texts"]

                # 创建标题输入区
                section['title'] = st.text_area(label="xxx", label_visibility="collapsed", placeholder='请输入章节标题', value=st.session_state.get(f"{section['id']}_title_change", section['title']),
                                                key=f"{section['id']}_title", height=55, on_change=on_title_change)

                # 创建正文内容输入区
                section['texts'] = st.text_area(label="xxx", label_visibility="collapsed", placeholder='请输入章节内容', value=st.session_state.get(f"{section['id']}_texts_change", section['texts']),
                                                key=f"{section['id']}_texts", height=150, on_change=on_texts_change)

                col1, col2, col3 = st.columns([1.45, 1.6, 0.4])
                with col1:
                    if st.button("单击添加子章节", key=f"{section['id']}_add_child"):
                        child_id = str(uuid.uuid4())
                        section['sections'].append({"flag": True, "id": child_id, "title": "", "texts": "", "sections": []})
                with col2:
                    if st.button("单击添加同级章节", key=f"{section['id']}_add_sibling"):
                        sibling_id = str(uuid.uuid4())
                        new_section = {"flag": True, "id": sibling_id, "title": "", "texts": "", "sections": []}
                        if parent_id is None:
                            st.session_state['sections'].insert(index + 1, new_section)
                        else:
                            parent_section = find_section(st.session_state['sections'], parent_id)
                            parent_section['sections'].insert(index + 1, new_section)
                with col3:
                    if st.button("双击删除本章节", key=f"{section['id']}_delete"):
                        section["flag"] = False
                        if parent_id is None:
                            sections_to_remove.append(section)
                        else:
                            parent_section = find_section(st.session_state['sections'], parent_id)
                            del parent_section['sections'][index]

                if section['sections']:
                    display_sections(section['sections'], section['id'], current_chapter_number)

    # Remove sections after iterating to avoid modifying list while iterating
    for section in sections_to_remove:
        sections.remove(section)


def find_section(sections, id):
    """
    递归查找具有指定ID的章节。

    :param sections: 包含章节信息的列表，每个章节为一个字典，包含章节ID、标题、正文内容和子章节列表。
    :param id: 需要查找的章节ID。
    :return: 如果找到具有指定ID的章节，则返回该章节的字典；如果未找到，则返回None。
    """
    for section in sections:
        if section['id'] == id:
            return section
        sub_section_result = find_section(section['sections'], id)
        if sub_section_result:
            return sub_section_result
    return None


def calculate_token(text):
    """
    计算文本token
    """
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    # 统计tokens的数量
    num_tokens = len(tokens)

    return num_tokens


def add_section_numbers(body, number_prefix=None):
    """
    为论文正文的每个章节和子章节添加章节编号，并去除章节中的'id'和'flag'字段。
    章节编号从3开始，并根据章节的层次结构递增（如3, 3.1, 3.1.1等）。

    :param body: 论文正文的结构，一个列表，其中每个元素代表一个章节，每个章节包含标题(title)、正文(texts)、
                 可选的子章节列表(sections)、以及其他字段如id和flag。函数会移除章节中的id和flag字段。
                 例如：
                 [
                     {
                         "id": "xxx",
                         "title": "章节标题",
                         "texts": "章节正文内容",
                         "flag": "important",
                         "sections": [...]
                     },
                     ...
                 ]
    :param number_prefix: 内部使用，用于记录当前处理章节的编号前缀。调用时通常不需要传递或传递None。
    """
    if number_prefix is None:
        number_prefix = [2]  # 初始化章节编号前缀为2，使得第一个章节的编号为3
    else:
        number_prefix.append(0)  # 进入新的子章节层级时，添加一个新的层级编号

    for section in body:
        number_prefix[-1] += 1  # 更新当前层级的章节编号
        section_number = '.'.join(map(str, number_prefix))  # 将编号列表转换为字符串形式
        section['section_number'] = section_number  # 为当前章节添加章节号字段

        # 移除'id'和'flag'字段
        section.pop('id', None)
        section.pop('flag', None)

        # 如果有子章节，递归调用该函数处理子章节
        if 'sections' in section:
            add_section_numbers(section['sections'], number_prefix.copy())  # 使用编号的副本，以防修改影响其他章节

    # 在返回之前，确保移除当前层级的编号，以避免影响同级的其他章节
    number_prefix.pop()

    return  body


def get_section_summary(sections, result=None):
    """
    获取章节号-段落总结字典，其中段落总结由ChatGPT API生成
    所有章节号均减去1，因为显示时abstract不计入章节号。其中第0章代表abstract章节
    """
    def adjust_section_number(section_number):
        # 将章节号分割为顶级章节号和其余部分
        parts = str(section_number).split('.')
        # 只减少顶级章节号
        parts[0] = str(int(parts[0]) - 1)
        # 重新组合章节号
        return '.'.join(parts)
    if result is None:
        result = {}

    for section in sections:
        original_section_number = section['section_number']
        content_summary = section['content_summary']

        # 调整章节号，对顶级章节号减1
        adjusted_section_number = adjust_section_number(original_section_number)

        # 将信息添加到结果字典中
        result[adjusted_section_number] = content_summary

        # 如果有子章节，递归处理子章节
        if 'sections' in section and section['sections']:
            get_section_summary(section['sections'], result)

    return result

