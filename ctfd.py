from cfscrape import *
from requests import session
from bs4 import BeautifulSoup
import json, os, requests, re,sys

class CTFdCrawl:
    def __init__(self, basedir, team, passwd, url):
        self.auth      = dict(name=team, password=passwd)
        self.header = {'User-Agent' : 'curl/7.37.0'}
        self.ses       = session()
        self.entry     = dict()
        self.keys      = 'data'
        self.url       = url
        self.basedir   = basedir
        self.ch_url    = self.url + '/api/v1/challenges'
        self.hi_url    = self.url + '/api/v1/hints'

        if not self.login():
            raise Exception('Login Failed')
        print('\n[+] Collecting resources')
        self.checkVersion()

    def login(self):
        resp  = self.ses.get(self.url + '/login', headers=self.header)
        soup  = BeautifulSoup(resp.text,'lxml')
        nonce = soup.find('input', {'name':'nonce'}).get('value')
        
        self.auth['nonce'] = nonce
        self.title = soup.title.string

        resp  = self.ses.post(self.url + '/login', data=self.auth, headers=self.header)
        return 'incorrect' not in resp.text
    def checkVersion(self):
        resp = self.ses.get(self.ch_url, headers=self.header)
        self.version = 'v.1.2.0' if '404' not in resp.text else 'v.1.0'
        
    def antiCloudflare(self, page):
        scrape = create_scraper()
        tokens = get_tokens('{}/{}'.format(self.URL, page))
        return tokens

    def parseChall(self, id):
        r = self.ses.get('{}/{}'.format(self.ch_url,id), headers=self.header)
        if sys.version_info.major == 2:
            return json.loads(r.text.decode('utf-8'))['data'] if self.version == 'v.1.2.0' else json.loads(r.text.decode('utf-8'))
        else:
            return json.loads(r.text)['data'] if self.version == 'v.1.2.0' else json.loads(r.text)

    def createReadme(self, cate, name, data):
        tmp  = "# {} [{} pts]\n\n".format(name, data['Points'])
        tmp += "## Category\n{}\n\n".format(cate)
        if sys.version_info.major == 2:
            tmp += "## Description\n>{}\n\n".format(data['Description'].encode('utf-8').replace('\n', '\n>').strip())
        else:
            tmp += "## Description\n>{}\n\n".format(data['Description'].replace('\n', '\n>').strip())
        tmp += "### Hint\n>{}\n\n".format(''.join(data['Hint'].replace('\n', '\n>')))
        tmp += "## Solution\n1.\n\n"
        tmp += "### Flag\n`Flag`\n"
        return tmp

    def parseAll(self):
        print ('[+] Finding challs')
        if self.version == 'v.1.0':
            self.ch_url = self.url + '/chals'
            self.hi_url = self.url + '/hints'
            self.keys   = 'game'
        html  = self.ses.get(self.ch_url, headers=self.header)
        if sys.version_info.major == 2:
            data  = sorted(json.loads(html.text)[self.keys])
        else:
            data  = json.loads(html.text)[self.keys]
            data.sort(key=lambda s: (s['category'], s['name']))
        ids       = [i['id'] for i in data]

        for id in ids:
            data    = self.parseChall(id)
            ch_name = data['name']
            ch_cat  = data['category']

            if not self.entry.get(ch_cat):
                self.entry[ch_cat] = {}
                count = 1
                print ('\n[v][No] ' + ch_cat)

            if sys.version_info.major == 2:
                print ('    {:02d}. {}'.format(count, ch_name.encode('utf-8')))
            else:
                print ('    {:02d}. {}'.format(count, ch_name))
                

            entries = {ch_name : {
              'ID'          : data['id'],
              'Points'      : data['value'],
              'Description' : data['description'],
              'Files'       : data['files'],
              'Hint'        : ''#data['hints']
             }
            }
            
            self.entry[ch_cat].update(entries)
            count += 1
         
    def createArchive(self):
        print ('\n[+] Downloading assets . . .')
        if not os.path.exists(self.basedir+self.title):
            os.makedirs(self.basedir+self.title)

        os.chdir(self.basedir+self.title)
        with open('challs.json','wb') as f:
            if sys.version_info.major == 2:
                f.write(json.dumps(self.entry ,sort_keys=True, indent=4))
            else:
                f.write(bytes(json.dumps(self.entry ,sort_keys=True, indent=4).encode()))

        r = re.compile("[^A-Za-z0-9 .\'_-]")

        if sys.version_info.major == 2:
            entry_items = self.entry.iteritems()
        else:
            entry_items = self.entry.items()
            
        for key, val in entry_items:
            if sys.version_info.major == 2:
                val_items = val.iteritems()
            else:
                val_items = val.items()
                
            for keys, vals in val_items:
                keys      = r.sub('',keys.strip())
                directory = '{}/{}'.format(key,keys)
                directory = directory.replace(' / ','-')
                while directory[-1] == ' ':
                    directory = directory[:-1]
                print ('    Directory '+directory+' has been created')
                if not os.path.exists(directory):
                    os.makedirs(directory)
                if not os.path.exists('{}/README.md'.format(directory)):
                    with open('{}/README.md'.format(directory),'wb') as f:
                        readme_tmp = self.createReadme(key, keys, vals)
                        if sys.version_info.major == 2:
                            f.write(readme_tmp)
                        else:
                            f.write(bytes(readme_tmp.encode()))
                            
                files = vals['Files']
                if files:
                    for url_file in files:
                        if self.version == 'v.1.0':
                            filename = url_file.split('/')[1]
                        else:
                            filename = url_file.split('/')[3].split('?')[0]
                        if not os.path.exists(directory + '/' + filename):
                            if self.version == 'v.1.0':
                                resp = self.ses.get(self.url + '/files/' + url_file, stream=False)
                            else:
                                resp = self.ses.get(self.url + url_file, stream=False)
                            with open(directory + '/' + filename, 'wb') as f:
                                f.write(resp.content)
                                f.close()
        print ('\n[+] Downloaded Assets Successfully 100%')

def main():
    if len(sys.argv) > 2:
     url           = sys.argv[1]
     user          = sys.argv[2]
     passwd        = sys.argv[3]
     try:
         basedir    = sys.argv[4]
     except:
         basedir    = ''
    else:
        if sys.version_info.major == 2:
            url    = raw_input('CTFd URL : ')
            user   = raw_input('Username : ')
            passwd = raw_input('Password : ')
            basedir = raw_input('Output (this dir input blank)  : ')
        else:
            url    = input('CTFd URL : ')
            user   = input('Username : ')
            passwd = input('Password : ')
            basedir = input('Output (this dir input blank)  : ')
    if basedir.replace(' ', '') == '':
        basedir = '.'
    ctf            = CTFdCrawl(basedir+'/', user,passwd,url)    
    ctf.parseAll()
    ctf.createArchive()    

if __name__ == '__main__':
    main()
