## Swagger
* 类似于`question_id[2166]=C&question_id[2167]=B&question_id[2168]=C&question_id[2169]=A&question_id[2170]=D`的数组参数如何表示？
```
  - name: "question_id"
    in: "formData"
    description: "提交的答案"
    required: true
    type: "array"
    items:
      type: "string"
```
