from py2neo import Graph


class GraphMatcher:
    """基于 cypher 语句查询数据库"""

    def __init__(self):
        self.graph = Graph('http://localhost:7474/finance_demo/db/', auth=('neo4j', 'neo4j123'))

    def parse_graph(self, ques_types, entities):
        """转换成 cypher 语句查询"""

        response = ""
        for each_ques_type in ques_types:
            if each_ques_type == 'concept':
                for entity_name, entity_type in entities.items():
                    if entity_type == '股票':
                        cypher_sql = f'MATCH (s:{entity_type})-[r:所属概念]->(c:概念) where s.股票名称 = "{entity_name}" return c.概念名称'
                        rtn = self.graph.run(cypher_sql).data()
                        response += f'{entity_name}所属概念是{rtn[0]["c.概念名称"]}' + '\n'
            elif each_ques_type == 'holder':
                for entity_name, entity_type in entities.items():
                    if entity_type == '股票':
                        cypher_sql = f'MATCH (h:股东)-[r:持有]->(s:{entity_type}) where s.股票名称 = "{entity_name}" return h.股东名称, r.hold_amount, r.hold_ratio'
                        rtn = self.graph.run(cypher_sql).data()
                        response += f'股东：{rtn[0]["h.股东名称"]}，持有{entity_name}{rtn[0]["r.hold_amount"]}，占比{rtn[0]["r.hold_ratio"]}' + '\n'
            elif each_ques_type == 'industry':
                for entity_name, entity_type in entities.items():
                    if entity_type == '股票':
                        cypher_sql = f'MATCH (s:{entity_type}) where s.股票名称 = "{entity_name}" return s.行业'
                        rtn = self.graph.run(cypher_sql).data()
                        response += f'{entity_name}的行业是{rtn[0]["s.行业"]}' + '\n'
        return response.strip()

    def predict(self, semantics):
        """预测 query"""
        response = self.parse_graph(semantics['ques_types'], semantics['entities'])
        return response
