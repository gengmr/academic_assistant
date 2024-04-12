import streamlit.components.v1 as components


def create_section_html(sections, section_summaries, api_comments_flag, selected_icon, level=1, num_prefix=""):
    """
    递归地生成HTML内容，用于表示文档或文章的层次结构化节(section)。

    :param sections: 包含文档各节信息的列表。每个节可以有标题("title")、文本("texts")，以及子节("sections")。
                     其中，"texts"是通过换行符('\n')分隔的字符串，表示一个或多个段落。
                     "sections"是包含更多此类节信息的列表，允许递归地构建文档结构。
    :param section_summaries: ChatGPT API生成的论文分章节总结内容，字典形式，键为章节号（其中0代表abstract），值为总结内容。
    :param api_comments_flag: 是否显示ChatGPT API汇总结果，布尔形式。
    :param level: 当前节的HTML标题等级。默认为1，表示顶级节用<h2>标签，因为HTML中<h1>通常保留给页面标题。
                  该参数随着递归进入子节而增加，用于生成适当等级的HTML标题标签。
    :param num_prefix: 用于前缀章节编号的字符串。在递归处理子节时，该前缀会根据父节的编号和当前子节的序号更新，以反映节的层次结构。
                       例如，顶级节为"1."，其第一个子节为"1.1."，依此类推。

    :return: 一个表示输入节结构的HTML字符串。包括标题、段落以及根据层次嵌套的子节。
    """
    html_content = ""
    section_counter = 1

    for item in sections:
        # 在每个可能的路径中确保current_num都被赋值
        current_num = f"{num_prefix}{section_counter}." if num_prefix else f"{section_counter}."

        # 处理章节标题
        if 'title' in item:
            # 添加HTML标题，级别由当前level决定
            html_content += f"<h{level + 1}>{current_num} {item['title']}</h{level + 1}>"
            section_counter += 1  # 更新章节计数器
            # 如果api_comments_flag为True，则增加注释显示
            if api_comments_flag and current_num[:-1] in section_summaries:  # 去掉末尾的点
                html_content += f'<p class="note-paragraph">{selected_icon}[{current_num} {item["title"]}-章节概述]:{section_summaries[current_num[:-1]]}</p>'

        # 处理单一字符串形式的多段文本
        if 'texts' in item:
            # 分割文本为段落
            paragraphs = item['texts'].split('\n')
            for paragraph in paragraphs:
                # 为每个段落添加<p>标签
                html_content += f'<p class="paragraph">{paragraph}</p>'

        # 递归处理子章节
        if 'sections' in item:
            # 递归调用，增加层级，更新编号前缀，此时current_num已定义
            html_content += create_section_html(item['sections'], section_summaries, api_comments_flag, selected_icon, level + 1, current_num)

    return html_content


