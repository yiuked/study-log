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

* swagger 报错
```
### Unable to render this definition

The provided definition does not specify a valid version field.

Please indicate a valid Swagger or OpenAPI version field. Supported version fields are `swagger: "2.0"` and those that match `openapi: 3.0.n` (for example, `openapi: 3.0.0`).

把 doc.jso文件中的  `swagger:2.0` 改成 `"openapi":"3.0.0"` 则可