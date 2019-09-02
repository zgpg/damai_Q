# damai_Q
基于Python和Selenium实现的抢票脚本

## 依赖
Python3.6+ 和 Chrome浏览器

安装依赖包
```
pip3 install -r requirements.txt
```
## 用法
1. 修改config.ini文件，保存你的配置信息
```
;修改说明：
;[信息]
;name           联系人写你的名字
;phone          换票用手机号
;[模式]
;round          抢票场次(1/2)
;quantity       抢票张数(1/2)
;grade          票档（1/2/3/4）
;express        是否快递(True/False)
;               True:快递 选快递需要提前在大麦登记好自己的收货信息，而且选这个的话页面加载会慢，不推荐使用
;               False:电子票
;url            抢票地址
```
2. 执行脚本(首次执行会有防火墙提示，通过后关闭并重新运行)
```
python main.py
```
3. 根据网页提示登陆你的大麦账号
4. 成功登陆后会进入买票页面，页面会判断“确定”按钮是否可用而不断刷新，一旦可用会自动开始抢票
5. 继续手动操作
6. 如果进入了“订单确认”页面，会自动填写联系人信息并提交(注意，这里默认使用电子票方式订票)

--- 
(祝你抢票成功)

## 免责声明 
1. 本脚本源码公开可见，仅做研究使用，不得用于非法获利，不得从于商业行为， 如产生法律纠纷与脚本作者无关!!!