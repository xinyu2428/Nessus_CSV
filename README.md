## 0x00 前言
之前写的一个脚本, 近期又用上了, 分享一下.<br />如果你有批量扫描IP的工作场景, 那么此脚本对你是很有帮助的.<br />
<br />**工作需求:** 经常使用Nessus会发现有时会有漏洞漏扫的情况, 此时需要我们根据扫描出来的服务及端口去确认是否存在未扫描出来的漏洞. 但Nessus上查看端口太过繁琐, 为了解决这个问题, 于是就有了此脚本.<br />**使用场景:** 使用Nessus进行批量扫描时<br />
<br />
<br />

## 0x01 使用说明
### 1).Nessus批量扫描完成后, 导出CSV格式的结果记录
![](https://cdn.nlark.com/yuque/0/2021/png/516736/1618536823079-d963a18d-6442-4cdc-b795-2c8f3a55e889.png#clientId=u579607ba-450e-4&from=paste&id=uc00f652e&margin=%5Bobject%20Object%5D&originHeight=905&originWidth=1606&originalType=binary&size=125838&status=done&style=stroke&taskId=ud7a4cc1b-4c7d-4188-a244-a2fe013b105)<br />
<br />

### 2).将脚本与生成的CSV文件放在同一个文件夹内
![](https://cdn.nlark.com/yuque/0/2021/png/516736/1618536984240-ab18e251-9a27-499e-9ca7-6940856958ee.png#clientId=u579607ba-450e-4&from=paste&id=u5321a42e&margin=%5Bobject%20Object%5D&originHeight=188&originWidth=1036&originalType=binary&size=19664&status=done&style=stroke&taskId=u17171247-5971-48ac-b013-d00efbedeec)<br />
<br />

### 3).运行批处理
将自动读取当前文件夹内的所有CSV文件进行处理, 并分别生成TXT格式的处理结果<br />如下是处理结果部分截图:<br />![](https://cdn.nlark.com/yuque/0/2021/png/516736/1618537343816-433d4afd-f502-4a91-809e-697ac154fb0e.png#clientId=u579607ba-450e-4&from=paste&id=u7d26061e&margin=%5Bobject%20Object%5D&originHeight=880&originWidth=1108&originalType=binary&size=64950&status=done&style=stroke&taskId=uf87bd2a9-e55c-492d-8dbf-d0347ddc951)<br />
<br />
<br />

## 0x02 自定义部分
![](https://cdn.nlark.com/yuque/0/2021/png/516736/1618537594268-60bc6a07-b9f7-410a-9222-2a42ee43e4b8.png#clientId=u579607ba-450e-4&from=paste&id=AAyQn&margin=%5Bobject%20Object%5D&originHeight=430&originWidth=916&originalType=binary&size=51227&status=done&style=stroke&taskId=uf96dc6ac-7a5f-4dde-88b2-e3d625f1f9f)<br />
<br />**可自定义部分有两个地方**
### 1).端口黑名单
意义: Nessus会扫描到一些无用端口, 如0, 7, 9或udp等端口这种对我们测试意义不大, 可以选择过滤.<br />单个端口用数字,范围端口使用双引号括起来(不然会变成减法...)<br />这里过滤的端口将不再生成文档中显示.<br />
<br />

### 2).Nessus扫描指纹
脚本中已加入常见端口服务指纹<br />
<br />添加指纹示例如下:<br />1.如下图, 我们在Nessus中找到 CVE-2019-0708 漏洞的指纹<br />![](https://cdn.nlark.com/yuque/0/2021/png/516736/1618538906562-a34b908f-77b1-4861-98cf-4253eea5c601.png#clientId=u579607ba-450e-4&from=paste&id=uf887d97c&margin=%5Bobject%20Object%5D&originHeight=587&originWidth=1452&originalType=binary&size=66006&status=done&style=stroke&taskId=u5b5d2705-df39-4d50-8b9c-ea5746c639c)<br />
<br />
<br />2.添加进脚本中<br />![](https://cdn.nlark.com/yuque/0/2021/png/516736/1618538827298-cd68a0a7-0569-43be-a474-e07bdd945017.png#clientId=u579607ba-450e-4&from=paste&id=ud31584a8&margin=%5Bobject%20Object%5D&originHeight=364&originWidth=974&originalType=binary&size=50480&status=done&style=stroke&taskId=u836073cb-178f-4f9c-9572-cdec3f2bbf4)<br />
<br />
<br />3.生成文件结果图如下:<br />![](https://cdn.nlark.com/yuque/0/2021/png/516736/1618539083808-1c45b2c5-43e4-45b3-9fc4-04b2a0c966dc.png#clientId=u579607ba-450e-4&from=paste&id=ua38ba037&margin=%5Bobject%20Object%5D&originHeight=880&originWidth=1162&originalType=binary&size=74294&status=done&style=stroke&taskId=u66610867-7566-496d-9ca0-5f13ea968cb)<br />
<br />
<br />

## 0x03 项目地址
[https://github.com/xinyu2428/Nessus_CSV](https://github.com/xinyu2428/Nessus_CSV)<br />
<br />
<br />
<br />
<br />

