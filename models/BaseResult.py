from typing import Any

def Response(code: int,data: Any,message: str="请求成功"):
    return {
        "code": code,
        "data": data,
        "message": message,
    }


def KownedException(code: int,data: Any,message: str="请求失败"):
    return {
        "code": code,
        "data": data,
        "message": message,
    }