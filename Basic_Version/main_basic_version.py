import argparse
import json
import re
import random
import os


def startup():
    ''' 根据命令行参数启动 设置path和article两个可选的命令行参数

    @return: args, 包含题库JSON文件的路径与文章的名称(如有)
    '''
    default_json_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "data.json")
    parser = argparse.ArgumentParser(description='Crossword puzzle')
    parser.add_argument('--path', type=str, default=default_json_path,
        help='path of data JSON file')
    parser.add_argument('--article', type=str, default="random",
        help='name of article')
    args = parser.parse_args()

    return args


def read_article(args):
    ''' 读取相应的题库 解析JSON文件

    如果遇到以下错误则返回None:
        (1) 题库JSON文件路径不正确
        (2) JSON文件中的某个字典的某个key名称不正确
        (3) JSON文件中的某个字典的某个value的类型不正确
        (4) 给定article参数但是题库JSON文件中不存在这一篇文章

    @return: selected_article, 选择的1份文章; 或者 None
    '''
    # 载入JSON文件
    try:
        with open(args.path, 'r', encoding="utf-8") as file:
            questions = json.load(file)
    except:
        print("Error 404: Data JSON file {} NOT Found! ".format(args.path))
        return None
    
    if not isinstance(questions, list):
        return None
    
    # 判断JSON文件中的各个字典是否合法
    # # 正确的key和对应的value的类型
    keys_should_exist = ("title", "article", "hints")
    value_type_should_be = (str, str, list)
    # # 遍历字典列表的每一个元素
    for question in questions:
        for i in range(len(keys_should_exist)):
            # 如果key不存在
            if keys_should_exist[i] not in question:
                print("Error 202: The key '{}' NOT exist in a dict of the JSON file {}!".format(
                            keys_should_exist[i], 
                            args.path
                        )
                    )
                
                return None
            else:
                # 如果key存在但是对应的value的类型不正确
                # # 建议用isinstance，直接用type比较可能会有问题
                if not isinstance(question[keys_should_exist[i]], value_type_should_be[i]):
                    print("Error 2022: Type of '{}' is WRONG in a dict of the JSON file {}! It should be type {}.".format(
                            keys_should_exist[i],
                            args.path,
                            value_type_should_be[i]
                        )
                    )

                    return None # 注意缩进 缩进不正确会导致逻辑错误
    
    # 选择文章
    if args.article == "random":
        # 随机选择一篇文章 默认选项
        article_index = random.randint(0, len(questions)-1)
        selected_article = questions[article_index]
    else:
        # 选择符合要求的第一篇文章
        try:
            selected_article = [x for x in questions if x['title'] == args.article][0]
        except:
            # 如果没有找到符合要求的文章
            print("Error 808: Article {} NOT Found! ".format(args.article))
            return None          

    return selected_article


def get_input_and_replace(selected_article):
    ''' 获取用户输入并替换关键词

    @return: 替换后的文章
    '''
    # 获取用户输入，并替换文章中的占位符
    for i, hint in enumerate(selected_article['hints']):
        word = input(f"请输入一个{hint}: ")    
        selected_article['article'] = re.sub('<{}>'.format(i+1), word, selected_article['article'])

    return selected_article['article']


def main():
    print("Welcome to Crossword puzzle!")

    args = startup()
    selected_article = read_article(args=args)
    if selected_article:
        article_replaced = get_input_and_replace(selected_article=selected_article)
        print(article_replaced)


if __name__ == "__main__":
    main()

