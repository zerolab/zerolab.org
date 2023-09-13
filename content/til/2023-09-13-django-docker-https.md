---
title: "Django over HTTPS in local Docker"
date: "2023-09-13 22:57:13.07777 +0100 BST m=+0.056481584"
tags: ["Django", "Docker"]
---

I needed to test a local build over HTTPS due SSO requirements in the past, and [Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) more recently.


The project(s) have the following layout:

```
. 
└── Project root/ 
│   ├── docker/ 
│   │   ├── Procfile 
│   │   └── other-docker-related-files 
│   ├── the_project/ 
│   ├── Dockerfile 
│   └── docker-compose.yaml
│   ...
```

Where `Procfile` is for [honcho](https://pypi.org/project/honcho/). A [Procfile](https://devcenter.heroku.com/articles/procfile) specifies
commands that are executed on startup by an app that supports it and uses a `<process type>: <command>` format:

```Procfile
web: python manage.py runserver 0.0.0.0:8000
```

On my host:

1. Install [mkcert](https://github.com/FiloSottile/mkcert)
2. Generate a new self-signed certificate
   
```bash
cd <path/to/project/>docker

mkcert -cert-file dev-cert.pem -key-file dev-key.pem localhost 127.0.0.1 my-project.local
```
	
3. Run `mkcert -install` from the `docker/` directory which contains the self-signed certificate (`dev-cert.pem` and `dev-key.pem`)
4. (optional) Create a `Procfile_https` file with
   
    ```Procfile
    web: python manage.py runserver_plus 0.0.0.0:8000 --cert-file docker/dev-cert.pem --key-file docker/dev-key.pem --keep-meta-shutdown  
    ```

5. In your web container:
	* if you use honcho and created `Procfile_https`, use `honcho_https run` instead of `honcho run`
	* if running `runserver` directly, then run `python manage.py runserver_plus 0.0.0.0:8000 --cert-file docker/dev-cert.pem --key-file docker/dev-key.pem --keep-meta-shutdown`

7. Access the site at `https://my-site.local:8000`

   _Note: add this domain to your local `hosts` file, if it's not there already_
