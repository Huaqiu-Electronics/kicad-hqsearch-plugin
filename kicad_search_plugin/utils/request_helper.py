from urllib import parse


class RequestHelper:
    @staticmethod
    def convert_dict_to_request_data(input: "dict"):
        print( f"request data:{parse.urlencode(list(input.items())).encode()}" )
        return parse.urlencode(list(input.items())).encode()
