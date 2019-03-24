from cfscrape import *
from requests import session
from bs4 import BeautifulSoup
import json, os, requests, re,sys

class CTFdCrawl:
    def __init__(self, team, passwd, url):
        self.auth   = dict(name=team, password=passwd)
        self.ses    = session()
        self.entry  = dict()
        self.keys   = 'data'
        self.url    = url
        self.ch_url = self.url + '/api/v1/challenges'

        if not self.login():
            raise Exception('Login Failed')
        print '\n[+] Collecting resources'
        self.checkVersion()

    def login(self):
        resp  = self.ses.get(self.url + '/login')
        soup  = BeautifulSoup(resp.text,'lxml')
        nonce = soup.find('input', {'name':'nonce'}).get('value')
        
        self.auth['nonce'] = nonce
        self.title = soup.title.string

        resp  = self.ses.post(self.url + '/login', data=self.auth)
        return 'incorrect' not in resp.text

    def checkVersion(self):
        resp = self.ses.get(self.ch_url)
        self.version = 'v.1.2.0' if '404' not in resp.text else 'v.1.0'

    def antiCloudflare(self, page):
        scrape = create_scraper()
        tokens = get_tokens('{}/{}'.format(self.URL, page))
        return tokens

    def parseChall(self, id):
        resp = self.ses.get('{}/{}'.format(self.ch_url,id)).json()
        return resp['data'] if self.version == 'v.1.2.0' else resp

    def parseAll(self):
        print '[+] Finding challs'
        if self.version == 'v.1.0':
            self.ch_url = self.url + '/chals'
            self.keys   = 'game'
        html  = sorted(self.ses.get(self.ch_url).json()[self.keys])
        ids   = [i['id'] for i in html]

        for id in ids:
            data    = self.parseChall(id)
            ch_name = data['name']
            ch_cat  = data['category'] if data['category'] else 'Uncategorized' 

            if not self.entry.get(ch_cat):
                self.entry[ch_cat] = {}
                count = 1
                print '\n [v]', ch_cat
            print '  {}. {}'.format(count, ch_name)

            entries = {ch_name : {
              'ID'          : data['id'],
              'Points'      : data['value'],
              'Description' : data['description'],
              'Files'       : data['files'],
              'Hint'        : data['hints']
             }
            }
            
            self.entry[ch_cat].update(entries)
            count += 1
         
    def createArchive(self):
        print '\n[+] Downloading assets . . .'
        if not os.path.exists(self.title):
            os.makedirs(self.title)

        os.chdir(self.title)
        with open('challs.json','wb') as f:
            f.write(json.dumps(self.entry ,sort_keys=True, indent=4))

        r = re.compile("[^A-Za-z0-9 .\'_-]")
        for key, val in self.entry.iteritems():
            for keys, vals in val.iteritems():
                keys      = r.sub('',keys.strip())
                directory = '{}/{} [{} pts]'.format(key,keys,vals['Points'])
                directory = directory.replace(' / ','-')
                print 'Directory', directory,'has been created'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open('{}/README.md'.format(directory),'wb') as f:
                    desc = vals['Description'].encode('utf-8').strip()
                    f.write('Description:\n{}'.format(desc))
                    f.write('\n\nHint:\n{}'.format(''.join(vals['Hint'])))

                files = vals['Files']
                if files:
                    for i in files:
                        filename = i.split('/')[1]
                        if not os.path.exists(directory + '/' + filename):
                            resp = self.ses.get(self.url + '/files/' + i, stream=False)
                            with open(directory + '/' + filename, 'wb') as f:
                                f.write(resp.content)
                                f.close()

def main():
    url    = raw_input('CTFd URL : ')
    user   = raw_input('Username : ')
    passwd = raw_input('Password : ')
    ctf    = CTFdCrawl(user,passwd,url)
    ctf.parseAll()
    ctf.createArchive()    

if __name__ == '__main__':
    main()