# Buildings（毕业论文）
Support PyTorch 1.0.0
## 一、网络介绍(理论知识)
详见Paper和笔记。
## 二、环境安装
### 1. 安装Anaconda
```
Anaconda3-5.1.0-Linux-x86_64.sh
```

## 二、目录结构

```
Buildings
├── c++ext
├── cocoapi
├── docs
├── data
├── fpn
├── images
├── models
├── models
├── tools
├── .gitignore
├── coco.py
├── config.py
├── data.py
├── data.py
├── explore.ipynb
├── explore.py
├── model.py
├── predict.py
├── train.sh
├── utils.py
```

## 三、数据准备
训练和验证数据集是MS COCO 2014.   
⾸先，数据集包含两类⽂件：   
* １.标注⽂件，位于annotations⽬录下，json格式；   
* ２．图像⽂件，jpg格式，例⼦如下： 
```
data
├── annotations
│   ├── captions_train2014.json
│   ├── captions_val2014.json
│   ├── instances_minival2014.json
│   ├── instances_train2014.json
│   ├── instances_val2014.json
│   ├── instances_valminusminival2014.json
│   ├── person_keypoints_train2014.json
│   └── person_keypoints_val2014.json
├── test2014
│   ├── COCO_test2014_000000000001.jpg
│   ├── COCO_test2014_000000000014.jpg
│   ├── COCO_test2014_000000000016.jpg
│   ├── COCO_test2014_000000581919.jpg
│   └── COCO_test2014_000000581923.jpg
├── train2014
│   ├──COCO_train2014_000000000009.jpg
│   ├──COCO_train2014_000000000049.jpg
│   ├──COCO_train2014_000000000061.jpg
│   ├──COCO_train2014_000000581909.jpg
│   └──COCO_train2014_000000581921.jpg
│── val2014
│   ├── COCO_val2014_000000000042.jpg
│   ├── COCO_val2014_000000000139.jpg
│   ├── COCO_val2014_000000000143.jpg
│   ├── COCO_val2014_000000581913.jpg
│   ├── COCO_val2014_000000581929.jpg
```

## 四、代码准备
### 1、代码阅读
* coco.py
    * [argparse的用法](notes/argparse.md)
    * [10分钟教程掌握Python调试器pdb](notes/pdb.md)