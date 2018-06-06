"""Utility library for DNA-C Northbound API

Leverages the requests library to interface with Northbound REST API.
"""
import logging
import json
from http.cookies import SimpleCookie

from requests import Session
from requests.auth import HTTPBasicAuth


logger = logging.getLogger(__name__)


class DNACHelper(object):
    """Utility class for interacting with Onboarding service on DNA-C. The only
    class level attribute stored is the Northbound REST API client.
    """

    address = ''
    user = ''
    password = ''

    client = None

    _rest_base_api = 'api/v1'
    _auth_uri = 'api/system/v1/auth/login'

    def __init__(self, address='', user='', password=''):
        """Initializes NB REST API client for DNA-C. Performs initial auth login
        and token exchange.

        Specify DNA-C instance by providing pyATS device instance OR all of the
        following: address, user, password.

        Args:
            device (Device, optional): pyATS device object for DNA-C cluster
            address (str, optional): DNA-C address
            user (str, optional): DNA-C login user
            password (str, optional): DNA-C login password

        Raises:
            ConnectionError: failed to authenticate client

        """
        self.address = address
        self.user = user
        self.password = password
        self._create_client()

    def _create_client(self):
        """Initializes REST client

        Raises:
            ConnectionError: failed to authenticate client

        """
        self.client = Session()
        # Disable server authentication from client-side
        self.client.verify = False
        self._gen_token()

    def _gen_token(self):
        """Performs auth login, extracts JWT, and sets JWT in header"""
        # Set login authorization required for token generation
        self.client.auth = HTTPBasicAuth(self.user, self.password)
        # Attempt login
        self.client.headers.update({'Content-Type': 'application/json'})
        resp = self.client.get('https://{}/{}'.format(self.address,
                                                      self._auth_uri))
        if (resp.status_code != 200) or ('set-cookie' not in resp.headers):
            logger.error('Failed to initialize client')
            logger.debug(resp)
            raise ConnectionRefusedError("HTTP Status %s" % resp.status_code)
        # Set session cookie to JWT retrieved from response header
        cookie = SimpleCookie()
        cookie.load(resp.headers['set-cookie'])
        client_cookies = {key: morsel.value for key, morsel in cookie.items()}
        self.client.cookies.update(client_cookies)

    def _call_api(self, request_type, path, params=None, data=None, files=None):
        """Calls REST API with provided information

        Args:
            request_type (str): GET, POST, PUT, DELETE, HEAD, and OPTIONS
            path (str): REST API path (e.g. onboarding/pnp-device)
            params (dict, optional): Dictionary to send in the query string
            data (dict, optional): Dictionary to send in the body of the Request

        Returns:
            requests.Response: requests response object
            None: upon call failure

        """
        url = 'https://{}/{}/{}'.format(self.address, self._rest_base_api, path)
        if not hasattr(self.client, request_type.lower()):
            raise ValueError("request_type (%s) unsupported" % request_type)
        send_kwargs = dict(url=url, params=params, data=data, files=files)
        if files:
                if isinstance(send_kwargs["files"], dict):
                    fd = send_kwargs["files"]
                    if len(fd) == 1 and isinstance(list(fd.values())[0], tuple):
                        ft = fd[list(fd.keys())[0]]
                        fd[list(fd.keys())[0]] = ft[:1] + (open(ft[1], "rb"),) + ft[2:]
                    else:
                        send_kwargs["files"] = {key: open(val, "rb") for key, val in fd.items()}

                if isinstance(send_kwargs["files"], str):
                    send_kwargs["files"] = open(send_kwargs["files"], "rb")

                if self.client.headers.get("Content-Type") == "application/json":
                    self.client.headers.pop("Content-Type")
        response = getattr(self.client, request_type.lower())(**send_kwargs)
        self.client.headers.update({"Content-Type": "application/json"})
        if not response or response.status_code not in (200, 204):
            logger.error("API call failed")
            logger.debug(response)
            return None
        return response

    def get_device(self, serialnumber=None, state=None, limit=None):
        request_type = 'GET'
        path = 'onboarding/pnp-device'
        payload={}
        if serialnumber:
            payload.update(serialNumber=serialnumber)
        if state:
            payload.update(state=state)
        if limit:
            payload.update(limit=1000)
        response = self._call_api(request_type, path, params=payload)
        if not response or response.status_code not in (200, 204):
            return ''
        response_body = response.json()
        if not response_body:
            return ''
        return response_body

    def delete_device(self, device_id):
        """Deletes the specified device from DNA-C database

        API: onboarding/pnp-device

        Args:
            device_id (str): Device ID

        Returns:
            bool: True if deleted successfully, False otherwise

        """
        request_type = 'DELETE'
        path = 'onboarding/pnp-device/{deviceId}'.format(deviceId=device_id)
        response = self._call_api(request_type, path)
        if not response or response.status_code not in (200, 204):
            return False
        return True

    def post_file(self, namespace, file):
        request_type = 'POST'
        path = 'file/'+namespace
        data = {}
        files={"fileUpload":file}
        # self.client.headers['Content-Type']='multipart/form-data'
        response = self._call_api(request_type,path,files=files)
        if not response or response.status_code not in (200, 204):
            return ''
        response_body = response.json()
        if not response_body:
            return ''
        return response_body


    def get_files(self, namespace):
        request_type = 'GET'
        path = 'file/namespace/'+namespace
        response = self._call_api(request_type, path)
        if not response or response.status_code not in (200, 204):
            return ""
        return response.json()['response']

    def post_workflow(self,workflow):
        request_type = 'POST'
        path = 'onboarding/pnp-workflow'
        response = self._call_api(request_type, path,data=json.dumps(workflow))
        if not response or response.status_code not in (200, 204):
            return response
        return response.json()

    def post_project(self, project):
        request_type = 'POST'
        path = 'onboarding/pnp-project'
        response = self._call_api(request_type, path,data=json.dumps(project))
        if not response or response.status_code not in (200, 204):
            return response
        return response.json()

    def post_device_claim(self, claim_data):
        request_type = 'POST'
        path = 'onboarding/pnp-device/claim'
        response = self._call_api(request_type, path, data=json.dumps(claim_data))
        if not response or response.status_code not in (200, 204):
            return response
        return response.json()

    def delete_config(self, id):
        request_type = 'DELETE'
        path = 'file/{fileId}'.format(fileId=id)
        response = self._call_api(request_type, path)