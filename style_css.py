import streamlit as st


def apple_style():
    # 苹果风格样式, 对st.text_area、st.code、st.button组件进行了样式的重调，增加边角圆润度和阴影效果，更改背景颜色。
    # 并去除st.text_area组件选中时显示红色边框效果
    style = """
        <style>
        /* Base styles for text area and code block */
        textarea {
            font-family: 'Georgia', serif !important;
            min-height: 55px !important;
        }
        .stTextArea [data-baseweb=textarea], .stTextArea [data-baseweb=base-input] {
            background-color: #f1f3f4;
            border: none !important;
            padding: 10px 15px;
            font-family: 'Georgia', sans-serif;
            font-size: 16px;
            outline: none !important;
        }

        /* Specific styles for text area and code block */
        .stTextArea [data-baseweb=textarea], .stCodeBlock {
            border-radius: 10px;  /* Rounded corners */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stCodeBlock* {
            background-color: #f1f3f4;
            padding: 10px 15px;
            font-family: 'Georgia', sans-serif !important;
            font-size: 16px;
        }

        /* Hover effect for input and code block */
        .stTextArea [data-baseweb=textarea]:hover, .stCodeBlock:hover {
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        .stButton>button, .stDownloadButton > button {
            background-color: #FFFFFF;  /* 白色背景 */
            color: #555555;  /* 深灰色字体 */
            border-radius: 15px;
            border: none;
            font-family: 'Helvetica Neue', sans-serif;  /* 使用苹果系统字体 */
            font-size: 16px;
            padding: 5px 15px;  /* 按钮的高度和宽度 */
            margin: 10px 0;
            box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s, box-shadow 0.3s;
            text-align: center;
            text-decoration: none;  /* 移除下划线 */
            display: inline-block;
            cursor: pointer;
        }
        .stButton>button:hover, .stDownloadButton > button:hover {
            background-color: #F0F0F0;  /* 浅灰色背景，悬停时略微变暗 */
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
            text-decoration: none;  /* 悬停时也移除下划线 */
        }
        .stButton>button:focus, .stButton>button:active, .stDownloadButton > button:focus, .stDownloadButton > button:active {
            color: #555555 !important;  /* 保持原始字体颜色 */
            box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.2);
        }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)
