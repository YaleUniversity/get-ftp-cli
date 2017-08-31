# get_ftp_cli

MS Azure furnishes a PublishSettings to faciliate uploading source/website code to a web application in the Azure App Service PaaS. This utility loads the downloaded file, extracts the necessary ftp parameters, and outputs a properly formatted `ftp` command to connect to the web app ftp site.

## Installation

Clone this repository. Install script requirements:

```bash
$ pip install -r requirements.txt.
$ chmod a+x get_ftp_cli.py
```

## Usage

```bash
$ ./get_ftp_cli.py [path/to/*.PublishSettings]
```
