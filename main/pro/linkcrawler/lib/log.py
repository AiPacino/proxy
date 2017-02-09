# coding:utf-8
import datetime

def write_log(filename, content, url):
    """把错误信息写入日志"""

    """获取log日志文件的句柄"""
    ferror = open(filename, "a")

    """写入错误信息error 加上空格"""
    ferror.write("#"+content+"# #")

    """写入现在的时间"""
    try:
        ferror.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"# #")
        """写入出错的url地址"""
        ferror.write(url+"#\n")
    except:
        pass
    """关闭文件"""
    ferror.close()
