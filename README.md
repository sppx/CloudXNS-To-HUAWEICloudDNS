# CloudXNS-To-HUAWEICloudDNS
# 导出CloudXNS记录为华为云DNS格式csv导出文件

## 注意事项
* Python 3.x
* 懒，只做了单域名导出，也没必要导出所有域名
* 目前支持且仅支持A(X)、CNAME(X)、MX、TXT、301/302跳转，不支持SRV及LINK记录，请自行寻找替代出路
* 301/302跳转整合为显性(显式)301跳转
* 导出后记录分别记录到两个文件，一个是以域名为文件名的.csv格式，另一个带有disable-前缀的，以域名为文件名的.csv格式。前者是CloudXNS里面启用状态的域名，后者为禁用状态的域名，因为京东云DNS导入的时候不能导入状态。
* 因为编码类型为utf-8（京东云DNS导入检查），所以windows下Excel、WPS等直接打开是乱码，请用notepad++打开

## 食用方法
1. 下载完整Git项目压缩包或者使用git clone命令下载
2. 修改api_key、secret_key为你的CloudXNS的
3. 安装lrzsz 支持 和python 支持pyexcel
4. python start.py 域名
5. 接收xlsx文件
6. 右上角，批量导入
7. 打完，收工

## 鸣谢
本脚本使用的CloudXNS Python SDK版本为：https://github.com/wevsty/CloudXNS_Python3_SDK ，官方版本只支持Python2。使用Python2的请自行安装官方Python SDK，然后修改代码导入。
