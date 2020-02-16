### Simple CTFd Scrapper for challenges gathering & archiving

#### Install Dependencies
```bash
$ pip install -r requirements.txt
```
#### Usage
```bash
$ python2 ctfd.py -h
usage: ctfd.py [-h] [--path path] [--worker worker] [--scheme scheme]
               [--override] [--no-download]
               url user passwd

Simple CTFd-based scraper for challenges gathering

positional arguments:
  url              CTFd platform url
  user             Username/email
  passwd           User password

optional arguments:
  -h, --help       show this help message and exit
  --path path      Target directory
  --worker worker  Number of threads
  --scheme scheme  URL scheme, default: https
  --override       Overrides old chall file
  --no-download    Don't download chall assets

```

#### Example
![Alt text](./demo.svg)
