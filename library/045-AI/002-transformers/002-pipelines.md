
Pipelines是一种方便的工具，它将多个NLP任务（如文本分类、命名实体识别、问答等）组合成一个流水线。下面是Pipelines的一些用途：

1.  文本分类（Text Classification）：将文本分为不同的类别，如垃圾邮件分类、情感分析、主题分类等。
2.  命名实体识别（Named Entity Recognition）：识别文本中的实体，如人名、地名、组织机构名等。
3.  问答（Question Answering）：根据给定的问题和一段文本，回答问题。
4.  摘要（Summarization）：将一篇文章或段落压缩成一个简短的摘要。
5.  翻译（Translation）：将一种语言翻译成另一种语言。
6.  生成（Generation）：生成文本，如自然语言生成、音乐生成、图像生成等。

```python
from transformers import pipeline

# 创建pipeline对象
nlp_pipeline = pipeline(task_name, model=model_name, tokenizer=tokenizer_name)

# 处理文本
result = nlp_pipeline(input_text)
```

其中，`task_name`是要执行的任务名称，如文本分类（"text-classification"）、命名实体识别（"ner"）、问答（"question-answering"）等。`model_name`是用于执行该任务的模型名称，如BERT、GPT-2等。`tokenizer_name`是用于处理输入文本的分词器名称，如BERT分词器、GPT-2分词器等。`input_text`是要处理的输入文本。
```python
class TaskNames(Enum):
    FEATURE_EXTRACTOR = "feature-extraction"
    MASKED_LANGUAGE_MODELING = "masked-lm"
    MULTILINGUAL_MASKED_LANGUAGE_MODELING = "mlm"
    CAUSAL_LANGUAGE_MODELING = "text-generation"
    MULTILINGUAL_CAUSAL_LANGUAGE_MODELING = "mlm-generation"
    SENTIMENT_ANALYSIS = "text-classification"
    QUESTION_ANSWERING = "question-answering"
    TOKEN_CLASSIFICATION = "ner"
    FILL_MASK = "fill-mask"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"

```
使用示例
```python
from transformers import pipeline, TaskNames

nlp_pipeline = pipeline(TaskNames.TEXT_CLASSIFICATION, model="distilbert-base-uncased-finetuned-sst-2-english", tokenizer="distilbert-base-uncased")

result = nlp_pipeline("This is a positive text.")
print(result)
# 输出： [{'label': 'POSITIVE', 'score': 0.9980878233909607}]
```
或者直接输入字符串
```python
nlp_pipeline = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", tokenizer="distilbert-base-uncased")
```

执行`pipeline`方法后，返回的结果`result`是一个字典，包含了执行该任务后的结果。具体的结果结构取决于任务类型。例如，如果是文本分类任务，则结果字典可能包括`label`和`score`两个键，分别表示预测的标签和得分。

需要注意的是，在使用Pipelines之前，需要安装Transformers库并下载相关的预训练模型和分词器。


### pipeline函数返回的结果是什么

`pipeline`函数返回的结果是一个列表或字典，具体取决于所执行的任务类型。

例如，对于文本分类任务，返回的结果是一个字典列表，每个字典包含以下键：

-   `label`: 预测的标签；
-   `score`: 预测标签的概率得分。

示例如下：

```python
from transformers import pipeline  

classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", tokenizer="distilbert-base-uncased") 

result = classifier("This is a positive text.") print(result) # 输出: [{'label': 'POSITIVE', 'score': 0.9980878233909607}]
```

对于命名实体识别（NER）任务，返回的结果是一个字典列表，每个字典包含以下键：

-   `word`: 实体所在的词汇；
-   `score`: 实体的概率得分；
-   `entity`: 实体的类型。

示例如下：

```python
ner = pipeline("ner", model="dslim/bert-base-NER", tokenizer="dslim/bert-base-NER") 
result = ner("My name is John and I live in New York.") 
print(result) 
# 输出： [{'entity': 'I-PER', 'score': 0.9983103, 'word': 'John'}, {'entity': 'I-LOC', 'score': 0.99790996, 'word': 'New'}, {'entity': 'I-LOC', 'score': 0.9977463, 'word': 'York'}]
```

对于问答任务，返回的结果是一个字典，包含以下键：

-   `answer`: 回答的文本；
-   `score`: 回答的概率得分；
-   `start`: 回答在原始文本中的起始位置；
-   `end`: 回答在原始文本中的结束位置。

示例如下：

```python
qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased-distilled-squad")
result = qa(question="What is the capital of France?", context="Paris is the capital of France.")
print(result)
# 输出：{'answer': 'Paris', 'score': 0.9971824889183044, 'start': 0, 'end': 5}

```

需要注意的是，对于一些需要预测多个结果的任务（如命名实体识别），返回的结果是一个列表，每个列表项对应一个预测结果。


可以在Transformers官方文档中查阅pipeline函数的返回值类型和内容。具体来说，每种任务类型的pipeline函数都有一个单独的文档页面，其中包含了该函数的详细说明、参数列表和返回值类型。

此外，也可以在Transformers源代码中查看pipeline函数的实现，以了解其具体的返回结果。不过，由于Transformers的代码比较复杂，这种方式可能需要一些时间和经验。

以下是常见任务类型的pipeline函数的返回结果清单：

-   文本分类任务（`text-classification`）：字典列表，每个字典包含`label`和`score`键。
-   命名实体识别任务（`ner`）：字典列表，每个字典包含`word`、`score`和`entity`键。
-   问答任务（`question-answering`）：字典，包含`answer`、`score`、`start`和`end`键。
-   摘要任务（`summarization`）：字符串，表示摘要文本。
-   机器翻译任务（`translation`）：字符串，表示翻译文本。
-   填充词任务（`fill-mask`）：字典列表，每个字典包含`sequence`、`score`和`token`键。
-   文本生成任务（`text-generation`）：字符串，表示生成的文本。
-   语言建模任务（`masked-lm`、`mlm`、`mlm-generation`）：字典，包含`sequence`、`score`和`token`键。

需要注意的是，上述清单只列出了一些常见的任务类型和返回结果类型，不代表所有的情况。具体的返回结果类型和内容还需要根据具体的任务类型和模型进行确认。