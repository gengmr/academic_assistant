import streamlit as st
import json
import streamlit_antd_components as sac
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
        font_key = 'font'
        icon_key = "ChatGPT_icon"
        selected_icon = "🦄"
        col11, col12, col13 = st.columns([1.8, 1, 1])
        with col12:
            api_comments_flag = sac.switch(label='论文小助手', value=False)

        with col13:
            col131, col132 = st.columns([1, 1])
            if api_comments_flag:
                # 论文小助手图标选择
                with col131:
                    # 定义下拉列表内容变化时的回调函数
                    def on_select_area_change():
                        st.session_state[f"{icon_key}-selectbox"] = st.session_state[f"{icon_key}-select"]
                        # 更新图标列表并保存
                        if st.session_state[f"{icon_key}-select"] in st.session_state["chatgpt_icon_options"]:
                            st.session_state["chatgpt_icon_options"].remove(st.session_state[f"{icon_key}-select"])
                        st.session_state["chatgpt_icon_options"].insert(0, st.session_state[f"{icon_key}-select"])
                        with open("config/ChatGPT_icons.json", "w", encoding='utf8') as file:
                            json.dump(st.session_state["chatgpt_icon_options"], file, indent=4, ensure_ascii=False)

                    options = st.session_state[f"chatgpt_icon_options"]
                    selected_icon = st.selectbox(
                        label="xxx",  # 非空即可
                        options=options,
                        index=options.index(st.session_state.get(f"{icon_key}-selectbox", options[0])),
                        key=icon_key + "-select",
                        on_change=on_select_area_change,
                        label_visibility="collapsed"
                    )

            # 字体选择
            with col132:
                # 定义下拉列表内容变化时的回调函数
                def on_select_area_change():
                    st.session_state[f"{font_key}-selectbox"] = st.session_state[f"{font_key}-select"]
                    # 更新图标列表并保存
                    if st.session_state[f"{font_key}-select"] in st.session_state["font_options"]:
                        st.session_state["font_options"].remove(st.session_state[f"{font_key}-select"])
                    st.session_state["font_options"].insert(0, st.session_state[f"{font_key}-select"])
                    with open("config/fonts.json", "w", encoding='utf8') as file:
                        json.dump(st.session_state["font_options"], file, indent=4, ensure_ascii=False)

                options = st.session_state["font_options"]
                selected_font = st.selectbox(
                    label="xxx",  # 非空即可
                    options=options,
                    index=options.index(st.session_state.get(f"{font_key}-selectbox", options[0])),
                    key=font_key + "-select",
                    on_change=on_select_area_change,
                    label_visibility="collapsed"
                )

        col21, col22 = st.columns([1, 1])  # 左右两侧分配相等的空间

        with col21:
            display_paper(
                language='en',
                font=selected_font,
                title=st.session_state["title-area"],
                authors=st.session_state["authors-area"],
                institutes=st.session_state["institutes-area"],
                introduction=st.session_state["introduction_processed"],
                abstract=st.session_state["abstract_processed"],
                keywords=st.session_state["keywords-area"],
                body=st.session_state["sections_processed"],
                api_comments_flag=api_comments_flag,
                selected_icon=selected_icon,
                summary=st.session_state["summary"],
                section_summaries=st.session_state["section_summaries"],
                overall_assessment=st.session_state["overall_assessment"],
            )

        with col22:
            display_paper(
                language='zh',
                font=selected_font,
                title=st.session_state["zh_title-area"],
                authors=st.session_state["authors-area"],
                institutes=st.session_state["zh_institutes-area"],
                introduction=st.session_state["zh_introduction_processed"],
                abstract=st.session_state["zh_abstract_processed"],
                keywords=st.session_state["zh_keywords-area"],
                body=st.session_state["zh_sections_processed"],
                api_comments_flag=api_comments_flag,
                selected_icon=selected_icon,
                summary=st.session_state["summary"],
                section_summaries=st.session_state["section_summaries"],
                overall_assessment=st.session_state["overall_assessment"],
            )


if __name__ == '__main__':
    main()