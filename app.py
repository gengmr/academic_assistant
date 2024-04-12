import streamlit as st
from init import init
from st_on_hover_tabs import on_hover_tabs
from page import home_page, paper_entry_page, upload, analysis, display


def main():
    # 初始化
    init()
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['主页', '导入', '编辑', '分析', '查看'],
                             iconName=['home', 'upload', 'edit', 'person', 'article'], default_choice=0)
    if tabs == '主页':
        home_page()
    elif tabs == '导入':
        upload()
    elif tabs == '编辑':
        paper_entry_page()
    elif tabs == '分析':
        analysis()
    elif tabs == '查看':
        display()


if __name__ == '__main__':
    main()