# -*- coding:utf-8 -*-

import csv
import os
import sys


def getFileName(file_type=None):
    """
    获取当前文件夹指定类型文件名列表
    :param file_type:
    :return:
    """
    new_file_name_list = []
    file_name_list = os.listdir("./")
    if file_type:
        for file_name in file_name_list:
            if file_name.endswith(file_type):
                new_file_name_list.append(file_name)
        if len(new_file_name_list) == 0:
            print("提示: 当前文件夹未发现指定类型文件")
    return new_file_name_list


def portFilter(port_blacklist, port):
    flag = True
    for i in port_blacklist:
        try:
            if int(port) == int(i):
                flag = False
        except Exception:
            temp = i.split("-")
            if len(temp) == 2:
                if int(temp[0]) <= int(port) <= int(temp[1]):
                    flag = False
            else:
                print("输入Port格式错误")
    return flag


def getServiceType(csv_all_list, input_service, port_blacklist):
    """
    获取csv文件中所有的数据并以字典的形式返回出去
    :param port_blacklist:
    :param input_service:
    :param csv_all_list:
    :return:
    """
    all_dict = {}
    temp_ip_dict = {}
    #  循环在字典中添加不同服务的key值
    for service in input_service:
        service_name = service[1]
        all_dict[service_name] = []
        temp_ip_dict[service_name] = []
    all_dict["其他未知端口"] = []
    temp_ip_port_list = []
    temp_ip_port_list_2 = []
    # 除去第一行标题栏,从第二行开始遍历
    for num in range(1, len(csv_all_list)):
        csv_list = csv_all_list[num]
        i = 0
        # 判断是否属于端口黑名单
        if portFilter(port_blacklist, csv_list[6]):
            while i < len(input_service):
                service = input_service[i]  # 输入服务列表中取出字典类型的信息
                service_type = service[0]
                service_name = service[1]
                # 服务类型==用户输入的
                if csv_list[7] == service_type:
                    if csv_list[4] not in temp_ip_dict[service_name]:
                        all_dict[service_name].append({"ip": csv_list[4], "port": csv_list[6], "flag": "y"})
                        temp_ip_dict[service_name].append(csv_list[4])  # 存储已经得到的IP
                    else:
                        all_dict[service_name].append({"ip": csv_list[4], "port": csv_list[6], "flag": "n"})
                    temp_ip_port_list.append(csv_list[4] + ":" + csv_list[6] + "\n")  # 存储已经得到的IP+端口(csv中大量重复)
                    break  # 只要判断出是已知服务,就跳出本次循环
                i += 1
            if i == len(input_service):
                temp_ip_port_list_2.append(csv_list[4] + ":" + csv_list[6] + "\n")
    all_dict["其他未知端口"] = list(set(temp_ip_port_list_2) - set(temp_ip_port_list))
    return all_dict


