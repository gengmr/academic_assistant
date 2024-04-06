import streamlit.components.v1 as components
import streamlit_antd_components as sac
import streamlit as st
from utils import run_chapter_editor, save_session_state
from chatgpt_api import api_process, api_test


def home_page():
    """
    主页显示内容
    :return:
    """
    # HTML内容，包括使用不同字号的样式定义
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: 'Georgia', serif;
                margin: 20px;
            }
            h1 {
                font-size: 40px; /* 大标题的字号 */
                color: #333;
                text-align: center; /* 设置标题居中 */
                margin-bottom: 1em; /* 在h1和下一个元素之间添加一行的间隔 */
            }
            h2 {
                font-size: 25px; /* 次级标题的字号 */
                color: #333;
            }
            h3 {
                font-size: 20px; /* 第三级标题的字号 */
                color: #333;
            }
            p {
                font-size: 16px; /* 段落文本的字号 */
                text-align: justify;
                text-justify: inter-word;
            }
            ul {
                font-size: 16px; /* 列表项的字号 */
            }
        </style>
    </head>
    <body>
        <h1>Scholar Assistant</h1>

        <h2>软件概述</h2>
        <p>Scholar Assistant 是一款专注于提高学术论文管理和阅读效率的工具。它提供了一个用户友好的界面，使用户能够高效地录入、查看和管理学术论文。</p>

        <h2>主要功能</h2>
        <ul>
            <li><strong>中英文对照查看：</strong>支持中英文对照查看论文内容。</li>
            <li><strong>结构化显示：</strong>结构化显示论文内容及其分析结果。</li>
            <li><strong>多论文管理与标星功能：</strong>可管理多篇论文及标记重要的论文。</li>
        </ul>

        <h2>使用步骤</h2>
        <h3>1. 录入数据</h3>
        <p>用户可通过以下两种方式录入论文数据信息：</p>
        <p>(1) 点击软件侧边栏的“编辑”功能，输入论文基础信息（标题、作者、机构、年份、发表刊物）、论文通用章节（摘要、关键词、引言、相关工作）、论文正文。点击“分析”按钮使用ChatGPT API进行汇总分析。</p>
        <p>(2) 点击软件侧边栏的“导入”功能，通过json文件导入论文数据</p>
        <h3>2. 保存</h3>
        <p>点击软件侧边栏的“编辑”功能，在"Step 4-API分析"中点击"保存按钮"将数据保存为文件</p>
        <h3>3. 阅读论文</h3>
        <p>点击软件侧边栏的“查看”功能，用户可以选择并阅读感兴趣的论文，包括论文概要、论文内容和ChatGPT分析结果。</p>
        
        <div class="version-history">
            <h2>版本记录</h2>
            <ul>
                <li>
                    <strong>v1.0 (2024.4.6):</strong>
                    <p>初始发布版本。包括论文编辑、保存、API调用、文件导入、中英文对照查看功能。</p>
                </li>
                <!-- 未来版本更新在这里添加新的列表项 -->
            </ul>
        </div>
    </body>
    </html>
    """

    # 使用components.html渲染HTML内容
    components.html(html_content, height=1200)


def create_text_area(placeholder, key, height=0):
    """
    输入论文文本
    :param placeholder: 占位符
    :param key: text_area的key
    :param height: 高度
    :return:
    """

    def on_text_area_change():
        st.session_state[key + "-area"] = st.session_state[key]

    st.text_area(
        label="xxx",  # 非空即可
        height=height,
        label_visibility="collapsed",
        placeholder=placeholder,
        value=st.session_state.get(key + "-area", ""),  # 从 session_state 获取初始值
        key=key,
        on_change=on_text_area_change
    )


def paper_entry_page():
    """
    编辑页显示内容：中英文论文信息录入，包含
    基本信息：
        标题、作者、所属机构、发表年份、发表刊物、
    通用章节：
        论文摘要、关键词、引言、相关工作
    正文：
        根据不同文章会有不同
    :return:
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: 'Georgia', serif;
                margin: 22px;
            }
            h1 {
                font-size: 20px; /* 字号 */
                color: #333;
                text-align: center; /* 设置标题居中 */
                margin-bottom: 0em; /* 在h1和下一个元素之间不添加间隔 */
            }
        </style>
    </head>
    <body>
        <h1>论文信息录入</h1>
    </body>
    </html>
    """

    components.html(html_content, height=62)

    tab = sac.steps(
        items=[
            sac.StepsItem(title='step 1', description='基本信息'),
            sac.StepsItem(title='step 2', description='通用章节'),
            sac.StepsItem(title='step 3', description='正文'),
            sac.StepsItem(title='step 4', description='API分析'),
        ], format_func='title'
    )

    if tab == 'step 1':
        # 定义输入项目
        info_items = [
            ("标题", "title", 55),
            ("作者", "authors", 55),
            ("所属机构", "institutes", 55),
            ("发表时间", "publish_time", 55),
            ("发表刊物", "publication", 55)
        ]
    
        # 创建输入框录入论文信息：
        with st.expander(label="论文基本信息录入（不存在项可为空）", expanded=True):
            for info_zh, key, height in info_items:
                placeholder = f"请输入论文{info_zh}"
                create_text_area(placeholder=placeholder, key=key, height=height)

    if tab == 'step 2':
        # 定义输入项目
        info_items = [
            ("摘要", "abstract", 300),
            ("关键词", "keywords", 55),
            ("引言", "introduction", 300),
        ]

        # 创建输入框录入论文信息：
        with st.expander(label="论文基本信息录入（不存在项可为空）", expanded=True):
            for info_zh, key, height in info_items:
                placeholder = f"请输入论文{info_zh}"
                create_text_area(placeholder=placeholder, key=key, height=height)

    if tab == 'step 3':
        run_chapter_editor()

    if tab == 'step 4':
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                font-family: 'Georgia', serif;
                margin: 20px;
                }
                h1 {
                    font-size: 20px; /* 字号 */
                    color: #333;
                    text-align: left; /* 设置标题居中 */
                    margin-bottom: 0em; /* 在h1和下一个元素之间不添加间隔 */
                }
            </style>
        </head>
        <body>
            <h1>步骤说明</h1>
                <p>Step1: 填写API Key</p>
                <p>Step2: 点击"测试"按钮，测试API调用是否正常</p>
                <p>Step3: 点击"提交"按钮(为防止程序错误，前面两步运行正常后显示)，调用API进行论文翻译、汇总</p>
        </body>
        </html>
        """

        components.html(html_content, height=150)

        key = "api_key"
        placeholder = "请输入API Key"

        col1, col2 = st.columns([8, 1])
        with col1:
            create_text_area(placeholder=placeholder, key=key, height=55)
        with col2:
            st.button(label="测试", on_click=api_test)

        if not st.session_state["api_key-area"]:
            st.error('1. API Key未填入！')
        else:
            st.success("1. API Key已填写！")

        if not st.session_state["api_flag"]:
            st.error('2. API调用测试失败！')
        else:
            st.success("2. API调用测试成功！")

        col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])
        with col2:
            if st.session_state["api_key-area"] and st.session_state["api_flag"]:
                st.button("提交", key=f"chatgpt_api_button", on_click=api_process)
        with col4:
            st.download_button(
                label="保存",
                data=save_session_state(),
                file_name=f"{st.session_state['title-area']}.json",
                mime="application/json"
            )


def upload():
    """
    上传论文信息以便阅读
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: 'Georgia', serif;
                margin: 20px;
            }
            h1 {
                font-size: 30px; /* 大标题的字号 */
                color: #333;
                text-align: center; /* 设置标题居中 */
                margin-bottom: 0em; /* 在h1和下一个元素之间不添加间隔 */
            }
            h2 {
                font-size: 16px; /* 正文字号 */
                color: #333;
                text-align: left; /* 设置标题居中 */
                margin-bottom: 0em; /* 在h1和下一个元素之间不添加间隔 */
            }
        </style>
    </head>
    <body>
        <h1>论文上传</h1>
        <h2>点击按钮上传，显示"导入成功!"后，点击"×"关闭导入文件</h2>
    </body>
    </html>
    """
    components.html(html_content, height=100)






