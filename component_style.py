import streamlit as st


def component_style():
    # 按照苹果风格样式, 对st.text_area、st.code、st.button、st.text_input、st.chat_input组件进行了样式的重调，增加边角圆润度和阴影效果，更改背景颜色。
    # 去除组件选中时显示红色边框效果
    style = """
    <style>
        /* 改变聊天框chat_input组件样式 */
        [data-testid="stChatInput"] {
            background-color: #f1f3f4; /* 浅灰色背景 */
            border: none !important; /* 移除边框 */
            padding: 10px 15px; /* 调整内边距 */
            font-family: 'Times New Roman', sans-serif; /* 更改字体 */
            font-size: 16px; /* 设置字体大小 */
            outline: none !important; /* 移除聚焦时的轮廓 */
            border-radius: 10px; /* 圆角边框 */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影 */
            transition: box-shadow 0.3s, background-color 0.3s; /* 过渡动画 */
        }
        
        /* 聊天框chat_input悬停效果 */
        [data-testid="stChatInput"]:hover {
            background-color: #F0F0F0;  /* 浅灰色背景，悬停时略微变暗 */
            box-shadow: 0 8px 10px rgba(0, 0, 0, 0.15);
        }

        /* 去掉text_input选中的边框 */
        div[data-baseweb="input"] {
            background-color: #f1f3f4;
            border: none !important;
            padding: 0px 0px;
            font-family: 'Times New Roman', sans-serif;
            font-size: 16px;
            outline: none !important;
        }
        
        /* 定义文本输入框的样式 */
        [data-testid="textInputRootElement"] input {
            background-color: #f1f3f4; /* 浅灰色背景 */
            border: none !important; /* 移除边框 */
            padding: 10px 15px; /* 调整内边距 */
            font-family: 'Times New Roman', sans-serif; /* 更改字体 */
            font-size: 16px; /* 设置字体大小 */
            outline: none !important; /* 移除聚焦时的轮廓 */
            border-radius: 10px; /* 圆角边框 */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影 */
            transition: box-shadow 0.3s, background-color 0.3s; /* 过渡动画 */
        }
        
        /* text_input悬停效果 */
        [data-testid="textInputRootElement"] input:hover {
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }

        div[data-baseweb="textarea"] {
            background-color: #f1f3f4;
            border: none !important;
            padding: 0px 0px;
            font-family: 'Times New Roman', sans-serif;
            font-size: 16px;
            outline: none !important;
        }

        /* Base styles for text area and code block */
        textarea {
            font-family: 'Times New Roman', serif !important;
            min-height: 55px !important;
        }
        .stTextArea [data-baseweb=textarea], .stTextArea [data-baseweb=base-input] {
            background-color: #f1f3f4;
            border: none !important;
            padding: 10px 15px;
            font-family: 'Times New Roman', sans-serif;
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
            font-family: 'Times New Roman', sans-serif !important;
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
            font-family: 'Times New Roman', sans-serif;  /* 使用苹果系统字体 */
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
