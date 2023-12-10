import http.client
import re
from models.BussinessException import BussinessException

def regix_share_url(douyin_share_url: str) -> str:
    share_url = re.search(r'https?://\S+', douyin_share_url)
    if share_url == None:
        raise BussinessException("抖音分享链接提取失败")
    return share_url.group()

def douyin_webApi_1(douyin_web_url: str) -> str:
    conn = http.client.HTTPSConnection("api.tsyinpin.com")

    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"link\"\r\n\r\n\r\n-----011000010111000001101001--\r\n\r\n"

    headers = { 'content-type': "multipart/form-data; boundary=---011000010111000001101001" }

    conn.request("POST", "/douyin_video.php?url={}".format(douyin_web_url), payload, headers)

    res = conn.getresponse()
    data = res.read()

    # 正则表达式模式匹配 realUrl 后的链接
    pattern = r'"realUrl":"([^"]*)"'
    match = re.search(pattern, data.decode("utf-8").replace("\/","/"))
    if match.group(1) == "":
        raise BussinessException("抖音免费接口信息返回失败")

    return match.group(1)

def webApi1_return_message(douyin_share_url: str):
    web_url = regix_share_url(douyin_share_url)
    return douyin_webApi_1(web_url)