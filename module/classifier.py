import fasttext
import jieba
from config import classifier_corpus_path, classifier_save_path


def train_classifier(input_file_path, model_save_path):
    """训练分类模型"""
    model = fasttext.train_supervised(input=input_file_path, epoch=10, lr=0.5, wordNgrams=3)

    for a in ['茅台的股东是谁', '它的概念是什么', '你好', '平安科技这个股票怎么样', '再见', 'hi', 'hello', '拜拜']:
        print(model.predict(' '.join(jieba.lcut(a))))

    model.save_model(model_save_path)


class Classifier:
    """分类器"""

    def __init__(self, model_load_path):
        self.model_load_path = model_load_path
        self.model = self.load_model()

    def load_model(self):
        """加载模型"""
        return fasttext.load_model(self.model_load_path)

    def predict(self, query):
        """预测 query"""
        query_intent = self.model.predict(' '.join(jieba.lcut(query)))
        # 预测 label 和概率
        return query_intent[0][0].replace('__label__', ''), query_intent[1][0]


if __name__ == '__main__':

    print('开始训练分类器...')

    train_classifier(classifier_corpus_path, classifier_save_path)

    print('分类器训练成功...')