def secondaryGetServiceType(csv_all_list, service_list, port_blacklist):
    all_dict = getServiceType(csv_all_list, service_list, port_blacklist)
    #  循环获取字典的每一种服务的列表,元组形式
    new_service_list = []
    for item in all_dict.items():
        str_service_list = []
        if item[0] == "HTTP服务":
            for ip_port in item[1]:
                if len(str_service_list) == 0:
                    pass
                url = ip_port["ip"] + ":" + ip_port["port"]
                url = "http://%s" % url if "443" not in url else "https://%s" % url
                str_service_list.append(url + "\n")
            str_service_list.insert(0, "\n\n\n%s[%d]\n" % (item[0], len(item[1])))
        elif item[0] == "WebLogic服务(存在控制台部分)" or item[0] == "WebLogic服务(全部)":
            str_service_list = []
            if item[0] == "WebLogic服务(存在控制台部分)":
                global weblogic_http_item
                weblogic_http_item = item
                str_service_list = findSameIP(item)
            elif item[0] == "WebLogic服务(全部)":
                str_service_list = []
                weblogic_ip_port_list = weblogic_http_item[1]  # webgic_http端口IP列表
                # 循环取出所有weblogic列表
                for ip_port in item[1]:
                    i = 0
                    while i < len(weblogic_ip_port_list):
                        # 判断是否为存在控制台的IP
                        if (ip_port["ip"] == weblogic_ip_port_list[i]["ip"]) and (
                                ip_port["port"] == weblogic_ip_port_list[i]["port"]):
                            break
                        elif i == len(weblogic_ip_port_list) - 1:
                            if ip_port["flag"] == "y":
                                str_service_list.append(ip_port["ip"] + ":" + ip_port["port"] + "\n")
                            elif ip_port["flag"] == "n":
                                str_service_list.append(ip_port["ip"] + ":" + ip_port["port"] + "\t# 重复的IP地址\n")
                        i += 1
                str_service_list.insert(0,
                                        "\n\n\nWebLogic服务(无控制台部分)[%d]\n" % (len(item[1]) - len(weblogic_ip_port_list)))
        elif item[0] == "其他未知端口":
            str_service_list = item[1]
            str_service_list.sort()
            str_service_list.insert(0, "\n\n\n%s[%d]\n" % (item[0], len(item[1])))
        else:
            str_service_list = findSameIP(item)
        if len(str_service_list) == 1:
            str_service_list.append("无\n")
        new_service_list += str_service_list
    return new_service_list


def findSameIP(item):
    """
    将列表中以字典形式存储的各个数据转换为字符串存储的方式,并标记出重复的IP地址
    :param item:
    :return: 可写入文件的字符串列表
    """
    ip_port_list = item[1]
    str_service_list = []
    for i in range(0, len(ip_port_list)):
        ip_port = ip_port_list[i]
        if ip_port["flag"] == "y":
            str_service_list.append(ip_port["ip"] + ":" + ip_port["port"] + "\n")
        elif ip_port["flag"] == "n":
            str_service_list.append(ip_port["ip"] + ":" + ip_port["port"] + "\t# 重复的IP地址\n")
    str_service_list.insert(0, "\n\n\n%s[%d]\n" % (item[0], len(item[1])))
    return str_service_list


def main():
    # 端口黑名单, 单个端口用数字,范围端口使用双引号括起来(不然会变成减法...)
    port_blacklist = [0, "10000-65535"]
    service_list = [
        ("HTTP Server Type and Version", "HTTP服务"),
        ("FTP Server Detection", "FTP服务"),
        ("SSH Server Type and Version Information", "SSH服务"),
        ("MySQL Server Detection", "MySQL数据库"),
        ("Microsoft SQL Server STARTTLS Support", "SQLServer数据库"),
        ("Oracle Database Detection", "Oralcle数据库"),
        ("Redis Server Detection", "Redis服务"),
        ("Oracle WebLogic HTTP Detection", "WebLogic服务(存在控制台部分)"),
        ("Oracle WebLogic Detection (Combined)", "WebLogic服务(全部)"),
        ("AJP Connector Detection", "AJP服务"),
        ("Apache Tomcat Detection", "tomcat默认页面"),
        ("Elasticsearch Detection", "Elasticsearch服务"),
    ]
    file_name_list = getFileName(".csv")
    for i, file_name in enumerate(file_name_list):
        print(i + 1, file_name)
    if len(sys.argv) == 2:
        if sys.argv[1] in file_name_list:
            file_name_list = [sys.argv[1]]
        else:
            print("当前目录不存在该文件")
            os.exit()
    for file_name in file_name_list:
        with open(file_name, "r", encoding="ISO-8859-1") as f:
            csv_all_list = list(csv.reader(f))
        with open(file_name[:file_name.rfind(".")] + "(针不戳).txt", "w", encoding="utf-8") as f:
            f.write("XINYU2428")
            f.writelines(secondaryGetServiceType(csv_all_list, service_list, port_blacklist))


if __name__ == '__main__':
    main()
