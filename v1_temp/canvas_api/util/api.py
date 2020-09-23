import base64
import re, json, collections
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import urllib, urllib.error
import logging
from configparser import ConfigParser

# Some regexes for dealing with HTTP responses from API
CHARSET_PATTERN = re.compile(r'charset=(.+?)(;|$)')

def check_JSON(response):
    '''checks whether a response is JSON'''
    content = response.headers.get('Content-Type')
    return "json" in content

def get_Charset(response):
    '''Gets the charset of an API response'''
    content = response.headers.get('Content-Type')
    if content is None:
        return None
    groups = CHARSET_PATTERN.search(content)
    if groups is None:
        return"utf-8"
    return groups.group(1)

def get_token(username, password):
    en = bytes("{}:{}".format(username, password), encoding="utf-8")
    ba = base64.b64encode(en)
    return ba.decode("utf-8")

def get_response_body(response):
    '''Converts an API response into a readable format'''
    if response is None:
        return ""
    charset = get_Charset(response)
    response_body = response.readline().decode(charset)
    is_JSON = check_JSON(response)
    if is_JSON and response_body is not None:
        response_body = json.loads(response_body, object_pairs_hook=collections.OrderedDict)
    return response_body

def get_url_and_token(filename):
    config = ConfigParser()
    config.read(filename)
    environment = config['default']['env']
    if not environment:
        envs = []
        for section in config.sections():
            if section == 'default':
                continue
            envs.append(section)
        for i in range(len(envs)):
            print("{i}: {env}".format(i=i,env=envs[i]))
        try:
            env = int(input("? "))
        except ValueError as e:
            logging.error("ValueError: {}".format(e))
            env = 0
        try:
            environment = envs[env]
        except IndexError as e:
            logging.error("IndexError: {}".format(e))
    try:
        url = config[environment]['url']
        token = config[environment]['token']
    except KeyError as e:
        logging.error("invalid environment: {}".format(e))
        url = None
        token = None
    return url, token


class Instance:    
    def __init__(self, *args, **kwargs):
        if 'url' in kwargs:
            self._base_url = kwargs['url']
        else:
            self._base_url = None
            
        if 'username' in kwargs and 'password' in kwargs:
            self._token = get_token(kwargs['username'], kwargs['password'])
            self._auth = "Basic"
        elif 'token' in kwargs:
            self._token = kwargs['token']
            self._auth = "Bearer"
        else:
            self._token = None
            self._auth = None

    def call_api(self, url, on_behalf_of=None, is_url_absolute=False, method="GET", post_fields=None):    
        request = self._build_request(url, on_behalf_of, is_url_absolute, method, post_fields)
        try:
            response = urlopen(request)
            logging.debug("HTTP {code} {reason}: {url}".format(code=response.code, reason=response.reason, url=request.full_url))
            return response
        except urllib.error.HTTPError as e:
            logging.debug("HTTP {code} {reason}: {url}".format(code=e.code, reason=e.reason, url=request.full_url))
            return e
        except Exception as e:
            logging.error(e)
            logging.warning("could not make request")

    def _build_request(self, url, on_behalf_of=None, is_url_absolute=False, method="GET", post_fields=None):
        if is_url_absolute:
            urlstr = url
        else:
            urlstr = "{}/{}".format(self._base_url, url)
        request = Request(urlstr)
        #request.add_header('Content-Type', 'application/json')
        if on_behalf_of:
            request.add_header("X-On-Behalf-Of", on_behalf_of)
        if self._auth and self._token:
            request.add_header('Authorization', '{auth} {token}'.format(auth=self._auth, token=self._token))
        request.method = method
        if post_fields is not None:
            request.data = urlencode(post_fields).encode()
        return request

    def get_body(self, response):
        return get_response_body(response)



class CanvasInstance(Instance):    
    def __init__(self, filename):
        url, token = get_url_and_token(filename)
        Instance.__init__(self, url=url, token=token)    

    def call_api(self, url, is_url_absolute=False, method="GET", post_fields=None, all_pages=True):
        response = super().call_api(url,None,is_url_absolute,method,post_fields)
        if response and all_pages and "Link" in response.headers:
            collector = []
            more_pages = True
            while more_pages:
                response_body = get_response_body(response)
                if isinstance(response_body, collections.OrderedDict):
                    response_body = [response_body]
                collector = collector + response_body
                for link in response.headers.get("Link").split(','):
                    print(link)
                    parts = link.split(";")
                    if parts[1].find('next') >= 0:
                        next_page = parts[0]
                        next_page = next_page.replace('<', '')
                        next_page = next_page.replace('>', '')
                        next_page = next_page.strip()
                        response = super().call_api(url=next_page,
                                                    on_behalf_of=None,
                                                    is_url_absolute=True,
                                                    method=method,
                                                    post_fields=post_fields)
                        break
                else:
                    more_pages = False
     
            return collector
        else:
            return get_response_body(response)
