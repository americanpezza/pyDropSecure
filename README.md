pyDropSecure
============

### Introduction
This is a simple encryption wrapper around the Dropbox API. The goal of the project is to offer a way of uploading
encrypted files as seamlessly as possible. This is done by attempting to replicate the official Dropbox client which
syncs all the files in a targeted folder. The encryption algorithm used is AES-128 with a HMAC applied to ensure message
integrity.

**NOTE** This project is a result of a week of hacking around on my free time. I offer no guarantees about the strength 
of the encryption. Use it at your own risk.

### Supported Operating Systems

This script has been developed on a Fedora 19 system. It should work well for all Linux and UNIX-based distributions.
Unfortunately, Windows is currently not supported. Version 2.0 perhaps. 

### Setup

1. Install `pip` from your distribution's package manager. On RHEL-based distributions this is done through 
   `yum install python -pip`
2. Install the required dependencies using `pip install -r requirements.txt`. 
2. Rename `src/settings_template.py` to `src/settings.py`
3. Go to https://www.dropbox.com/developers/apps/create and create a new application. Here are the options you will 
   need to select
   1. What type of app do you want to create? - Dropbox API app
   2. What type of data does your app need to store on Dropbox? - Files and datastores
   3. Can your app be limited to its own, private folder? - Yes My app only needs access to files it creates.
4. Modify the `APP_KEY` and `APP_SECRET` parameters in `src/settings.py` to reflect the key and secret Dropbox 
   provided for your own app.
5. Run `./src/dropsecure.py --configure`

### Usage

The help option is pretty self explanatory.

```
$ ./src/dropsecure.py -h
usage: dropsecure.py [-h]
                     (--start | --stop | --restart | --export EXPORT | --import IMP | --configure)

optional arguments:
  -h, --help       show this help message and exit
  --start          Start the script
  --stop           Stop the script
  --restart        Restart the script
  --export EXPORT  Export application keys
  --import IMP     Import application keys
  --configure      Configure the application
```

### License

```
The MIT License (MIT)

Copyright (c) 2013 Terry Chia

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

### Credits

https://github.com/ldx/DBdownload - I based my syncing code around this excellent project while rewriting a portion of it
                                    to fit my coding style better as well as implementing upload functionality.
                                    
http://code.activestate.com/recipes/576980-authenticated-encryption-with-pycrypto/ - My encryption code is based on this
very handy little snippet. I modified it to use a 128 bit key instead of 192 bit key.
