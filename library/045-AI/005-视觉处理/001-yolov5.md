
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