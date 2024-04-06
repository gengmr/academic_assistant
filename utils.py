import streamlit as st
import streamlit_nested_layout  # ！！注意，此代码虽然没有调用，但支持嵌套的展开器（expander），不能删除
import uuid
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
    # 保存st.session_state到JSON
    """
    # 将 st.session_state 转换为标准字典
    session_state_dict = {key: value for key, value in st.session_state.items()}
    # 序列化转换后的字典
    session_state_json = json.dumps(session_state_dict, indent=4)
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


def chatgpt_api_process():
    """
    通过chatgpt api处理
    """
    # step1. 翻译论文标题


