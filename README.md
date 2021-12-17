aiowebdav
=========
[![pypi](https://img.shields.io/pypi/v/aiowebdav.svg)](https://pypi.org/project/aiowebdav/)
![python](https://img.shields.io/pypi/pyversions/aiowebdav)
![implementation](https://img.shields.io/pypi/implementation/aiowebdav)
![wheel](https://img.shields.io/pypi/wheel/aiowebdav)
![action](https://img.shields.io/github/workflow/status/synodriver/aiowebdav/upload/aiowebdav)

Package aiowebdav based on https://github.com/designerror/webdav-client-python but uses `aiohttp` instead of `requests`.
It provides easy way to work with WebDAV-servers.

Installation
------------
```bash
$ pip install aiowebdav
```

Sample Usage
------------

```python
import asyncio
from aiowebdav.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login': "login",
 'webdav_password': "password",
 "disable_check": True
}

async def main():
    client = Client(options)
    client.verify = False  # To not check SSL certificates (Default = True)
    client.execute_request("mkdir", 'directory_name')
asyncio.run(main())
```

Webdav API
==========

Webdav API is a set of webdav actions of work with cloud storage. This set includes the following actions:
`check`, `free`, `info`, `list`, `mkdir`, `clean`, `copy`, `move`, `download`, `upload`, `publish` and `unpublish`.

**Configuring the client**

Required key is host name or IP address of the WevDAV-server with param name `webdav_hostname`.  
For authentication in WebDAV server use `webdav_login`, `webdav_password`.  
For an anonymous login do not specify auth properties.

```python
from aiowebdav.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login': "login",
 'webdav_password': "password"
}
client = Client(options)
```

If your server does not support `HEAD` method or there are other reasons to override default WebDAV methods for actions use a dictionary option `webdav_override_methods`. 
The key should be in the following list: `check`, `free`, `info`, `list`, `mkdir`, `clean`, `copy`, `move`, `download`, `upload`,
 `publish` and `unpublish`. The value should a string name of WebDAV method, for example `GET`.

```python
from aiowebdav.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login': "login",
 'webdav_password': "password",
 'webdav_override_methods': {
  'check': 'GET'
 }

}
client = Client(options)
```

For configuring a requests timeout you can use an option `webdav_timeout` with int value in seconds, by default the timeout is set to 30 seconds.

```python
from aiowebdav.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login': "login",
 'webdav_password': "password",
 'webdav_timeout': 30
}
client = Client(options)
```

When a proxy server you need to specify settings to connect through it.

```python
from aiowebdav.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login': "w_login",
 'webdav_password': "w_password",
 'webdav_proxy': "http://127.0.0.1:8080",
 'webdav_proxy_auth': "xxx",
}
client = Client(options)
```

If you want to use the certificate path to certificate and private key is defined as follows:

```python
from aiowebdav.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login': "w_login",
 'webdav_password': "w_password",
 'webdav_ssl': 'sslcontext'
}
client = Client(options)
```

Or you want to limit the speed or turn on verbose mode:

```python
options = {
 ...
 'recv_speed' : 3000000,
 'send_speed' : 3000000,
 'verbose'    : True
}
client = Client(options)
```

recv_speed: rate limit data download speed in Bytes per second. Defaults to unlimited speed.  
send_speed: rate limit data upload speed in Bytes per second. Defaults to unlimited speed.  
verbose:    set verbose mode on/off. By default verbose mode is off.

Also if your server does not support `check` it is possible to disable it:

```python
options = {
 ...
 'disable_check': True
}
client = Client(options)
```

By default, checking of remote resources is enabled.

For configuring chunk size of content downloading use `chunk_size` param, by default it is `65536`

```python
options = {
 ...
 'chunk_size': 65536
}
client = Client(options)
```

**Asynchronous methods**

```python
# Checking existence of the resource

await client.check("dir1/file1")
await client.check("dir1")
```

```python
# Get information about the resource

await client.info("dir1/file1")
await client.info("dir1/")
```

```python
# Check free space

free_size = await client.free()
```

```python
# Get a list of resources

files1 = await client.list()
files2 = await client.list("dir1")
files3 = await client.list("dir1", get_info=True) # returns a list of dictionaries with files details
```

```python
# Create directory

await client.mkdir("dir1/dir2")
```

```python
# Delete resource

await client.clean("dir1/dir2")
```

```python
# Copy resource

await client.copy(remote_path_from="dir1/file1", remote_path_to="dir2/file1")
await client.copy(remote_path_from="dir2", remote_path_to="dir3")
```

```python
# Move resource

await client.move(remote_path_from="dir1/file1", remote_path_to="dir2/file1")
await client.move(remote_path_from="dir2", remote_path_to="dir3")
```

```python
# Download a resource

await client.download(remote_path="dir1/file1", local_path="~/Downloads/file1")
await client.download(remote_path="dir1/dir2/", local_path="~/Downloads/dir2/")
```

```python
# Upload resource

await client.upload(remote_path="dir1/file1", local_path="~/Documents/file1")
await client.upload(remote_path="dir1/dir2/", local_path="~/Documents/dir2/")
```

```python
# Publish the resource

link = await client.publish("dir1/file1")
link = await client.publish("dir2")
```

```python
# Unpublish resource

await client.unpublish("dir1/file1")
await client.unpublish("dir2")
```

```python
# Exception handling

from aiowebdav.exceptions import WebDavException

try:
 ...
except WebDavException as exception:
...
```

```python
# Get the missing files

await client.pull(remote_directory='dir1', local_directory='~/Documents/dir1')
```

```python
# Send missing files

await client.push(remote_directory='dir1', local_directory='~/Documents/dir1')
```

```python
# Unload resource

kwargs = {
 'remote_path': "dir1/file1",
 'local_path':  "~/Downloads/file1",
 'callback':    callback
}
client.upload_async(**kwargs)

kwargs = {
 'remote_path': "dir1/dir2/",
 'local_path':  "~/Downloads/dir2/",
 'callback':    callback
}
client.upload_async(**kwargs)
```

Resource API
============

Resource API using the concept of OOP that enables cloud-level resources.

```python
# Get a resource

res1 = client.resource("dir1/file1")
```

```python
# Work with the resource

await res1.rename("file2")
await res1.move("dir1/file2")
await res1.copy("dir2/file1")
info = await res1.info()
await res1.read_from(buffer)
await res1.read(local_path="~/Documents/file1")
await res1.write_to(buffer)
await res1.write(local_path="~/Downloads/file1")

```

# For Contributors

### Prepare development environment
1. Install docker on your development machine
1. Start WebDAV server for testing by following commands from the project's root folder or change path to `conf` dir in second command to correct:
```shell script
docker pull bytemark/webdav
docker run -d --name webdav -e AUTH_TYPE=Basic -e USERNAME=alice -e PASSWORD=secret1234 -v conf:/usr/local/apache2/conf -p 8585:80 bytemark/webdav
``` 

### Code convention

Please check your code according PEP8 Style guides.

### Run tests
1. Check that webdav container is started on your local machine
1. Execute following command in the project's root folder:
```shell script
python -m unittest discover -s tests
```

### Prepare a Pull Request

Please use this check list before creating PR:
1. You code should be formatted according PEP8
1. All tests should successfully pass
1. Your changes shouldn't change previous default behaviour, exclude defects
1. All changes are covered by tests 
