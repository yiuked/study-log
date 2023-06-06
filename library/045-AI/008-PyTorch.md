### 学习文档
https://pytorch123.com/SecondSection/autograd_automatic_differentiation/

### 安装
https://pytorch.org/get-started/locally/

### 版本检测
```
import torch
torch.__version__
```

### 张量
```
import torch

# 创建张量
torch.empty(5,3)
torch.rand(5,3)
torch.zeros(5, 3, dtype=torch.long)
x = 
torch.tensor([5.5, 3])

# 输出张量维度
print(x.size())

# 运算
y = torch.rand(5, 3)
print(x+y)
print(torch.add(x, y))
print(y.add_(x))
```
>tensor.view() 操作改变的仅是tensor的形状(shape),而不改变其数据大小(size)。tensor的size代表其所包含的总元素数量,与shape无关。而shape则决定这些元素如何排布,以形成我们所熟知的矩阵、三维数组等结构。

### autograd
autograd 包是 PyTorch 中所有神经网络的核心。首先让我们简要地介绍它，然后我们将会去训练我们的第一个神经网络。该 autograd 软件包为 Tensors 上的所有操作提供自动微分。它是一个由运行定义的框架，这意味着以代码运行方式定义你的后向传播，并且每次迭代都可以不同。我们从 tensor 和 gradients 来举一些例子。


```
# 报这个错
AttributeError: module 'distutils' has no attribute 'version'
setuptools==59.5.0

# Inplace update to inference tensor outside InferenceMode is not allowed.
torch==1.13.1
torchversion==0.14.1
```