def display_paper(language, font, title, authors, institutes, introduction, abstract, keywords, body, api_comments_flag, selected_icon, summary, section_summaries, overall_assessment):
    """
    在streamlit中显示论文。

    :param language: 语言，"en" or "zh"
    :param font: 页面显示字体，字符串格式。
    :param title: 论文的标题，字符串格式。
    :param authors: 论文作者，字符串格式。
    :param institutes: 作者所属机构名称，字符串格式。
    :param introduction: 论文的引言，字符串格式。
    :param abstract: 论文的摘要，字符串格式。
    :param keywords: 论文关键词，字符串格式。
    :param body: 论文正文内容，以列表形式组织，列表中的每个元素是一个字典，包含"title"、"texts"和可选的"sections"键。
                 "title"键对应章节的标题，为字符串格式。
                 "texts"键对应章节的正文内容，为字符串格式，可以包含多段，使用"\n"进行分段。
                 "sections"键是可选的，对应于子章节，其值为一个列表，列表中的每个元素也是一个字典，包含"title"和"texts"键及可选的"sections"键，结构与上级相同。
    :param api_comments_flag: 是否显示ChatGPT API汇总结果，布尔形式
    :param selected_icon: 论文助手图标
    :param summary: ChatGPT API对整篇论文概述，字符串形式
    :param section_summaries: ChatGPT API生成的论文分章节总结内容，字典形式，键为章节号（其中0代表abstract），值为总结内容。
    :param overall_assessment: ChatGPT API对整篇论文评估，列表形式，


    本函数将输入的论文信息整合成一个HTML格式的模板，并使用Streamlit库的markdown方法进行显示。该函数设计用于展示论文的结构化内容，包括标题、作者、机构、摘要、关键词以及正文。
    """
    # 根据语言选择Abstract和Keywords的标题
    abstract_title = "Abstract" if language == "en" else "摘要"
    keywords_title = "Keywords" if language == "en" else "关键词"
    introduction_title = "Introduction" if language == "en" else "引言"
    # 将引言部分作为正文的第一节
    introduction_section = [{"title": f"{introduction_title}", "texts": introduction}]
    # 创建正文HTML
    body_html = create_section_html(introduction_section + body, section_summaries, api_comments_flag, selected_icon)
    # abstract注释(ChatGPT API生成的中文总结)
    if api_comments_flag:
        self_introduction = f'<p class="note">{selected_icon}[自我介绍]:您好⊂◉‿◉つ！我是论文小助理，我会为您耐心、专业地讲解论文。在论文的开头，我会为您提供"论文概述"以及我对论文"研究主题"、"研究成果"、"研究方法"、"创新点"、"数据集"、"写作逻辑"的总结和评价，并给出我对论文的总体评价。在正文中，我会对每一章节的内容进行汇总，方便您高效阅读论文。下面让我们开始吧！</p>'
    else:
        self_introduction = ""

    if api_comments_flag and summary:
        paper_summary = f'<p class="note">{selected_icon}[论文概述]:{summary}</p>'
    else:
        paper_summary = ""

    if api_comments_flag and "research_topic" in overall_assessment:
        paper_research_topic = f'<p class="note">{selected_icon}[研究主题]:{overall_assessment["research_topic"]}</p>'
    else:
        paper_research_topic = ""

    if api_comments_flag and "research_outcomes" in overall_assessment:
        paper_research_outcomes = f'<p class="note">{selected_icon}[研究成果]:{overall_assessment["research_outcomes"]}</p>'
    else:
        paper_research_outcomes = ""

    if api_comments_flag and "methodology" in overall_assessment:
        paper_methodology = f'<p class="note">{selected_icon}[研究方法]:{overall_assessment["methodology"]}</p>'
    else:
        paper_methodology = ""

    if api_comments_flag and "innovations" in overall_assessment:
        paper_innovations = f'<p class="note">{selected_icon}[创新点]:{overall_assessment["innovations"]}</p>'
    else:
        paper_innovations = ""

    if api_comments_flag and "dataset_description" in overall_assessment:
        paper_dataset_description = f'<p class="note">{selected_icon}[数据集]:{overall_assessment["dataset_description"]}</p>'
    else:
        paper_dataset_description = ""

    if api_comments_flag and "paper_structure" in overall_assessment:
        paper_structure = f'<p class="note">{selected_icon}[写作逻辑]:{overall_assessment["paper_structure"]}</p>'
    else:
        paper_structure = ""

    if api_comments_flag and "conclusions" in overall_assessment:
        paper_conclusions = f'<p class="note">{selected_icon}[整体评价]:{overall_assessment["conclusions"]}</p>'
    else:
        paper_conclusions = ""

    abstract_note = ''
    if api_comments_flag and "0" in section_summaries:
        abstract_note = f'<p class="note-paragraph">{selected_icon}[摘要概述]:{section_summaries["0"]}</p>'
    # 定义整个页面的HTML模板
    paper_html_template = f"""
    <html>
    <head>
        <script>
            window.MathJax = {{
                tex: {{
                    inlineMath: [['$', '$']]
                }},
                svg: {{
                    fontCache: 'global'
                }}
            }};
        </script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    </head>
    <style>
        body {{ font-family: "{font}", serif; }}
        h1 {{ font-size: 28px; font-weight: bold; text-align: center; margin-top: 20px; }}
        h2 {{ font-size: 26px; font-weight: bold; text-align: left; margin-top: 20px; }}
        h3 {{ font-size: 24px; font-weight: bold; text-align: left; margin-top: 20px; }}
        h4 {{ font-size: 22px; font-weight: bold; text-align: left; margin-top: 20px; }}
        h5 {{ font-size: 22px; font-weight: bold; text-align: left; margin-top: 20px; }}
        .abstract-title {{ font-size: 26px; font-weight: bold; text-align: center; margin-top: 10px; }}
        .keywords-title {{ font-size: 26px; font-weight: bold; text-align: left; margin-top: 10px; }}
        .paragraph, .keywords {{ font-size: 20px; text-align: justify; text-justify: inter-word; margin: 5px 0; text-indent: 2em; }}
        .authors, .institute {{ text-align: center; font-style: italic; font-size: 14px; }}
        .abstract-content {{ font-size: 20px; text-align: justify; text-justify: inter-word; margin: 5px 0; text-indent: 0em;  padding-left: 100px; padding-right: 100px; }}
        .note {{ font-size: 18px; font-weight: bold; text-align: left; margin-top: 20px; color: #967BB6;}} /* 设置注释文字颜色为淡紫色 */
        .note-paragraph {{ font-size: 18px; font-weight: bold; text-align: left; margin-top: 20px; color: #967BB6;}} /* 设置注释文字颜色为淡紫色 */
        /* 额外样式，用于可滚动内容 */
        .scrollable-section {{
            background-color: #DFF0D8; /* 护眼色 */
            height: 760px;
            overflow-y: scroll;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }}
    </style>
    <div class="scrollable-section">
        {self_introduction}
        <br>
        {paper_summary}
        {paper_research_topic}
        {paper_research_outcomes}
        {paper_methodology}
        {paper_innovations}
        {paper_dataset_description}
        {paper_structure}
        {paper_conclusions}
        <br>
        <h1>{title}</h1>
        <div class="authors">{authors}</div>
        <div class="institute">{institutes}</div>
        <p class="abstract-title">{abstract_title}</p>
        {abstract_note}
        <p class="abstract-content">{abstract}</p>
        <p class="keywords-title">{keywords_title}</p>
        <p class="keywords">{keywords}</p>
        {body_html}
    </div>
    </html>
    """
    # 使用Streamlit的components.html方法来渲染HTML模板
    components.html(paper_html_template, height=800, scrolling=True)
