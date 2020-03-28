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

After fulfilling the prerequisites, you can directly clone this repository or download the source from our [releases](https://github.com/eiji98/CTFdScraper/releases).

```bash
$ git clone https://github.com/eiji98/CTFdScraper
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
usage: ctfd.py [-h] [--data data] [--path path] [--worker worker]
               [--scheme scheme] [--override] [--no-download]
               [user] [passwd] [url]

Simple CTFd-based scraper for challenges gathering

positional arguments:
  user             Username/email
  passwd           User password
  url              CTFd platform url

optional arguments:
  -h, --help       show this help message and exit
  --data data      Populate from chall.json
  --path path      Target directory, default: CTF
  --worker worker  Number of threads, default: 3
  --scheme scheme  URL scheme, default: https
  --override       Overrides old chall file
  --no-download    Don't download chall assets
                                                      
```
### Collect challenges

By default, you need to define `username`, `password`, and `CTFd` url respectively (use HTTPS by default).  

```bash
$ python ctfd.py user passwd https://some-domain
```

Alternatively, you can also populate only the challenges from an existed `challs.json`. Unfortunately, you need to pass `username` & `password` in order to download the [internal files](https://github.com/CTFd/CTFd/issues/789) . Furthermore, check the [examples](./examples/CTF/challs.json).

```bash
# Populate challenges only from existed data
$ python2 ctfd.py --data challs.json

# Populate challenges alongwith files
$ python ctfd.py user passwd https://some-domain --data chall.json
```

Lastly, the collected challenge will be saved to `CTF/${ctf_name}`
directory. You can customize the path by passing `--path pathname`argument.

## Examples

### Challenges Hierarchy

```bash
$ tree
.
├── challs.json
├── Crypto
│   ├── 007-1
│   │   ├── chall.zip
│   │   └── README.md
│   └── Simple Math
│       ├── chall.zip
│       └── README.md
└── Web
   ├── ArkavPay
   │   ├── ArkavPay.zip
   │   └── README.md
   ├── Balasan Buruk
   │   └── README.md
   └── Edit Your Source
       └── README.md
```

### Challenge README

```
# Balasan Buruk [344 pts]

**Category:** Web
**Solves:** 23

## Description
>Saya baru saja belajar mata kuliah Jaringan Komputer, sebagai Tugas Besar, saya ditugaskan untuk membuat HTTP server sederhana tanpa menggunakan library HTTP apapun.

`http://3.0.19.78:15001`

Author: didithilmy

**Hint**
* 

## Solution

### Flag
```


## Demo

For instances, here is the demonstration of CTFdScraper.

![Alt text](demo.svg)


## Authors

* **eiji98** - *Initial work* 
See also the list of [contributors](https://github.com/eiji98/CTFdScraper/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Credits

* [CTFd](https://github.com/CTFd/CTFd), a Capture The Flag framework focusing on ease of use and customizability.
* [markdown2png](https://github.com/andrewlin12/markdown2png),  a module to render John Gruber's markdown format to `PNG` (or other image formats) by using `Pillow` and `Markdown` dependencies.