from typing import Any

def Response(code: int,data: Any,method_code: int,message: str="请求成功"):
    return {
        "code": code,
        "data": data,
        "message": message,
        "method_code": method_code
    }


def KownException(code: int,data: Any,method_code: int,message: str="请求失败"):
    return {
        "code": code,
        "data": data,
        "message": message,
        "method_code": method_code
    }