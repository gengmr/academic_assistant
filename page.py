import streamlit.components.v1 as components
import streamlit_antd_components as sac
import streamlit as st
import json
from datetime import datetime, timedelta
from utils import run_chapter_editor, save_session_state
from chatgpt_api import test_api, api_processing
from display_paper import display_paper


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
        <h3>2. 下载</h3>
        <p>点击软件侧边栏的“编辑”功能，在"Step 4-API分析"中点击"下载"按钮将数据保存为文件</p>
        <h3>3. 阅读论文</h3>
        <p>点击软件侧边栏的“查看”功能，用户可以选择并阅读感兴趣的论文，包括论文概要、论文内容和ChatGPT分析结果。</p>
        
        <div class="version-history">
            <h2>版本记录</h2>
            <ul>
                <li>
                    <strong>v1.0 (2024.4.6):</strong>
                    <p>初始发布版本。包括论文编辑、保存、API调用、文件导入、中英文对照查看功能。</p>
                </li>
                <li>
                    <strong>v2.0 (2024.4.8):</strong>
                    <p>更新论文小助手功能，可以显示分析结果，更换图标</p>
                    <p>显示界面支持更换字体</p>
                </li>
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
            sac.StepsItem(title='step 4', description='API Key'),
        ], format_func='title'
    )

    if tab == 'step 1':
        # 定义输入项目
        info_items = [
            ("标题", "title", 55),
            ("作者", "authors", 55),
            ("所属机构", "institutes", 55),
            ("发表刊物", "publication", 55),
        ]

        def on_select_date_change():
            st.session_state[f"publish_time"] = st.session_state[f"publish_time-date"].strftime("%Y-%m-%d")

        # 设置日期选择的最小值和最大值
        min_date = datetime.now() - timedelta(days=30 * 365)  # 30年前
        max_date = datetime.now()  # 当天
        publish_time = st.session_state.get("publish_time", None)
        if publish_time:
            publish_time = datetime.strptime(publish_time, "%Y-%m-%d").date()
            selected_date = st.date_input("论文发表日期", value=publish_time, key="publish_time-date",
                                          on_change=on_select_date_change, min_value=min_date, max_value=max_date)
        else:
            selected_date = st.date_input("论文发表日期", key="publish_time-date", on_change=on_select_date_change,
                                          min_value=min_date, max_value=max_date)

        # 如果用户选择了日期，更新session state中的 'publish_time'
        if selected_date:
            formatted_date = selected_date.strftime("%Y-%m-%d")
            st.session_state['publish_time'] = formatted_date
    
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
                <p>Step3: 点击"提交"按钮(为防止调用API时缺失API Key信息导致程序报错，在前两步运行正常后显示)，调用ChatGPT API进行论文翻译、汇总</p>
                <p>Step4: 点击"下载"按钮将论文元数据和分析数据下载为文件以便下次查看</p>
        </body>
        </html>
        """

        components.html(html_content, height=150)

        st.session_state["openai_service"] = sac.switch(label='是否使用官方API', value=False)
        col1, col2 = st.columns([8, 1])
        with col1:
            create_text_area(placeholder="请输入API Key", key="api_key", height=55)
        with col2:
            st.button(label="测试", on_click=test_api)

        if not st.session_state[f"api_key-area"]:
            st.error('1. API Key未填入！')
        else:
            st.success("1. API Key已填写！")

        if not st.session_state["api_flag"]:
            st.error('2. API调用测试失败！')
        else:
            st.success("2. API调用测试成功！")
        col1, col2 = st.columns([1, 1.15])
        with col2:
            # 定义文件名生成逻辑
            def generate_file_name():
                if st.session_state['publish_time']:
                    return f"{st.session_state['publish_time']} {st.session_state['title-area']}.json"
                else:
                    return f"{st.session_state['title-area']}.json"
            st.download_button(
                label="下载",
                data=save_session_state(),
                file_name=generate_file_name(),  # 论文标题作为保存名称
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
                font-size: 20px; /* 大标题的字号 */
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

    # 上传器，允许用户上传 JSON 文件来恢复会话状态
    uploaded_file = st.file_uploader(label="xxx", label_visibility="collapsed", type=['json'])

    if uploaded_file is not None:
        session_state_data = json.load(uploaded_file)
        # 清空当前的session state
        st.session_state.clear()
        for key, value in session_state_data.items():
            st.session_state[key] = value
        st.success('导入成功!')


def analysis():
    """
    使用ChatGPT对论文进行分析
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
                font-size: 20px; /* 大标题的字号 */
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
        <h1>论文分析</h1>
        <h2>1. 完成"编辑"页面论文信息录入，填写正确的API信息并通过测试</h2>
        <h2>2. 选择选项进行处理，处理过程中页面会呈现阻塞状态，请耐心等待</h2>
    </body>
    </html>
    """
    components.html(html_content, height=150)

    # 如果填写API Key且测试成功
    if st.session_state[f"api_key-area"] and st.session_state["api_flag"]:
        api_service = sac.segmented(
            items=[
                sac.SegmentedItem(label="总结"),
                sac.SegmentedItem(label="润色")
            ], label='', align='center', color='teal', use_container_width=True
        )
        if api_service == "总结":
            st.session_state["polish_flag"] = False
            st.markdown(st.session_state["polish_flag"])
            st.session_state["translate_flag"] = sac.switch(label='是否翻译', value=False)
            st.button("提交", key=f"chatgpt_api_button", on_click=api_processing)
            if st.session_state["summary_result"]:
                try:
                    st.markdown("ChatGPT总结结果如下：")
                    st.json(st.session_state["summary_result"])
                except:
                    pass
        elif api_service == "润色":
            st.session_state["translate_flag"] = False
            st.session_state["polish_flag"] = True
            st.markdown(st.session_state["polish_flag"])
            st.session_state["polish_language_is_english"] = sac.switch(label='英文润色', value=False)
            st.button("提交", key=f"chatgpt_api_button", on_click=api_processing)
    else:
        st.error('请在"编辑-分析保存"页面填写正确的API Key信息，并通过API调用测试！')


def display():
    font_key = 'font'
    icon_key = "ChatGPT_icon"
    selected_icon = "🦄"
    col11, col12, col13, col14 = st.columns([0.5, 1.3, 1, 1])
    with col11:
        display_mode_key = "display_model"

        # 定义下拉列表内容变化时的回调函数
        def on_select_area_change():
            st.session_state[display_mode_key + "-selectbox"] = st.session_state[display_mode_key + "-select"]

        display_mode_options = ["翻译模式", "润色模式"]
        selected_display_mode = st.selectbox(
            label="xxx",  # 非空即可
            options=display_mode_options,
            index=display_mode_options.index(
                st.session_state.get(display_mode_key + "-selectbox", display_mode_options[0])),
            key=display_mode_key + "-select",
            on_change=on_select_area_change,
            label_visibility="collapsed"
        )

    with col13:
        api_comments_flag = sac.switch(label='论文小助手', value=True)
    with col14:
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

    if selected_display_mode == "翻译模式":
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
                api_comments_flag=False,
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

    elif selected_display_mode == "润色模式":
        with col21:
            display_paper(
                language='en',
                font=selected_font,
                title=st.session_state["title-area"],
                authors=st.session_state["authors-area"],
                institutes=st.session_state["institutes-area"],
                introduction=st.session_state["introduction-area"],
                abstract=st.session_state["abstract-area"],
                keywords=st.session_state["keywords-area"],
                body=st.session_state["sections"],
                api_comments_flag=False,
                selected_icon=selected_icon,
                summary=st.session_state["summary"],
                section_summaries=st.session_state["section_summaries"],
                overall_assessment=st.session_state["overall_assessment"],
            )

        with col22:
            display_paper(
                language='en' if st.session_state["polish_language_is_english"] else "zh",
                font=selected_font,
                title=st.session_state["polished_title"],
                authors=st.session_state["authors-area"],
                institutes=st.session_state["institutes-area"],
                introduction=st.session_state["polished_introduction"],
                abstract=st.session_state["polished_abstract"],
                keywords=st.session_state["keywords-area"],
                body=st.session_state["polished_sections"],
                api_comments_flag=api_comments_flag,
                selected_icon=selected_icon,
                summary=st.session_state["summary"],
                section_summaries=st.session_state["section_summaries"],
                overall_assessment=st.session_state["overall_assessment"],
            )


