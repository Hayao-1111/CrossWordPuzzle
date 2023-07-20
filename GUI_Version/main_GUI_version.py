import streamlit as st
import json
import random
import re
import os


# 配置页面标题、icon、菜单栏等
st.set_page_config(
    page_title="Crossword Puzzle", 
    page_icon=os.path.join(os.path.split(os.path.realpath(__file__))[0], "images/game_icon.png"),
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Hayao-1111/CrossWordPuzzle',
        'Report a bug': "https://github.com/Hayao-1111/CrossWordPuzzle/issues",
        'About': '''
**Crossword Puzzle :red[GUI Version]**  v1.0   
**Author**: Hayao-1111  
**email**: sunxl18@foxmail.com
'''
    }
)


def get_JSON_file(use_uploaded_json:bool):
    ''' 获取JSON数据文件 '''

    # 如果用户上传文件
    if use_uploaded_json:
        uploaded_file = st.file_uploader("请选择上传的文件: ", 
                                         accept_multiple_files=False, 
                                         type=['json']
                                        )
        # 用户完成文件上传后 解析并检查JSON数据文件
        if uploaded_file:
            try:
                questions = json.loads(uploaded_file.getvalue().decode("utf-8"))
            except json.JSONDecodeError:
                st.warning("JSON文件解析错误！请检查JSON文件格式是否正确")
                return None
            except UnicodeDecodeError:
                st.warning("JSON文件解码错误！文件应当为UTF-8编码！")
                return None
            if checkJSONValidity(questions):
                return questions
    # 使用默认JSON数据文件
    else:
        default_json = os.path.join(os.path.split(os.path.realpath(__file__))[0], "data/data.json")
        with open(default_json, 'r', encoding="utf-8") as file:
            questions = json.load(file)
        if checkJSONValidity(questions):
            return questions    


def checkJSONValidity(articles):
    ''' 检测JSON文件格式是否正确 '''

    if not isinstance(articles, list):
        st.warning("JSON文件应可转化为字典列表！")
        return False
    for article in articles:
        if not isinstance(article, dict):
            st.warning("JSON文件列表中每个元素应为字典！")
            return False
        if "hints" not in article:
            st.warning("JSON文件中的每篇文章字典中应包含hints键！")
            return False
        if "title" not in article:
            st.warning("JSON文件中的每篇文章字典中应包含title键！")
            return False
        if "article" not in article:
            st.warning("JSON文件中的每篇文章字典中应包含article键！")
            return False
        if not isinstance(article["hints"], list):
            st.warning("JSON文件中的每篇文章字典中的hints键对应的值应为列表！")
            return False
    return True
        

def read_article(questions: list, article_name: str):
    ''' 读取相应的题库 解析JSON文件
    '''
    
    # 选择文章
    index_of_article = 0   # 文章在题库中的索引 便于编号输入框的key

    # 随机选择文章
    if article_name == "random":
        # 随机选择一篇文章 
        # NOTE v1.0 版本暂时删去此选项
        article_index = random.randint(0, len(questions)-1)
        selected_article = questions[article_index]
    # 选择指定的文章 选择符合要求的第一篇文章
    else:
        article_list = [x["title"] for x in questions]  # 获取文章名称
        try:
            # 找到列表中所有文章名等于指定文章名的字典元素 并选择第一个
            selected_article = [x for x in questions if x['title'] == article_name][0]
            # 找到指定文章在列表中的位置索引
            index_of_article = article_list.index(article_name)
        except:
            # 如果没有找到符合要求的文章
            st.warning("Error 808: Article {} NOT Found! ".format(article_name))
            return None          

    return (selected_article, len(selected_article["hints"]), index_of_article)


def get_input_and_replace(questions, question_option):
    ''' 获取用户输入并生成替换后的文字
    '''
    selected_article, length, index_of_article = read_article(
        questions, 
        question_option
    )

    is_all_submitted = True     # 记录是否所有输入框都有输入

    # 建立表单 以防止单独建立多个text_input时的刷新"过快"
    with st.sidebar.form(key="user_input"):
        for i in range(length):
            word = st.text_input(
                "请输入一个" + selected_article["hints"][i], 
                key="key{}_{}".format(index_of_article, i)  
                # NOTE 每篇文章的每个hint都有不同的key 
                #   使得每次重新选择文章后下面的输入框的内容为空  
            )
            selected_article['article'] = re.sub(
                '<{}>'.format(i+1), 
                ":red[{}]".format(word),    # 重点标红
                selected_article['article']
            )

            # 仅当所有输入框都有用户输入时 is_all_submitted变为True
            is_all_submitted = is_all_submitted and word

        # 表单需配备的提交按钮
        submit_button = st.form_submit_button(label='查看生成的文字')

    # 点击提交按钮后 才执行下列的命令
    if submit_button:
        if is_all_submitted:
            st.write(selected_article["article"])
            st.write("---")
            
            # 建立一个rerun按钮 点击后重新运行
            # NOTE 有待改进
            re_run_button = st.button("再来一次")

            if re_run_button:
                st.experimental_rerun()
                # st.caching.clear_cache()
                # raise st.script_runner.StopException



def main():
    ''' 主函数 v1.0

    @Author: Hayao-1111
    @Date: 2023-07-20
    @Description: GUI Version of Crossword Puzzle ...
    '''
    # 标题
    st.title("文章填词")
    # st.write("---")
    st.write("欢迎来到**文章填词**游戏！请转到左侧边栏开始游戏~")
    st.write("---")

    # 侧边栏
    st.sidebar.header("1. 选择 JSON")
    st.sidebar.write("**勾选**下面的选项以自行上传文件，否则使用默认JSON文件:")
    use_uploaded_json = st.sidebar.checkbox("自行上传JSON文件")

    st.sidebar.write("---")

    # 读取JSON题库数据文件
    questions = get_JSON_file(use_uploaded_json)

    # 读取文件后，再进行下列操作
    if questions:
        # 确定article列表
        article_list = [x["title"] for x in questions]

        # 选择article
        st.sidebar.header("2. 选择 Article")
        question_option = st.sidebar.selectbox(
            "选择 Article",
            label_visibility="hidden",
            options=[""] + article_list
        )

        st.sidebar.write("---")

        # 用户选择article后，再进行下列操作
        if question_option != "":
            get_input_and_replace(questions, question_option)

    with st.expander("Let's have a rest~"):
        st.image("https://images.unsplash.com/photo-1462332420958-a05d1e002413?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2107&q=80"
                , caption="Nebula, from usplash, see: https://unsplash.com/photos/-hI5dX2ObAs"
                )
        st.image("https://images.unsplash.com/photo-1534447677768-be436bb09401?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1494&q=80"
                , caption="Black sailing boat, from usplash, see: https://unsplash.com/photos/DKix6Un55mw"
                )
        st.image("https://images.unsplash.com/photo-1531366936337-7c912a4589a7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
                , caption="Northern lights over snow-capped mountian, from usplash, see: https://unsplash.com/photos/LtnPejWDSAY"
                )



if __name__ == "__main__":
    main()
