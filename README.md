This project targets the design of a tool that *resembles* unCurl.
Therefore, we forked that repo, and we intend to re-use those test cases.

We will accept known-good curl GET calls as input.
Those statements can be securely tested for either success else informative failures.
This tool shall convert those same proven curl statement configs into python and java code.

Some REST API's being targeted for json GET calls:
 - CloudForms
 - GitHub
 - MeetUp
 - AWS

We plan to use python *requests* module.
http://docs.python-requests.org/en/master/

We are currently moving tasks and tests to github project issues.
https://github.com/spulec/uncurl/issues

Note that for constrained corporate LAN's,
additional layers of network and service security may be in place.

For example:
 - single sign-on
 - proxy server
<hr>

# Uncurl - Converting curl requests to python-requests

[![Build Status](https://travis-ci.org/spulec/uncurl.png?branch=master)](https://travis-ci.org/spulec/uncurl)

# In a nutshell

Uncurl is a library that allows you to convert curl requests into python code that uses [Requests](github.com/kennethreitz/requests). Since the Chrome network inspector has a nifty "Copy as cURL", this tool is useful for recreating browser requests in python.


## Example

```bash
$ uncurl "curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: foo=bar;' -H 'Connection: keep-alive' --compressed"
requests.get("https://pypi.python.org/pypi/uncurl", headers={
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
}, cookies={
    "foo": "bar",
})
```

The underlying API:

```python
import uncurl

print uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch'")
```

prints the string

```bash
'requests.get("https://pypi.python.org/pypi/uncurl", headers={
    "Accept-Encoding": "gzip,deflate,sdch",
})'
```

You can also pipe input to uncurl:

```bash
pbpaste | uncurl
```

## Install

```console
$ pip install uncurl
```
