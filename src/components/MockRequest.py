import logging, telegram, json

from telegram.utils.request import Request

class MockRequest(Request):
    def __init__(self):
        self.__response_map = {
            "get": {},
            "post": {},
            # "retrieve": {},
            # "download": {}
        }

        self.__trigger_map = {
            "get": {},
            "post": {},
            # "retrieve": {},
            # "download": {}
        }

        self.__sent_responses = []

        self.__logger = logging.getLogger(__name__)

        self._con_pool_size = 1

    def add_mock_response(self, method, endpoint, response, domain="mock.bot/mock:token"):
        method = method.lower()

        if method not in self.__response_map.keys():
            self.__logger.warning("Unable to register mock response ({}, {}, {}), unknown method {}".format(method))
            return

        self.__response_map[method]["{}/{}".format(domain, endpoint)] = response

    def add_trigger(self, method, endpoint, trigger, domain="mock.bot/mock:token"):
        method = method.lower()

        if method not in self.__trigger_map.keys():
            self.__logger.warning("Unable to register mock response ({}, {}, {}), unknown method {}".format(method))
            return

        self.__trigger_map[method]["{}/{}".format(domain, endpoint)] = trigger

    def get(self, url, timeout=None):
        try:
            trigger = self.__recover_trigger("get", url)

            if trigger:
                trigger()

            try:
                response_data = self.__response_map["get"][url]
                self.__send_response("GET", response_data)

                return response_data
            except KeyError:
                if not trigger:
                    self.__logger.warning("Unknown GET mock reaction (no data/trigger) for url {}".format(url))

                return None

        except Exception as e:
            self.__logger.error("Unknown exception on GET request with url {} ({})".format(url, e))
            return None

    def post(self, url, data, timeout=None):
        try:
            serialized_data = str(data)

            trigger = self.__recover_trigger("post", url, serialized_data)

            try:
                # Retrieve possible data dictionary for the given URL 
                data_dict = self.__response_map["post"][url]
            except KeyError:
                data_dict = None

            if not trigger and not data_dict:
                self.__logger.warning("Unknown POST mock reaction (no data/trigger) for url {} with data {}".format(url, data))

                return None

            if trigger:
                trigger()

            if data_dict:
                try:
                    response_data = data_dict[serialized_data]
                except KeyError:
                    self.__logger.warning("Unknown POST mock response data {} with url {} ".format(data, url))
                    return None

                self.__send_response("POST", response_data)

                return response_data

        except Exception as e:
            self.__logger.error("Unknown exception on POST request with url {} and data {} ({})".format(url, data, e))
            return None

    def __recover_trigger(self, method, url, index=None):
        try:
            if not index:
                return self.__trigger_map[method][url]
            else:
                return self.__trigger_map[method][url][index]
        except KeyError:
            return None

    def pull_responses(self):
        current_responses = list(self.__sent_responses)

        self.__sent_responses.clear()

        return current_responses

    def __send_response(self, method, data):
        self.__sent_responses.append({
            "method": method,
            "data": data
        })

        return data