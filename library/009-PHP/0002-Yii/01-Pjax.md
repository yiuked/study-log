1. `Pjax::begin()`
```php
// eg.1
\yii\widgets\Pjax::begin(['options' => ['id' => 'pjax-container']);
// eg.2
\yii\widgets\Pjax::begin(['options' => ['id' => 'pjax-container'], 'linkSelector' => '[pjax!=false]']);
```
eg.1中，表示所有包含在选择器`#pjax-container`中的`a`标签对象都会调用`pjax`.  
eg.2中，表示所有包含在选择器`#pjax-container`中的`a`标签对象中，除了`pjax`属性不为`false`的对象都会调用`pjax`.  
