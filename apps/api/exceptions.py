
class APIError(Exception):
    def __init__(self, *args, **kwargs):
        response = kwargs.get('response', None)

        if response is None:
            return super(APIError, self).__init__(*args, **kwargs)

        json = response.json()

        self.status = json['status']['status_code']
        self.message = json['status']['message']
        custom_args = [self.message]

        return super(APIError, self).__init__(*custom_args)
