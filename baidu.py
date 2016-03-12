import httplib
import json
import re
import sys
import subprocess
import urllib2
import time
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')
from lxml import etree
from select import select
reponse = urllib2.urlopen("http://music.baidu.com/songlist")
html = reponse.read()
reponse.close()
tree=etree.HTML(html)
ids =tree.xpath("//a[@sid]/@sid")
names = tree.xpath("//a[@sid]/@title")
url = "http://music.baidu.com/data/music/fmlink?type=mp3&rate=320&songIds="
#for td in names:
#    print td
def control():
        rlist, _, _ = select([sys.stdin], [], [], 1)
        if rlist:
            s = sys.stdin.readline()
            if s[0] == 'n':
                return 'next'
            elif s[0] == 'p':
                return 'prev'

def start(i):
    while i < len(ids):
        playmode = True
        print(names[i])
        reponses = urllib2.urlopen(url+ids[i])
        htmls = reponses.read()
        song = json.loads(htmls)
        song = song['data']
        song = song['songList']
        song = song[0]
#        print song
#       print song['queryId']
        durations = song['time']
        starttime = time.time()
        player = subprocess.Popen(['mpg123', '-v',song['songLink']], shell=False, universal_newlines=True, stdin=None,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while playmode:
            c = control()
            endtime = time.time()
            usetime = endtime - starttime - durations
            if c == 'next' or usetime > 2:
                player.kill()
                i = i + 1
                break
            elif c == 'prev':
                player.kill()
                i = i - 1
                break
#d = u ''' '''


print "next n preview p"
while 1:
    y=0
    start(y)