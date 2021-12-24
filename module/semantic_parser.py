from config import entity_corpus_path, entity_searcher_save_path, contexts
import ahocorasick
import pandas as pd
import os
import pickle


def build_search_tree(input_folder_path, tree_save_path):
    """读取股票名称，股东和概念实体，构建 ac 树"""
    # https://pypi.org/project/pyahocorasick/
    tree = ahocorasick.Automaton()

    stock_basic = pd.read_csv(os.path.join(input_folder_path, '股票信息.csv'), encoding='gbk')
    for idx, each_row in stock_basic.iterrows():
        # (key, value = (实体名字，实体类型))
        tree.add_word(each_row['name'], (each_row['name'], '股票'))

    concept = pd.read_csv(os.path.join(input_folder_path, '概念信息.csv'), encoding='gbk')
    for idx, each_row in concept.iterrows():
        # (key, value = (实体名字，实体类型))
        tree.add_word(each_row['name'], (each_row['name'], '概念'))

    holder = pd.read_csv(os.path.join(input_folder_path, '股东信息.csv'), encoding='gbk')
    for idx, each_row in holder.iterrows():
        # (key, value = (实体名字，实体类型))
        tree.add_word(each_row['股东名称'], (each_row['股东名称'], '股东'))

    tree.make_automaton()

    with open(tree_save_path, 'wb') as fout:
        pickle.dump(tree, fout)


class SemanticParser:
    """实体搜索器"""

    def __init__(self, entity_model_load_path, question_types):
        self.entity_model_load_path = entity_model_load_path
        self.entity_model = self.load_model()
        self.question_types = question_types

    def load_model(self):
        """加载模型"""
        with open(self.entity_model_load_path, 'rb') as fin:
            return pickle.load(fin)

    def predict_question_types(self, query):
        """判断问题类型，这里只是通过关键词去判断，可以改成分类模型"""

        rtn_ques_types = []
        for ques_type, kws in self.question_types.items():
            for each_kw in kws:
                if each_kw in query:
                    rtn_ques_types.append(ques_type)
                    break
        return rtn_ques_types

    def predict(self, query):
        """预测 query"""

        rtn = {}

        # 预测类型
        ques_types = self.predict_question_types(query)

        # 预测实体
        entities = {}
        for end_index, (entity_name, entity_type) in self.entity_model.iter(query):
            entities[entity_name] = entity_type

        #如果预测类型和预测实体都找到，那么备份问题以便继承
        if len(ques_types) != 0 and len(entities) != 0:
            rtn['ques_types'] = ques_types
            rtn['entities'] = entities
            # 备份
            contexts['ques_types'] = ques_types
            contexts['entities'] = entities
        elif len(ques_types) != 0:
            rtn['ques_types'] = ques_types
            # 备份
            contexts['ques_types'] = ques_types

            # 从对话历史中继承问题类型
            rtn['entities'] = contexts['entities']
        elif len(entities) != 0:
            # 从对话历史中继承问题类型
            rtn['ques_types'] = contexts['ques_types']

            rtn['entities'] = entities
            contexts['entities'] = entities

        # 如果两个都没有找到，那说明是没有涉及 KG
        else:
            rtn['ques_types'] = []
            rtn['entities'] = {}

        return rtn


if __name__ == '__main__':

    print('开始训练实体搜索树...')

    build_search_tree(entity_corpus_path, entity_searcher_save_path)

    print('实体搜索树训练成功...')