import streamlit as st
import json
from init import initialize_session_state_variables
from st_on_hover_tabs import on_hover_tabs
from page import home_page, paper_entry_page, upload
from display_paper import display_paper
from style_css import apple_style


def main():
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
    apple_style()
    # 设置侧边栏样式
    st.markdown('<style>' + open('sidebar.css').read() + '</style>', unsafe_allow_html=True)
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['主页', '编辑', '导入', '查看'],
                             iconName=['home', 'edit', 'upload', 'article'], default_choice=0)
    if tabs == '主页':
        home_page()

    elif tabs == '编辑':
        paper_entry_page()

    elif tabs == '导入':
        upload()
        # 上传器，允许用户上传 JSON 文件来恢复会话状态
        uploaded_file = st.file_uploader(label="xxx", label_visibility="collapsed", type=['json'])

        if uploaded_file is not None:
            session_state_data = json.load(uploaded_file)
            for key, value in session_state_data.items():
                st.session_state[key] = value
            st.success('导入成功!')

    elif tabs == '查看':

        col1, col2 = st.columns([1, 1])  # 左右两侧分配相等的空间

        with col1:
            display_paper(
                language='en',
                title=st.session_state["title-area"],
                authors=st.session_state["authors-area"],
                institutes=st.session_state["institutes-area"],
                introduction=st.session_state["introduction_processed"],
                abstract=st.session_state["abstract_processed"],
                keywords=st.session_state["keywords-area"],
                body=st.session_state["sections_processed"],
                api_comments_flag=True,
                summary=st.session_state["summary"],
                section_summaries=st.session_state["section_summaries"],
                overall_assessment=st.session_state["overall_assessment"],
            )

        with col2:
            display_paper(
                language='zh',
                title=st.session_state["zh_title-area"],
                authors=st.session_state["authors-area"],
                institutes=st.session_state["zh_institutes-area"],
                introduction=st.session_state["zh_introduction_processed"],
                abstract=st.session_state["zh_abstract_processed"],
                keywords=st.session_state["zh_keywords-area"],
                body=st.session_state["zh_sections_processed"],
                api_comments_flag=True,
                summary=st.session_state["summary"],
                section_summaries=st.session_state["section_summaries"],
                overall_assessment=st.session_state["overall_assessment"],
            )


if __name__ == '__main__':
    main()