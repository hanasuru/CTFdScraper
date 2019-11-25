#!/usr/bin/env python2
from itertools import izip_longest as iz
from threading import Thread, Lock
from requests import session
from bs4 import BeautifulSoup
import json, os, requests, re,sys

class CTFdScrape(object):
    def __init__(self, team, passwd, url):
        self.auth   = dict(name=team, password=passwd)
        self.url    = url
        self.defineVar()
        # Login Handle
        if not self.login():
            raise Exception('Login Failed')
        print '\n[+] Collecting resources'
        self.checkVersion()
        # Create Folder
        if not os.path.exists(self.title):
            os.makedirs(self.title)
        os.chdir(self.title)

    def defineVar(self):
        # CTFd params
        self.keys    = 'data'
        self.version = 'v.1.0'
        self.entry   = dict(url=self.url, data={})
        # Persistent session
        self.ses     = session()
        self.ses.headers.update({'User-Agent' : 'curl/7.37.0'})
        # CTFd Endpoint
        self.ch_url  = self.url + '/api/v1/challenges'
        self.hi_url  = self.url + '/api/v1/hints'
        self.lg_url  = self.url + '/login'

    def login(self):
        resp  = self.ses.get(self.lg_url)
        soup  = BeautifulSoup(resp.text,'lxml')
        nonce = soup.find('input', {'name':'nonce'}).get('value')

        self.auth['nonce'] = nonce
        self.title = soup.title.string

        resp  = self.ses.post(self.lg_url, data=self.auth)
        return 'incorrect' not in resp.text

    def checkVersion(self):
        resp = self.ses.get(self.ch_url)
        if '404' in resp.text:
            self.keys    = 'game'
            self.version = 'v.1.2.0'
            self.ch_url  = self.url + '/chals'
            self.hi_url  = self.url + '/hints'

    def getChall(self, id):
        resp = self.ses.get('%s/%s' % (self.ch_url,id)).json()
        if self.version != 'v.1.2.0':
            self.parseData(resp['data'])
            return resp['data']
        return resp

    def parseData(self, data):
        entry = {
            'id'          : data['id'],
            'name'        : data['name'],
            'points'      : data['value'],
            'description' : data['description'],
            'files'       : data['files'],
            'category'    : data['category'],
            'hint'        : '' # not implemented
        }
        return self.createArchive(entry)

    def getChalls(self):
        print '[+] Finding challs'
        challs = self.ses.get(self.ch_url).json()[self.keys]
        lists  = dict()

        for ch in sorted(challs):
            genre = ch['category']
            chall = lists.get(genre, list())
 
            if not chall:
                print '\n [v]', genre
                lists[genre] = chall
                count = 1
            print '  %s. %s' %(count, ch['name'])
            chall.append(ch['id'])
            count += 1
        # Get id foreach category
        challs = [list(filter(None,i)) for i in iz(*lists.values())]
        # Archiving files
        print '\n[+] Downloading assets . . .'
        self.challThreader(challs)
        # Archiving json file
        with open('challs.json','wb') as f:
            f.write(json.dumps(self.entry ,sort_keys=True, indent=4))

    def createArchive(self, content):
        for key,val in content.items():
            exec(key+'=val')
        
        path = '%s/%s [%s pts]' % (category,name,points)
        path = path.replace(' / ','-')
        
        if os.path.exists(path.split(' [')[0]):
            os.rename(path, path)
        else:
            os.makedirs(path)

        with open('%s/README.md' % (path),'wb') as f:
            desc = description.encode('utf-8').strip()
            f.write('Description:\n{}'.format(desc))
        
        for i in files:
            url = re.search(r'(\/files\/)?([a-f0-9]*\/\w*\.*\w*)', i).group(2)
            filename = url.split('/')[-1]

            if not os.path.exists(path + '/' + filename):
               resp = self.ses.get(self.url + '/files/' + url, stream=False)
               with open(path + '/' + filename, 'wb') as f:
                f.write(resp.content)
                f.close()  
        
        print 'Directory', path,'has been created'
        data = self.entry['data'].get(category, list())
        if not data:
            self.entry['data'][category] = data
        data.append(content)

    def startThread(self, id, lock=None):
        self.getChall(id)

    def challThreader(self, challs):
        self.lock = []
        self.thrd = []
        for i in challs:
            for _ in i:
                self.thrd.append(Thread(target=self.startThread, args=(_, self.lock)))
                self.thrd[-1].start()
            [i.join() for i in self.thrd]

def main():
    url    = sys.argv[1]
    user   = sys.argv[2]
    passwd = sys.argv[3]
    
    ctf = CTFdScrape(user,passwd,url)
    ctf.getChalls()

if __name__ == '__main__':
    main()