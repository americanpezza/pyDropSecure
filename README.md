pyDropSecure
============

### Introduction
This is a simple encryption wrapper around the Dropbox API. The goal of the project is to offer a way of uploading
encrypted files as seamlessly as possible. This is done by attempting to replicate the official Dropbox client which
syncs all the files in a targeted folder. The encryption algorithm used is AES-128 with a HMAC applied to ensure message
integrity.

**NOTE** This project is a result of a week of hacking around on my free time. I offer no guarantees about the strength 
of the encryption. Use it at your own risk.

### Setup

The current setup method is very clunky as this project is very much in development mode. I will streamline the process 
in the near future.

1. Rename `src/settings_template.py` to `src/settings.py`
2. Register a new application with Dropbox and obtain the application key and secret.
3. Modify the `APP_KEY` and `APP_SECRET` parameters in `src/settings.py` accordingly.
4. Run `src/configure.py` and follow the instructions.

If you want to setup sync on another machine, manually create `~/DropSecure` and `~/.dropsecure` yourself. Next, copy 
the `~/.dropsecure/config.db` file from the machine you originally performed the setup on to the `~/.dropsecure` directory
you created. Again, this is very much in development mode. I **will** streamline the process in the near future.

### Credits

https://github.com/ldx/DBdownload - I based my syncing code around this excellent project while rewriting a portion of it
                                    to fit my coding style better as well as implementing upload functionality.
                                    
http://code.activestate.com/recipes/576980-authenticated-encryption-with-pycrypto/ - My encryption code is based on this
very handy little snippet. I modified it to use a 128 bit key instead of 192 bit key.
