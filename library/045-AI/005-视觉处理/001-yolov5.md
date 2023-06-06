
### 训练结果解析
```
Epoch    GPU_mem   box_loss   obj_loss   cls_loss  Instances       Size
78/99     0G     0.0313    0.03745   0.004692        123            640

 Class     Images  Instances          P          R      mAP50   mAP50-95:
 all        128        929      0.938       0.89      0.957      0.742
```
>- Epoch:训练轮数,此处显示为68/99,表示已经训练68轮,总轮数设置为99轮。
>- GPU_mem:GPU显存占用情况,此处显示为0G,表示显存占用很低。如果显存不足会显示为2G/11G等。
>- box_loss:边界框回归loss,此处为0.03343,表示边界框预测的loss值。
>- obj_loss:对象ness loss,此处为0.03745,表示是否包含对象的loss值。
>- cls_loss:分类loss,此处为0.005675,表示对象分类预测的loss值。
>- Instances:训练图片中的目标实例数,此处为182,表示一共182个实例。
>- Size:图片大小,此处为640,表示使用640x640的图片进行训练。
>- Class: 类别,此处显示为all,代表总体指标。
>- Images:测试集图片数,此处显示为128,表示一共128张测试集图片。
>- Instances:测试集目标实例数,此处显示为929,表示一共929个测试集实例。 
>- P:Precision,精度,此处显示为0.918,表示模型在测试集上的预测精度为91.8%。
>- R:Recall,召回率,此处显示为0.9,表示模型在测试集上的召回率为90%。
>- mAP50:mAP@IoU=0.5, 此处显示为0.95,表示模型在IoU=0.5时的mAP为95%。  
>- mAP50-95: mAP@IoU=0.5:0.95,此处显示为0.718,表示模型在IoU=0.5:0.95范围内的mAP为71.8%。

```
Exception ignored in tp_clear of: <class 'memoryview'> Traceback (most recent call last): File "F:\scoop\apps\miniconda3\current\envs\main\lib\concurrent\futures\process.py", line 697, in submit w = _WorkItem(f, fn, args, kwargs) BufferError: memoryview has 1 exported buffer
```

在std.py 530行打个断点，就可以过了？


#### yolo v5 导出 Android 手机上可以运行的 TFLite 模型
https://www.sunzhongwei.com/yolo-v5-export-tflite-model-run-on-android


查看CUDA版本
```
nvidia-smi
```

nvcc --version和nvidia-smi的版本可能會不一樣，前者是runtime api對應的版本，後者是driver api的版本。

通常需要和runtime的版本匹配，driver的版本可以向下兼容。

CUDA-toolkit
https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html
https://www.codenong.com/cs106685050/
https://developer.nvidia.com/cuda-toolkit-archive

cuDNN
https://developer.nvidia.com/rdp/cudnn-archive#a-collapse51b


OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
```

UserWarning: Failed to load image Python extension: [WinError 127] 找不到指定的程序。
  warn(f"Failed to load image Python extension: {e}")
  
