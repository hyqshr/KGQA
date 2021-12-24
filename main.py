from module.classifier import Classifier
from module.semantic_parser import SemanticParser
from module.graph_matcher import GraphMatcher
from config import classifier_load_path, entity_searcher_load_path, chat_responses, question_types
from random import choice

# 加载分类器
classifier = Classifier(classifier_load_path)

# 加载语义解析器，预测问题类型和涉及的实体
semantic_parser = SemanticParser(entity_searcher_load_path, question_types)

# 加载图数据库查询
graph_matcher = GraphMatcher()


while True:
    query = input('用户: ')
    if query == 'stop':
        break
    else:
        # 预测 label 和概率
        query_intent_label, query_intent_prob = classifier.predict(query)

        # 闲聊
        if query_intent_prob > 0.9:
            response = choice(chat_responses[query_intent_label])
        # 知识问答
        else:
            semantics = semantic_parser.predict(query)
            # print(semantics)

            # 匹配到用户输入的实体才能继续，问题类型默认是 股东
            if semantics['ques_types'] and semantics['entities']:
                    response = graph_matcher.predict(semantics)
            else:
                response = choice(chat_responses['safe'])
        print(f'机器人: {response}')

        if query_intent_label == 'goodbye':
            break
