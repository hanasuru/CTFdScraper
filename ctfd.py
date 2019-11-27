#!/usr/bin/env python2
from threading import Thread, Lock
from progress.bar import IncrementalBar
from requests import session
from bs4 import BeautifulSoup
import json, os, requests, re,sys, time

class CTFdScrape(object):
    def __init__(self, team, passwd, url):
        self.auth   = dict(name=team, password=passwd)
        self.url    = url
        self.defineVar()
        
        # Login Handle
        print '\n+ Authenticating'
        if not self.login():
            raise Exception('- Login Failed')
        self.manageVersion()
        
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
        # Regex Rule
        self.regex   = re.compile(r'(\/files\/)?([a-f0-9]*\/\w*\.*\w*)')
        # Other
        self.dlSize  = 0
        self.chcount = 0
        self.chfiles = 0
        self.starTim = time.time()

    def login(self):
        resp  = self.ses.get(self.lg_url)
        soup  = BeautifulSoup(resp.text,'lxml')
        nonce = soup.find('input', {'name':'nonce'}).get('value')

        self.auth['nonce'] = nonce
        self.title = soup.title.string

        resp  = self.ses.post(self.lg_url, data=self.auth)
        return 'incorrect' not in resp.text

    def manageVersion(self):
        resp = self.ses.get(self.ch_url)
        if '404' in resp.text:
            self.keys    = 'game'
            self.version = 'v.1.2.0'
            self.ch_url  = self.url + '/chals'
            self.hi_url  = self.url + '/hints'

    def getHintById(self, id):
        resp = self.ses.get('%s/%s' % (self.hi_url,id)).json()
        return resp['data']['content']

    def getHints(self, data):
        res = [] 
        for hint in data:
            if hint['cost'] == 0:
                if self.version != 'v.1.2.0':
                    res.append(self.getHintById(hint['id']))
                else:
                    res.append(hint['hint'])
        return res

    def getChallById(self, id, lock=None):
        if self.version != 'v.1.2.0':
            resp = self.ses.get('%s/%s' % (self.ch_url,id)).json()
            self.parseData(resp['data'])
        else:
            self.parseData(self.c[id])

    def parseData(self, data):
        entry = {
            'id'          : data['id'],
            'name'        : data['name'],
            'points'      : data['value'],
            'description' : data['description'],
            'files'       : data['files'],
            'category'    : data['category'],
            'hints'       : self.getHints(data['hints']) # not checked yet
        }
        # print json.dumps(entry ,sort_keys=True, indent=4)
        self.chcount += 1
        self.createArchive(entry)

    def getChalls(self):
        print '+ Collecting challs'
        challs = self.ses.get(self.ch_url).json()[self.keys]
        lists  = dict()
        self.c = dict() # v.1.2.0 only

        for ch in sorted(challs):
            genre = ch['category']
            chall = lists.get(genre, list()) 
            if not chall:
                print '\n [v]', genre
                lists[genre] = chall
                count = 1
            print '  %s. %s' %(count, ch['name'])
            chall.append(ch['id'])
            self.c.update({ch['id'] : ch})
            count += 1

        # Archiving files
        print '\n+ Downloading Assets'
        self.challThreader(lists)
        
        # Archiving json file
        with open('challs.json','wb') as f:
            f.write(json.dumps(self.entry ,sort_keys=True, indent=4))

        # Show report
        print '\n+ Total challs : {}'.format(self.chcount)
        print '+ Downloaded file : {}'.format(self.chfiles)
        print '+ Downloaded size : {0:.2f} KB'.format(self.dlSize/1000)
        print '\n+ Finished in {0:.2f} second'.format(time.time() - self.starTim)

    def createArchive(self, content):
        for key,val in content.items():
            exec(key+'=val')

        path = '%s/%s' % (category,name)
        path = path.replace(' / ','-')
        
        if not os.path.exists(path):
            os.makedirs(path)

            for i in files:
                url = self.regex.search(i).group(2)
                filename = url.split('/')[-1]
                while 1:
                    try:
                      resp = self.ses.get(self.url + '/files/' + url, stream=True)
                      break
                    except:
                      pass

                with open(path + '/' + filename, 'wb') as handle:
                    for chunk in resp.iter_content(chunk_size=512):
                        if chunk:
                            handle.write(chunk)
                self.dlSize  += int(resp.headers.get('Content-Length', 0))
                self.chfiles += 1
      
        with open('%s/README.md' % (path),'wb') as f:
            desc = description.encode('utf-8').strip()
            name = name.encode('utf-8').strip()
            f.write('# %s [%s pts]\n\n' % (name, points))
            f.write('## Category\n%s\n\n' % (category))
            f.write('## Description\n>%s\n\n' % (desc))
            f.write('### Hint\n>%s\n\n' % ('\n>'.join(hints)))
            f.write('## Solution\n\n\n')
            f.write('### Flag\n\n')

        data = self.entry['data'].get(category, list())
        if not data:
            self.entry['data'][category] = data
        data.append(content)
        self.bar.next()

    def startThread(self, threads, msg):
        self.bar  = IncrementalBar('  {0:<19}'.format(msg),\
                    max=len(threads), suffix='%(percent)d%%')
        
        [i.start() for i in threads]
        [i.join() for i in threads]
        self.bar.finish()

    def challThreader(self, challs):
        for msg,val in challs.iteritems():
            lock   = []
            threads = []            
            for i in val:
                threads.append(Thread(target=self.getChallById, args=(i, lock)))
            self.startThread(threads, msg)

def main():
    if len(sys.argv) > 1:
        url     = sys.argv[1]
        user    = sys.argv[2]
        passwd  = sys.argv[3]
    
        ctf = CTFdScrape(user,passwd,url)
        ctf.getChalls()
    else:
        print 'Usage: python2', sys.argv[0], '<url> <user> <passwd>'

if __name__ == '__main__':
    main()