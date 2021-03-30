# 使用Flask的组件大全、怎样部署Flask

## 本部署框架的好处
1. 单文件启动，python3 pss_waitress.py
2. 入口文件可以多次启动，比如多次运行python3 pss_waitress.py，这样的好处是可以把python3 pss_waitress.py加到定时任务，每1分钟运行一次，那么如果进程挂掉了，就会自己启动起来了；
3. 包含日志打印模块，打印到文件，并且会滚动删除

## 使用说明


1. 安装包

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask waitress requests
```


2. 启动服务的方法：
```
python3 pss_waitress.py
```


