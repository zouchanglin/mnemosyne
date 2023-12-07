from flask import Flask, jsonify

from unity_response import UnityResponse


class CustomFlask(Flask):
    def make_response(self, rv):
        """视图函数可以直接返回: list、dict、None"""
        if rv is None or isinstance(rv, (list, dict)):
            rv = UnityResponse.success(rv)

        if isinstance(rv, UnityResponse):
            rv = jsonify(rv.to_dict())
        return super().make_response(rv)
