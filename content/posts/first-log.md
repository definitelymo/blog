---
title: "internimage"
date: 2025-07-16T20:00:00+08:00
draft: false
---

# 版本兼容问题使用CUDA11.8

## PyTorch 版本
PyTorch 版本过新似乎会导致许多问题，很多库并不兼容 2.1.0，现在改成 2.0.1。
## 不能导入前馈网络
cannot import name 'FEEDFORWARD_NETWORK' from 'mmcv.cnn.bricks.transformer
effcient——ffn中修改import处去掉前馈网络，增加registry的导入作为注册表，将basemodule导入改成from mmengine.model.base_module import BaseModule
## mmcv.runner完全消失
from mmcv.runner import force_fp32
ModuleNotFoundError: No module named 'mmcv.runner'
改成from mmengine.model.utils import force_fp32
# 使用11.3版本的CUDA
## 核心库版本如下：  
- mmcv-full==1.5.0 
- mmsegmentation==0.27.0 
- timm==0.6.11 
- mmdet==2.28.1 
- numpy==1.26.4 
- pydantic==1.10.13
- yapf==0.40.1
  
`pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113  -f https://download.pytorch.org/whl/torch_stable.html `
[官方仓库连接](https://github.com/OpenGVLab/InternImage)
## 库报错
### linux版本冲突
如Scipy等库不同版本对linux依赖不同，使用conda安装即可解决
### opencv
cv2.error: OpenCV(4.7.0) :-1: error: (-5:Bad argument) in function 'imdecode'
Overload resolution failed:buf is not a numpy array, neither a scalar

尝试cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)修改为img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)，失败
怀疑是地址重复将dataroot删掉，img_prefix=data_root + 'val2017/',修改data_root为绝对路径


导入自定义的导入文件，将pipeline里的load文件修改前面加上My
问题似乎聚焦在新老版本的数据读取方式上，意思配置文件比较新但整体框架是老的，有许多冲突  现在尝试转换读取方式绕过opencv


自己写的存在数组转换问题，要先转换成浮点保持精度
TTA的存在让自己写的转换函数只运行一次，报错会一直存在，要改变TTA结构


使用AI大概改了20多次pipeline文件，过程全部省略，一直反复出现assertion error，然后AI崩溃放弃了。。。。  他希望从头再来，直接改图片本身，我的评价是他是这个
numpy版本不止一个，疑似openmim安装的 全部卸载后重新安装并且重装openmim等来保证链接
opencv的读取不到疑似是opencv版本的问题 

程序在运行train.py的时候卡住了，没有报任何错，在输出初始配置的日志之后就没有输出任何训练日志，尝试用断点寻找原因，进入了六层函数还是没到头  
最后发现是数据集的配置文件错误导致始终在读取而无法进行正确训练，包括annotation以及cofnig里的lass
## 数据集
### YOLO类转COCO类
AI写了个脚本，注意一下文件结构，要注意annotaion的具体配置