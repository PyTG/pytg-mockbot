import logging, telegram, json

from telegram.utils.request import Request

class MockRequest(Request):
    def __init__(self):
        self.response_map = {
            "get": {},
            "post": {},
            "retrieve": {},
            "download": {}
        }

        self.logger = logging.getLogger(__name__)

        pass

    def add_mock_response(self, method, url, response):
        method = method.lower()

        if method not in self.response_map.keys():
            self.logger.warning("Unable to register mock response ({}, {}, {}), unknown method {}".format(method))
            return

        self.response_map[method][url] = response

    def get(self, url, timeout=None):
        try:
            return self.response_map["get"][url]
        except KeyError:
            self.logger.warning("Unknown GET mock response for url {}".format(url))
            return None
        except Exception as e:
            self.logger.error("Unknown exception on GET request with url {} ({})".format(url, e))
            return None

    def post(self, url, data, timeout=None):
        try:
            # Retrieve possible data dictionary for the given URL 
            data_dict = self.response_map["post"][url]

            # Look for the right data (if present)
            for key in data_dict:
                if key == data:
                    return data_dict[key]

            # If not, return null
            self.logger.warning("Unknown POST mock response data {} with url {} ".format(url, data))
            return None
        except KeyError:
            self.logger.warning("Unknown POST mock response for url {}".format(url, data))
            return None
        except Exception as e:
            self.logger.error("Unknown exception on GET request with url {} and data {} ({})".format(url, data, e))
            return None

    # def _request_wrapper(self, *args, **kwargs):
    #     data = {}

    #     return data

    # def _parse(self, json_data):
    #     return json_data