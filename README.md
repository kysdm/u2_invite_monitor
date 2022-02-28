# 用户保种量监控

> 重构了整个脚本，未长时间测试，可能有未知 BUG。


## 编写环境
    Python 3.9.9  
    mysql 8.0.27


## 使用方法

1. 导入SQL文件  
    ``` bash
    mysql < u2_invite.sql
    ```

2. 修改配置文件  
    ``` bash
    cookie sql # 需按照自己的环境更改
    ```

3. 创建虚拟环境  
    ``` bash
    python3 -m venv ./virtual
    ```

4. 激活虚拟环境  
    ``` bash
    source ./virtual/bin/activate
    ```

5. 安装依赖  
    ``` bash
    pip3 install -r requirements.txt
    ```

6. 运行  
    ``` bash
    python3 run.py
    ```


## 说明
    每15分钟抓取一次数据
