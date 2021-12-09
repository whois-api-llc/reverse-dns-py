from json import loads, JSONDecodeError
import re

from .net.http import ApiRequester
from .models.response import Response
from .models.request import Fields
from .exceptions.error import ParameterError, EmptyApiKeyError, \
    UnparsableApiResponseError


class Client:
    __default_url = "https://reverse-dns.whoisxmlapi.com/api/v1"
    _api_requester: ApiRequester or None
    _api_key: str

    _re_api_key = re.compile(r'^at_[a-z0-9]{29}$', re.IGNORECASE)

    _PARSABLE_FORMAT = 'json'

    LIMIT = 1000

    JSON_FORMAT = 'json'
    XML_FORMAT = 'xml'

    CNAME = 'cname'
    SOA = 'soa'
    TXT = 'txt'

    def __init__(self, api_key: str, **kwargs):
        """
        :param api_key: str: Your API key.
        :key base_url: str: (optional) API endpoint URL.
        :key timeout: float: (optional) API call timeout in seconds
        """

        self._api_key = ''

        self.api_key = api_key

        if 'base_url' not in kwargs:
            kwargs['base_url'] = Client.__default_url

        self.api_requester = ApiRequester(**kwargs)

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = Client._validate_api_key(value)

    @property
    def api_requester(self) -> ApiRequester or None:
        return self._api_requester

    @api_requester.setter
    def api_requester(self, value: ApiRequester):
        self._api_requester = value

    @property
    def base_url(self) -> str:
        return self._api_requester.base_url

    @base_url.setter
    def base_url(self, value: str or None):
        if value is None:
            self._api_requester.base_url = Client.__default_url
        else:
            self._api_requester.base_url = value

    @property
    def timeout(self) -> float:
        return self._api_requester.timeout

    @timeout.setter
    def timeout(self, value: float):
        self._api_requester.timeout = value

    def get(self, **kwargs) -> Response:
        """
        Get parsed API response as a `Response` instance.

        :key terms: Required. Dictionary. See the API docs for format
        :key record_type: Required. Supported options: CNAME, SOA, TXT
        :key limit: Optional. Integer. Max: `Client.LIMIT`. 1 by default
        :return: `Response` instance
        :raises ConnectionError:
        :raises ReverseDnsApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        kwargs['output_format'] = Client._PARSABLE_FORMAT

        response = self.get_raw(**kwargs)

        try:
            parsed = loads(str(response))
            if 'result' in parsed:
                return Response(parsed)
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)
        except JSONDecodeError as error:
            raise UnparsableApiResponseError(
                    "Could not parse API response",
                    error)

    def get_raw(self, **kwargs) -> str:
        """
        Get raw API response.

        :key terms: Required. Dictionary. See the API docs for format
        :key record_type: Required. Supported options: CNAME, SOA, TXT
        :key limit: Optional. Integer. Max: `Client.LIMIT`. 1 by default
        :key output_format: Optional. Use constants JSON_FORMAT and XML_FORMAT
        :return: str
        :raises ConnectionError:
        :raises ReverseDnsApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        if self.api_key == '':
            raise EmptyApiKeyError('')

        if 'terms' in kwargs:
            terms = Client._validate_terms(kwargs['terms'])
        else:
            terms = None

        if not terms:
            raise ParameterError("Search terms required")

        if 'record_type' in kwargs:
            record_type = Client._validate_record_type(kwargs['record_type'])
        else:
            record_type = None

        if not record_type:
            raise ParameterError("Record type required")

        if 'response_format' in kwargs:
            kwargs['output_format'] = kwargs['response_format']
        if 'output_format' in kwargs:
            output_format = Client._validate_output_format(
                kwargs['output_format'])
        else:
            output_format = Client._PARSABLE_FORMAT

        if 'limit' in kwargs:
            limit = Client._validate_limit(kwargs['limit'])
        else:
            limit = Client.LIMIT

        return self._api_requester.post(self._build_payload(
            self.api_key,
            record_type,
            terms,
            limit,
            output_format
        ))

    @staticmethod
    def _build_payload(
            api_key,
            record_type,
            terms,
            limit,
            output_format
    ) -> dict:
        tmp = {
            'apiKey': api_key,
            'recordType': record_type,
            'terms': terms,
            'limit': limit,
            'outputFormat': output_format,
        }

        payload = {}
        for k, v in tmp.items():
            if v is not None:
                payload[k] = v
        return payload

    @staticmethod
    def _validate_api_key(api_key) -> str:
        if Client._re_api_key.search(
                str(api_key)
        ) is not None:
            return str(api_key)
        else:
            raise ParameterError("Invalid API key format.")

    @staticmethod
    def _validate_limit(value: int) -> int:
        if type(value) is int and 1 <= value <= Client.LIMIT:
            return value

        raise ParameterError(f"Limit must be between 1 and {Client.LIMIT}")

    @staticmethod
    def _validate_output_format(value: str):
        if type(value) is str \
                and value.lower() in [Client.JSON_FORMAT, Client.XML_FORMAT]:
            return value.lower()

        raise ParameterError(
            f"Response format must be {Client.JSON_FORMAT} "
            f"or {Client.XML_FORMAT}")

    @staticmethod
    def _validate_record_type(value: str):
        if type(value) is not str:
            raise ParameterError("Unknown record type")

        if value.lower() in [Client.CNAME, Client.SOA, Client.TXT]:
            return value.lower()

        raise ParameterError("Unknown record type")

    @staticmethod
    def _validate_terms(value) -> list:
        if value is None:
            raise ParameterError("Search term list cannot be None.")
        elif type(value) is list:
            if len(value) < 1 or len(value) > 4:
                raise ParameterError(
                    "Search term list must include form 1 to 4 items.")
            for item in value:
                if 'field' not in item or 'term' not in item:
                    raise ParameterError("Invalid search term format.")
                if item['field'] not in Fields.values():
                    raise ParameterError("Unknown field name.")
                if item['term'] is None or type(item['term']) is not str \
                        or len(item['term']) < 3:
                    raise ParameterError("Term string cannot be empty.")
                if 'exclude' in item and item['exclude'] not in [True, False]:
                    raise ParameterError("Exclude must be true or false")

            return value

        raise ParameterError("Expected a list of pairs field <-> term.")
