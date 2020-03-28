# coding=utf-8


import datetime

from .aliyun_oss import get_img_oss_url

# 将sql原生语句执行之后返回的结果转换为字典格式

"""
     reserve:为预设key,当执行sql原生语句给与的结果进行字典转换,当key与查询出的字段为一致则进行一些额外操作
     例如:
        
        数据库查询得到字段(select field_1,field_2 from table where ...) 其中field_*需要经过特别处理,
        创建一个list_items 列表和 item字典,
        数据并循环(sql原生语句查询得到的结构为一个列表,使用dir可以看到该循环的keys...操作方法),
        使用该数据的 enumerate(result.keys()) 得到index索引和key值
        (注意在select field_1 as u1,field_2 as u2 from ...    那么在keys中的key为as之后的值,无as则为表中字段名)
        将得到的key填充到字典item的key位置,value为索引位置
        
        如下 一个时间格式, 经过isinstance 是否该字段为datetime类,是则进行字符串转换
        
        这里因为是对这个项目负责,该项目用户上传文件都市通过阿里云oss的sign签名
            后端返回oss中的路径,由前端上传阿里云oss,如果经过保存则由前端上传完毕之后把oss路径返回后端保存,不经过服务器代理上传
                所以当用户查询到一些保存在oss中数据时,不处理返回的则是单纯的在oss保存路径,无效 
        
        这个方法已经固定了,如果有需求可以另外重构
        
"""
def sql_result_to_dict(results,reserve=None):
    list_items = []

    for result in results:
        item = {}
        for index ,key in enumerate(result.keys()):
            if isinstance(result[index], datetime.datetime) or isinstance(result[index], datetime.date):
                item[key] = result[index].strftime('%Y-%m-%d %H:%M:%S')
            else:
                item[key] = result[index]

            if key == reserve:
                item[key] = get_img_oss_url(result[index],86000/2)
        list_items.append(item)

    return list_items