embedded 将结构展开
```
MenuMeta  `json:"meta" gorm:"embedded;comment:附加属性"` // 附加属性
```

在 GORM 中，`ForeignKey` 和 `AssociationForeignKey` 是用于关联关系的字段，具体区别如下：

-   `ForeignKey`：定义了当前 Model 的外键，用于表明关联关系的“主键”。
-   `AssociationForeignKey`：定义了关联 Model 的外键，用于表明关联关系的“外键”。

例如，一个 `User` 模型和一个 `Article` 模型，它们之间的关系是一个 User 对应多个 Article。这时，`User` 模型中的 `id` 就是 `Article` 模型中的 `user_id` 的 `ForeignKey`，而 `Article` 模型中的 `id` 就是 `User` 模型中的 `id` 的 `AssociationForeignKey`。