from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    paramserror = 400  # 参数错误
    unauth = 401  # 未授权
    methoderror = 405  # 请求方法错误
    servererror = 500  # 服务器错误


# 返回方法
def result(code=HttpCode.ok, message='', data=None, kwargs=None):
    json_dict = {'code': code, 'message': message, 'data': data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():  # 其他参数检查是否有值是否是字典 ，再拼接
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


#  封装错误代码的方法
def ok():
    return result()


def params_error(message="", data=None):
    return result(code=HttpCode.paramserror, message=message, data=data)


def unauth(message="", data=None):
    return result(code=HttpCode.unauth, message=message, data=data)


def method_error(message='', data=None):
    return result(code=HttpCode.methoderror, message=message, data=data)


def server_error(message='', data=None):
    return result(code=HttpCode.servererror, message=message, data=data)
