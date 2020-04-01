# CTFdScraper

CTFdScraper is a simple scraper for automating challenges gathering from a [CTFd](https://github.com/CTFd/CTFd/) platform. Generally, it's utilizing the CTFd endpoint on `/api/v1/challenges`or `/chals`for older version.

## Getting Started

### Prerequisites

In order to run this properly, you need a `python2` or `python3` environment installed. For  a certain circumstance, `termux` user need to install several packages before installing [lxml](https://github.com/termux/termux-packages/issues/3793).

```bash
# Termux-only (lxml)
$ pkg install clang libxml2 libxslt
$ pip install cython
```

### Installation

After fulfilling the prerequisites, you can directly clone this repository or download the source from our [releases](https://github.com/hanasuru/CTFdScraper/releases).

```bash
$ git clone https://github.com/hanasuru/CTFdScraper
```

After that, go install its dependencies by using `pip`.

```bash
$ cd CTFdScraper/
$ pip install -r requirements.txt
```

## Usage

For instances, you can check helper section by passing `-h` or `--help`.

```bash
$ python ctfd.py --help
usage: ctfd.py [-h] [--data data] [--proxy proxy] [--path path]
               [--worker worker] [--scheme scheme] [--enable-cloud]
               [--override] [--no-download] [--export]
               [user] [passwd] [url]

Simple CTFd-based scraper for challenges gathering

positional arguments:
  user             Username/email
  passwd           Password
  url              CTFd platform url

optional arguments:
  -h, --help       show this help message and exit
  --data data      Populate from challs.json
  --proxy proxy    Request behind proxy server
  --path path      Target directory, default: CTF
  --worker worker  Number of threads, default: 10
  --scheme scheme  URL scheme, default: https
  --enable-cloud   Permit file download from a cloud drive, default=False
  --override       Override existed chall file
  --no-download    Don't download chall file
  --export         Export challenges directory as zip, default=False
                                                      
```
### Collect challenges by credentials

By default, you need to define `username`, `password`, and `CTFd` url respectively (use HTTPS by default).  

```bash
$ python ctfd.py user passwd https://some-domain
```

### Enable Cloud-files download

By default, this option are disabled due to file size issues where user accidentally spend most of internet quotas from downloading a large file. Otherwise, you can enable this opting by passing `--enable-cloud` argument

```bash
$ python ctfd.py user passwd https://some-domain --enable-cloud
``` 

Currently, only `Google-drive` and `Dropbox` that are supported.

As a note, the review that shows size output may be wrong (false positive) due to the usage of request.get(url, stream=True) in order to get the `Content-Length` header  

### Override existed challenges file

During CTF competition, the organizer may update the current binary/file. Unfortunately, by default `CTFdScraper` couldn't override the existed challenges file. If you insist to modify the current binary/file, you need to pass `--override` argument

```bash
$ python ctfd.py user passwd https://some-domain --override
```

### Collect challenges by existed `challs.json`

Alternatively, you can also populate only the challenges from an existed `challs.json`. Additionally, you can also combine with `--enable-cloud` & `--override` to download files from a cloud drive. Furthermore, check the [examples](./examples/CTF/Arkavidia/challs.json).

```bash
# Populate challenges only from existed data
$ python ctfd.py --data challs.json

# Populate challenges alongwith files
$ python ctfd.py user passwd https://some-domain --data chall.json

# Populate challenges alongwith interal file (if public) and external file
$ python ctfd.py --data chall.json --enable-cloud --override
```

### Enable request behind proxy

To be able to conduct a requests behind proxy you need to pass `--proxy proxy-server` argument or manually add `export http_proxy="http://host:port"`.

```bash
$ python ctfd.py user passwd https://some-domain --proxy 127.0.0.1:8080

# or set up an environtment variable
$ export http_proxy = "http://127.0.0.1:8080"
$ export https_proxy = "http://127.0.0.1:8080"
```

### Wrap up the CTFd folder into a Zip file 

For archiving purpose, you can save the `CTFd` folder as a Zip file by passing the `--export` argument

```bash
$ python ctfd.py user passwd https://some-domain --export
```

Lastly, the collected challenge will be saved to `CTF/${ctf_name}`
directory. You can customize the path by passing `--path pathname`argument.

## Examples

### Challenges Hierarchy

```bash
$ tree
.
└── Online Playground CTF for Beginner
    ├── challs.json
    ├── Cryptography
    │   ├── Base64
    │   │   └── README.md
    │   └── Single-Byte XOR Cipher
    │       └── README.md
    ├── Forensic
    │   ├── Data Exfil
    │   │   └── README.md
    │   └── Volatility 4
    │       └── README.md
    ├── Pwn
    │   ├── cariuang
    │   │   └── README.md
    │   └── vault
    │       └── README.md
    ├── Reverse
    │   ├── IFEST-password
    │   │   └── README.md
    │   └── Password
    │       └── README.md
    └── Web
        ├── babyPHP
        │   └── README.md
        └── Optimus Prime
            └── README.md
```

### Challenge README.md

```
# Optimus Prime [50 pts]

**Category:** Web
**Solves:** 23

## Description
>Optimus Prime is coming

http://18.139.8.91:3015/

author: Arkavidia5

**Hint**
* -

## Solution

### Flag
```

## Demo

For instances, here is the demonstration of CTFdScraper. For simplicity, the svg file was removed

### Scrape using credentials

```bash
▶ python ctfd.py test 12345 http://playgroundctf.xyz            
✔ Login Success
✔ Found 43 new challenges
✔ Found 24 files (0.5 MB downloaded)

[Summary]
✔ Web                           (3)
✔ Reverse                       (3)
✔ Cryptography                  (9)
✔ Forensic                      (10)
✔ Intro                         (7)
✔ Survey                        (1)
✔ Pwn                           (5)
✔ Hacktoday 2019 - Penyisihan   (5)

[Finished in 3.44 second]
```

### Scrape using cloud drive support

```bash
▶ python ctfd.py test 12345 http://playgroundctf.xyz --enable-cloud
✔ Login Success
✔ Loaded 43 challs from challs.json
⚠ There are no new challenges
✔ Found 26 files (143.0 MB downloaded)

[Summary]
✔ Web                           (3)
✔ Reverse                       (3)
✔ Cryptography                  (9)
✔ Forensic                      (10)
✔ Intro                         (7)
✔ Survey                        (1)
✔ Pwn                           (5)
✔ Hacktoday 2019 - Penyisihan   (5)

[Finished in 9.56 second]                               
```

### Scrape using existed `chall.json`

```bash
▶ python ctfd.py --data challs.json                                                       
✔ Loaded 43 challs from challs.json
✔ Found 24 files (0.0 MB downloaded)

[Summary]
✔ Web                           (3)
✔ Reverse                       (3)
✔ Cryptography                  (9)
✔ Forensic                      (10)
✔ Intro                         (7)
✔ Survey                        (1)
✔ Pwn                           (5)
✔ Hacktoday 2019 - Penyisihan   (5)

[Finished in 0.09 second]
                                         
```

## Authors

* **hanasuru** - *Initial work* 

See also the list of [contributors](https://github.com/hanasuru/CTFdScraper/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Credits

* [CTFd](https://github.com/CTFd/CTFd), a Capture The Flag framework focusing on ease of use and customizability.
* [markdown2png](https://github.com/andrewlin12/markdown2png),  a module to render John Gruber's markdown format to `PNG` (or other image formats) by using `Pillow` and `Markdown` dependencies.