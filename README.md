# prepare_dev

MS Azure furnishes a PublishSettings to faciliate uploading source/website code to a web application in the Azure App Service PaaS. This utility loads the downloaded file, extracts the necessary ftp parameters, and outputs a properly formatted `ftp` command to connect to the web app ftp site.

## Installation

Clone this repository. Install script requirements:

```bash
$ pip install -r requirements.txt.
$ chmod a+x prepare_dev.py
```

## Usage

```bash
$ ./prepare_dev.py [path/to/*.PublishSettings]
```
