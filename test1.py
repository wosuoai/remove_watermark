import http.client,re

def douyin_webApi_1(douyin_web_url: str) -> dict:
    conn = http.client.HTTPSConnection("api.tsyinpin.com")

    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"link\"\r\n\r\n\r\n-----011000010111000001101001--\r\n\r\n"

    headers = { 'content-type': "multipart/form-data; boundary=---011000010111000001101001" }

    conn.request("POST", "/douyin_video.php?url={}".format(douyin_web_url), payload, headers)

    res = conn.getresponse()
    data = res.read()

    # 正则表达式模式匹配 realUrl 后的链接
    pattern = r'"realUrl":"([^"]*)"'
    match = re.search(pattern, data.decode("utf-8").replace("\/","/"))

    return data


print(douyin_webApi_1("https://v.douyin.com/i8R37qGb/"))