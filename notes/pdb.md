# 10分钟教程掌握Python调试器pdb
如果你还主要靠print来调试代码，那值得花10分钟试试pdb这个Python自带的Debug工具。

pdb有2种用法：   
* 非侵入式方法（不用额外修改源代码，在命令行下直接运行就能调试）   
`python3 -m pdb filename.py`  
* 侵入式方法（需要在被调试的代码中添加一行代码然后再正常运行代码）   
`import pdb;pdb.set_trace()`   

当你在命令行看到下面这个提示符时，说明已经正确打开了pdb   
`(Pdb) `   
然后就可以开始输入pdb命令了，下面是pdb的常用命令   
|命令	|   用途|
|:-|:-|
|break 或 b	|设置断点|
|continue 或 c|	继续执行程序, 或是跳到下个断点|
|list 或 l|	查看当前行的代码段|
|step 或 s|	进入函数|
|return 或 r|	执行代码直到从当前函数返回|
|exit 或 q|	中止并退出|
|next 或 n|	执行下一行|
|p 或!	|打印变量的值，例如p a|
|help 或 h	|帮助|

### 代码部分
```
# utils.py
def add(a,b):
    return a+b

# main.py
import utils

def cal(a,b):
    import pdb;pdb.set_trace()  #引入pdb代码片段，不需要时，可以注掉
    c=utils.add(a,b)
    print c

if __name__=='__main__':
   cal(3,4)
```
### 调试部分
```
root@native-sunaihua-5-25-18:~/pdb_test# python main.py   #开始
> /root/pdb_test/main.py(5)cal()
-> c=conf.add(a,b)
(Pdb) s                                                   #进入调用函数
--Call--
> /root/pdb_test/conf.py(1)add()
-> def add(a,b):
(Pdb) l                                                    #查看代码
  1  -> def add(a,b):
  2         return a+b
[EOF]
(Pdb) b 2                                                  #设置断点
Breakpoint 1 at /root/pdb_test/conf.py:2
(Pdb) c                                                    #继续执行到下一个断点
> /root/pdb_test/conf.py(2)add()
-> return a+b
(Pdb) n                                                    #执行下一行         
--Return--
> /root/pdb_test/conf.py(2)add()->7
-> return a+b
(Pdb) n
> /root/pdb_test/main.py(6)cal()
-> print c
(Pdb) n
7
--Return--
> /root/pdb_test/main.py(6)cal()->None
-> print c
(Pdb) p c                                                   #查看c变量的值      
7
(Pdb) q                                                     #退出
```

## Reference
[1] https://www.ibm.com/developerworks/cn/linux/l-cn-pythondebugger/index.html