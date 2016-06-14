import argparse
from collections import OrderedDict
import json
from six.moves import http_cookies as Cookie
from cookielib import MozillaCookieJar as CookieJar
import shlex
import os, re # JMW

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('url')
parser.add_argument('-d', '--data')
parser.add_argument('--data-binary', default=None) # JMW changed
parser.add_argument('-H', '--header', action='append', default=[])
parser.add_argument('--compressed', action='store_true')
parser.add_argument('-k', '--insecure', action='store_true') # JMW
parser.add_argument('-b', '--cookie', default=None) # JMW
parser.add_argument('-c', '--cookie-jar', default=None) # JMW
parser.add_argument('-L', '--location', action='store_true') #JMW
parser.add_argument('-x', '--proxy', default=None)
parser.add_argument('-o', '--output', default=None)
parser.add_argument('-K', '--config', nargs='?',
                    const='.curlrc') # JMW
parser.add_argument('-O','--remote-name', action='store_true')

def parse(curl_command):
    method = "get"

    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)

    # read from config file if specified
    if parsed_args.config:
        if parsed_args.config == '-':
            # read from stdin
            curl_command = sys.stdin.read()
        else:
            curl_command = curl_config.convert(parsed_args.config)
        tokens = shlex.split(curl_command)
        parsed_args = parser.parse_args(tokens)

    base_indent = " " * 4
    data_token = ''
    post_data = parsed_args.data or parsed_args.data_binary
    if post_data:
        method = 'post'
        try:
            post_data_json = json.loads(post_data)
        except ValueError:
            post_data_json = None

        # If we found JSON and it is a dict, pull it apart. Otherwise, just leave as a string
        if post_data_json and isinstance(post_data_json, dict):
            post_data = dict_to_pretty_string(post_data_json)
        else:
            post_data = "'{}',\n".format(post_data)

        # JMW
        # parse the environment variables out of the string

        env_vars = re.findall(r'\$\{[A-Za-z]+\}', post_data)
        if len(env_vars) > 0:
            post_data_split = re.split(r'\$\{[A-Za-z]+\}', post_data)
            for idx, ev in enumerate(map(lambda x: x.strip('${}'), env_vars)): 
                post_data_split.insert(idx+1, os.environ[ev])

            post_data = ''.join(post_data_split) # reassemble

        data_token = '{}data={}'.format(base_indent, post_data)

    
    cookie_dict = OrderedDict()
    quoted_headers = OrderedDict()
    
    if parsed_args.cookie_jar: # cookie file has been specified
        cookie_jar = CookieJar(parsed_args.cookie_jar)
        cookie_dict = 'cookie_jar'
    else: # original uncurl behavior
        for curl_header in parsed_args.header:
            header_key, header_value = curl_header.split(":", 1)

            if header_key.lower() == 'cookie':
                cookie = Cookie.SimpleCookie(header_value)
                for key in cookie:
                    cookie_dict[key] = cookie[key].value
            else:
                quoted_headers[header_key] = header_value.strip()
    
    proxy_dict = None # default
    if parsed_args.proxy:
        proxy_protocol = parsed_args.proxy.split(':')[0].lower()
        proxy_url = ':'.join(parsed_args.proxy.split(':')[1:])[2:]
        proxy_dict = {proxy_protocol : proxy_url}

    verify = parsed_args.insecure

    result = """requests.{method}("{url}",\n{data_token}{headers_token}{cookies_token}{redirects_token}{proxies_token}{verify_token})""".format(
        method=method,
        url=parsed_args.url,
        data_token=data_token,
        headers_token="{}headers={}".format(base_indent, dict_to_pretty_string(quoted_headers)),
        cookies_token="{}cookies={}".format(base_indent, 'cookie_jar' if parsed_args.cookie_jar else dict_to_pretty_string(cookie_dict)),
        redirects_token="{}allow_redirects={},\n".format(base_indent, parsed_args.location),
        proxies_token="{}proxies={}".format(base_indent, dict_to_pretty_string(proxy_dict)),
        verify_token="{}verify={},\n".format(base_indent, parsed_args.insecure)
        )

    return result


def dict_to_pretty_string(the_dict, indent=4):
    if not the_dict:
        return "{},\n"

    base_indent = " " * indent
    inner_indent = base_indent + " " * 4

    return_value = "{\n"
    sorted_keys = sorted(the_dict.keys())
    for key in sorted_keys:
        value = the_dict[key]
        if isinstance(value, dict):
            value = dict_to_pretty_string(value, indent=indent + 4)
        else:
            value = '"{}",\n'.format(value)
        return_value += inner_indent + '"{0}": {1}'.format(key, value)

    return_value += base_indent + '},\n'

    return return_value
