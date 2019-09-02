# Buildings（毕业论文）
Support PyTorch 1.0.0～1.1.0   
参考：https://github.com/delldu/MaskRCNN   
## 一、网络介绍(理论知识)
* [MaskRCNN笔记_TensorFlow](https://github.com/fusimeng/MaskRCNN)   
## 二、运行环境
### 1.docker镜像
fusimeng/building:18.04-10.0-7.4-3.6-pmth-xrdp
```
root@60f4672b0559:/examples# pip list
Package                      Version            
---------------------------- -------------------
absl-py                      0.7.1              
asn1crypto                   0.24.0             
astor                        0.8.0              
attrs                        19.1.0             
backcall                     0.1.0              
bleach                       3.1.0              
catfish                      1.4.4              
certifi                      2019.6.16          
cffi                         1.12.3             
chardet                      3.0.4              
cloudpickle                  1.2.1              
cryptography                 2.1.4              
cupshelpers                  1.0                
cycler                       0.10.0             
Cython                       0.29.13            
decorator                    4.4.0              
defer                        1.0.6              
defusedxml                   0.6.0              
distro-info                  0.18ubuntu0.18.04.1
entrypoints                  0.3                
future                       0.17.1             
gast                         0.2.2              
google-pasta                 0.1.7              
graphviz                     0.8.4              
grpcio                       1.21.1             
h5py                         2.9.0              
horovod                      0.16.4             
httplib2                     0.9.2              
idna                         2.8                
ipykernel                    5.1.1              
ipython                      7.6.1              
ipython-genutils             0.2.0              
ipywidgets                   7.5.0              
jedi                         0.14.1             
Jinja2                       2.10.1             
joblib                       0.13.2             
json5                        0.8.5              
jsonschema                   3.0.1              
jupyter                      1.0.0              
jupyter-client               5.3.1              
jupyter-console              6.0.0              
jupyter-core                 4.5.0              
jupyterlab                   1.0.2              
jupyterlab-server            1.0.0              
Keras                        2.2.4              
Keras-Applications           1.0.8              
Keras-Preprocessing          1.1.0              
keyring                      10.6.0             
keyrings.alt                 3.0                
kiwisolver                   1.1.0              
language-selector            0.1                
launchpadlib                 1.10.6             
lazr.restfulclient           0.13.5             
lazr.uri                     1.0.3              
lightdm-gtk-greeter-settings 1.2.2              
macaroonbakery               1.1.3              
Markdown                     3.1.1              
MarkupSafe                   1.1.1              
matplotlib                   3.1.1              
menulibre                    2.2.0              
mistune                      0.8.4              
mugshot                      0.4.0              
mxnet-cu100                  1.4.1              
nbconvert                    5.5.0              
nbformat                     4.4.0              
notebook                     6.0.0              
numpy                        1.14.6             
oauth                        1.0.1              
olefile                      0.45.1             
onboard                      1.4.1              
opencv-contrib-python        4.1.0.25           
opencv-python                4.1.0.25           
pandas                       0.25.0             
pandocfilters                1.4.2              
parso                        0.5.1              
pexpect                      4.7.0              
pickleshare                  0.7.5              
Pillow                       6.0.0              
pip                          19.1.1             
prometheus-client            0.7.1              
prompt-toolkit               2.0.9              
protobuf                     3.8.0              
psutil                       5.6.3              
ptyprocess                   0.6.0              
pycairo                      1.16.2             
pycparser                    2.19               
pycrypto                     2.6.1              
pycups                       1.9.73             
pycurl                       7.43.0.1           
Pygments                     2.4.2              
pygobject                    3.26.1             
pymacaroons                  0.13.0             
PyNaCl                       1.1.2              
pyparsing                    2.4.1              
pyRFC3339                    1.0                
pyrsistent                   0.15.3             
python-apt                   1.6.4              
python-dateutil              2.8.0              
python-debian                0.1.32             
python-debianbts             2.7.2              
python-magic                 0.4.16             
pytz                         2019.1             
pyxdg                        0.25               
PyYAML                       5.1.1              
pyzmq                        18.0.2             
qtconsole                    4.5.1              
reportlab                    3.4.0              
requests                     2.22.0             
requests-unixsocket          0.1.5              
scikit-learn                 0.21.2             
scipy                        1.1.0              
SecretStorage                2.3.1              
Send2Trash                   1.5.0              
setuptools                   41.0.1             
sgt-launcher                 0.2.4              
simplejson                   3.13.2             
six                          1.12.0             
sklearn                      0.0                
system-service               0.3                
systemd-python               234                
tensorboard                  1.14.0             
tensorboardX                 1.8                
tensorflow-estimator         1.14.0             
tensorflow-gpu               1.14.0             
termcolor                    1.1.0              
terminado                    0.8.2              
testpath                     0.4.2              
torch                        1.1.0              
torchvision                  0.3.0              
tornado                      6.0.3              
traitlets                    4.3.2              
typing                       3.7.4              
ubuntu-drivers-common        0.0.0              
urllib3                      1.25.3             
wadllib                      1.3.2              
wcwidth                      0.1.7              
webencodings                 0.5.1              
Werkzeug                     0.15.4             
wheel                        0.33.4             
widgetsnbextension           3.5.0              
wrapt                        1.11.2             
xcffib                       0.5.1              
xkit                         0.0.0              
zope.interface               4.3.2       
```
## 三、目录结构
```
Buildings
├──mrcnn
│    ├── c++ext     # MaskRCNN的NMS等函数库
│    ├── cocoapi    # COCOAPI
│    ├── data       # 数据集，COOC2014 & IAILD
│    │   ├── annotations
│    │   │    ├── captions_train2014.json
│    │   │    ├── captions_val2014.json
│    │   │    ├── instances_minival2014.json
│    │   │    ├── instances_train2014.json
│    │   │    ├── instances_val2014.json
│    │   │    ├── instances_valminusminival2014.json
│    │   │    ├── person_keypoints_train2014.json
│    │   │    └── person_keypoints_val2014.json
│    │   ├── test2014
│    │   │    ├── COCO_test2014_000000000001.jpg
│    │   │    ├── COCO_test2014_000000000014.jpg
│    │   │    ├── COCO_test2014_000000000016.jpg
│    │   │    ├── COCO_test2014_000000581919.jpg
│    │   │    └── COCO_test2014_000000581923.jpg
│    │   ├── train2014
│    │   │    ├──COCO_train2014_000000000009.jpg
│    │   │    ├──COCO_train2014_000000000049.jpg
│    │   │    ├──COCO_train2014_000000000061.jpg
│    │   │    ├──COCO_train2014_000000581909.jpg
│    │   │    └──COCO_train2014_000000581921.jpg
│    │   └──val2014
│    │        ├── COCO_val2014_000000000042.jpg
│    │        ├── COCO_val2014_000000000139.jpg
│    │        ├── COCO_val2014_000000000143.jpg
│    │        ├── COCO_val2014_000000581913.jpg
│    │        └── COCO_val2014_000000581929.jpg
│    ├── fpn        # FPN学习内容，程序中未使用
│    ├── images     # 测试图片
│    ├── models     # 推理时模型存放位置
│    ├── tools      # 工具包
│    ├── .gitignore # 提交时忽略内容
│    ├── coco.py    # coco数据集的训练和测试内容
│    ├── config.py  # 配置文件
│    ├── data.py    # COCO数据读取
│    ├── explore.ipynb  # MaskRCNN结构学习
│    ├── explore.py     # MaskRCNN结构学习
│    ├── model.py       # MaskRCNN模型
│    ├── predict.py     # 预测/推理
│    ├── train.sh       # 训练脚本
│    ├── eval.sh        # 验证脚本
│    └── utils.py       # 工具
├──notes
     ├── argparse.md
     ├── pdb.md
```
## 四、数据准备
### 1、COCO数据集
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
### 2、IAILD
法国国家信息与自动化研究所提供的[Inria Aerial Image Labeling Dataset](https://project.inria.fr/aerialimagelabeling/)。    


## 五、代码阅读
* [argparse的用法](notes/argparse.md)
* [10分钟教程掌握Python调试器pdb](notes/pdb.md)
* [编译封装包](https://github.com/fusimeng/Python/blob/master/notes/pip_myself.md)
## 六、代码运行
### 1、下载代码和数据
#### 下载代码：   
```
git clone https://github.com/fusimeng/Buildings
```
#### 下载数据集：   
百度云：链接:https://pan.baidu.com/s/1VZjF_aOOIhnHhJMxVbevzw  密码:aduo   
下载后放到相应位置，位置可参考目录结构。

#### 下载训练好的模型：   
百度云：链接:https://pan.baidu.com/s/1LgUFW41jzjVXlsnJKtu5_g  密码:lwm5  
下载后放到相应位置，位置可参考目录结构。 
### 2、编译
* 编译c++ext：   
```
~# cd Buildings/mrcnn/c++ext 
mrcnn/c++ext# make

mrcnn/c++ext# pip list | grep maskrcnn
maskrcnn                     0.1   
```
* 编译COCOAPI：
```   
~# cd Buildings/mrcnn/cocoapi/PythonAPI
Buildings/mrcnn/cocoapi/PythonAPI# make

mrcnn/cocoapi/PythonAPI# pip list | grep coco
pycocotools                  2.0                
```
### 3、Demo
```
cd Buildings/mrcnn/
PYTHONIOENCODING=utf-8 python predict.py images/car58a54312d.jpg
```
在有xrdp的界面中会显示：   
![](mrcnn/output/01.png)  
### 4、Training/训练 
```
mrcnn# ./train.sh
或者
mrcnn# PYTHONIOENCODING=utf-8 python coco.py train --dataset data
```
模型和日志会存放在logs目录下。
### 2、Inference/推理
```
mrcnn# ./eval.sh
或者
mrcnn# PYTHONIOENCODING=utf-8 python coco.py evaluate --dataset data

```