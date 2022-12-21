from flask import Response, Request
import json
from keys import Keys


class Validation:
    

    def __init__(self, validation: bool, response: Response) -> None:
        self.validation = validation
        self.response = response


    @classmethod
    def __error_validation(cls, message: str, code: int):
        return Validation(False, Response(json.dumps({'message':message}, indent = 2), code, mimetype = 'application/json'))


    @classmethod
    def __ok_validation(cls):
        return Validation(True, Response())


    @classmethod
    def payload_size_checker(cls, length: int):
        if length == 0 or length == None:
            return cls.__error_validation('No auth token', 204)
        return cls.__ok_validation()
        

    @classmethod
    def key_checker(cls, key: str):
        if key == None: 
            return cls.__error_validation('No key', 401)
        if len(key) == 0 or key.isspace():
            return cls.__error_validation('Incorrect key', 401)
        return cls.__ok_validation()


    @classmethod
    def token_checker(cls, token: str):
        if token == None: 
            return cls.__error_validation('No auth token', 401)
        if len(token) == 0 or token.isspace():
            return cls.__error_validation('Incorrect token', 401)
        if token != cls.CONFIRMATION_TOKEN:
            return cls.__error_validation('Incorrect token', 401)
        return cls.__ok_validation()

    
    @classmethod
    def issuer_key_checker(cls, key: str):
        auth = cls.key_checker(key)
        if not auth.validation:
            return auth.response
        if not Keys.issuer_key_checker(key):
            return cls.__error_validation('Incorrect key', 422)
        return cls.__ok_validation()


    @classmethod
    def receiver_key_checker(cls, key: str):
        auth = cls.key_checker(key)
        if not auth.validation:
            return auth.response
        if not Keys.connection_checker(key):
            return cls.__error_validation('No connection', 404)
        return cls.__ok_validation()