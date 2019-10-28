from cfscrape import *
from requests import session
from bs4 import BeautifulSoup
import json, os, requests, re,sys

class CTFdCrawl:
    def __init__(self, team, passwd, url):
        self.auth  = dict(name=team, password=passwd)
        self.ses   = session()
        self.entry = dict()
        self.url   = url

        if not self.login():
            raise Exception('Login Failed')
        print '\n[+] Collecting resources'

    def login(self):
        resp  = self.ses.get(self.url + '/login')
        soup  = BeautifulSoup(resp.text,'lxml')
        nonce = soup.find('input', {'name':'nonce'}).get('value')
        
        self.auth['nonce'] = nonce
        self.title = soup.title.string

        resp  = self.ses.post(self.url + '/login', data=self.auth)
        return 'incorrect' not in resp.text

    def antiCloudflare(self, page):
        scrape = create_scraper()
        tokens = get_tokens('{}/{}'.format(self.URL, page))
        return tokens

    def parseChall(self, id):
        r = self.ses.get('{}/api/v1/challenges/{}'.format(self.url,id))
        return json.loads(r.text.decode('utf-8'))['data']

    def parseAll(self):
        print '[+] Finding challs',
        html  = self.ses.get(self.url + '/api/v1/challenges')
        data  = sorted(json.loads(html.text)['data'])
        ids   = [i['id'] for i in data]

        for id in ids:
            data    = self.parseChall(id)
            ch_name = data['name']
            ch_cat  = data['category']

            if not self.entry.get(ch_cat):
                self.entry[ch_cat] = {}
                count = 1
                print
                print ' [v]', ch_cat

            print '  {}. {}'.format(count, ch_name)

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

                rr = re.compile(r'\/*[a-f0-9]*\/\w*\.*\w*')
                files = vals['Files']
                if files:
                    for i in files:
                        i = ''.join(rr.findall(i))
                        filename = i.split('/')[1]
                        if not os.path.exists(directory + '/' + filename):
                            # print self.url + '/files/' + i
                            resp = self.ses.get(self.url + '/files/' + i, stream=False)
                            with open(directory + '/' + filename, 'wb') as f:
                                f.write(resp.content)
                                f.close()

def main():
    if len(sys.argv) > 1:
     url    = sys.argv[1]#raw_input('CTFd URL : ')
     user   = sys.argv[2]#raw_input('Username : ')
     passwd = sys.argv[3]#raw_input('Password : ')
    else:
     url    = raw_input('CTFd URL : ')
     user   = raw_input('Username : ')
     passwd = raw_input('Password : ')
    ctf    = CTFdCrawl(user,passwd,url)    
    ctf.parseAll()
    ctf.createArchive()    

if __name__ == '__main__':
    main()
