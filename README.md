# KGQA

**基于知识图谱的金融数据问答系统**

**Knowledge Graph Question Answering with Chinese Financial data** from TuShare



运行实例：

![image-20211223193845972](https://raw.githubusercontent.com/hyqshr/MD_picgo/main/image-20211223193845972.png)



- Stored financial data as **knowledge graph** with ```neo4j```
- Extract question type & entity from user query  with ```Aho–Corasick```  algorithm
- Detect if query is random chat using ```fasttext```



## Step

run ```semantic_parser.py``` to build a AC automation trie tree

run ```classifier.py``` to build a fasttext classifier

run ```store_to_neo4j.py``` transform the data into ```neo4j```

run ```main.py```





## Overall workflow:

![image-20211223192547920](https://raw.githubusercontent.com/hyqshr/MD_picgo/main/image-20211223192547920.png)



## neo4j

You can download ```neo4j``` at  https://neo4j.com/download/

create a new DBMS in local, and then **Start** the server, so you can dump data into **KG** and visualize the data



![image-20211223195133657](https://raw.githubusercontent.com/hyqshr/MD_picgo/main/image-20211223195133657.png)

## AC自动机: Aho-Corasick



```
Input: text = "ahishers"    
       arr[] = {"he", "she", "hers", "his"}

Output:
   Word his appears from 1 to 3
   Word he appears from 4 to 5
   Word she appears from 3 to 5
   Word hers appears from 4 to 7
```

***RUNTIME: O(n + m + z)*** 

AC自动机的基础是Trie树。和Trie树不同的是，树中的每个结点除了有指向孩子的指针（或者说引用），还有一个fail指针，它表示输入的字符与当前结点的**所有孩子结点都不匹配时**(注意，不是和该结点本身不匹配)，自动机的状态应转移到的状态（或者说应该转移到的结点）。

