import requests
import logging

from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class GETInterface:
    __metaclass__ = ABCMeta

    def get(self) -> requests:
        pass


class GETRequest(GETInterface):

    def __init__(self, url="", query_params=dict):
        self.url = url
        self.query_params = query_params

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value: dict):
        self._query_params = value

    def get(self):
        response = requests.get(self.url, params=self.query_params)
        logger.debug(f"GETRequest->get: {response.content}")
        return response
