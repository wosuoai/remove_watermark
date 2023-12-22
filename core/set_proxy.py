# import requests, random
# from models.BussinessException import BussinessException
# from core.logger import logger
# import time
#
# proxyIpList = []
# with open("core/ip.txt", "r", encoding='utf-8') as f:
#     ipList = f.readlines()
#     if len(ipList) > 0:
#         proxyIpList = eval(ipList[-1])
# logger.info(f"ip.txt中记录的IP是{proxyIpList}")
#
# def set_proxy():
#     """
#     get a proxy ip from ip provider
#     :return:
#     """
#     global proxyIpList
#     while True:
#         if len(proxyIpList) < 1:
#             time.sleep(3)
#             get_ip = requests.get(url=f"").text.split('\r\n')
#
#
#             get_ip = [item for item in get_ip if item != ""]
#             logger.debug(f"新获取到的IP是{get_ip}")
#             proxyIpList = get_ip
#
#             # 每次获取到ip写入到文本里
#             with open("core/ip.txt", "w") as f:
#                 f.write(str(proxyIpList) + "\n")
#                 logger.debug(f"------{str(proxyIpList)}写入到ip.txt--------")
#
#         else:
#             ip = random.choice(proxyIpList)
#             proxies = {
#                 "http": "http://{}".format(ip),
#                 "https": "http://{}".format(ip)
#             }
#
#             url = "https://www.baidu.com/abcd"
#             logger.info(f"用于测试IP是否存活的是链接是{url}，IP是{ip}")
#             try:
#                 response = requests.get(url, proxies=proxies, timeout=3)
#                 if response.status_code == 404:
#                     return proxies
#
#             # 这里的异常只存在超时的情况
#             except Exception as error:
#                 proxyIpList.remove(ip)
#                 logger.error(f"提取IP出现的错误是：{str(error)}")
#                 return None
#
# def useable_ip():
#     count = 5
#     while True:
#         if set_proxy() == None:
#             count -= 1
#             logger.debug("当前返回的IP不可用")
#             set_proxy()
#         else:
#             logger.debug(f"当前拿到的可用IP是{set_proxy()}")
#             return set_proxy()
#
#     raise BussinessException("多次调用ip接口拿不到可用ip")


def useable_ip():
    return None