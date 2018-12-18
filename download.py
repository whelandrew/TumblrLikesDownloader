# Created by Andrew Whelan
# 12/08/2018
# Access tumblr likes list and download them to local harddrive

import pytumblr
import os
import os.path
import urllib
import urllib.request
import urllib.error
import re
import threading
from tumblr_keys import *

client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    token_key,
    token_secret
)

def media_download(mylikes, dirname, client):
    if 'posts' in mylikes:
           for i in range(0, len(mylikes['my_posts'])):
               like = mylikes['my_posts'][i]
               if 'photo' in like['type']:
                   print('IMAGE ', like, "\n")
                   for j in range(0, len(like['photos'])):
                       url = like['photos'][j]['original_size']['url']
                       name = re.findall(r'tumblr_\w+.\w+', url)
                       urllib.request.urlretrieve(url, dirname + '/' + name[0])
                       client.unlike(like['id'], like['reblog_key'])
                       print('[' + str(i+1) + ':' + str(len(like)) + ']')
               elif like['type'] == 'video':
                   print('VIDEO ', like, "\n")
                   if True in ['trail']['blog']['active']:
                       url = like['video_url']
                       name = re.findall(r'tumblr_\w+.\w+', url)
                       urllib.request.urlretrieve(url, dirname + '/' + name[0])
                       client.unlike(like['id'], like['reblog_key'])
               elif like['type'] == 'text':
                   print('OTHER ', like, "\n")
                   url = like['post_url']
                   name=re.findall(r'tumblr_\w+.\w+', url)
                   urllib.request.urlretrieve(url, dirname + '/' + like['blog_name'])
                   client.unlike(like['id'], like['reblog_key'])
               else:
                   print('[' + str(i+1) + ':' + str(len(mylikes['posts'])) + ']')
    else:
        print("End")
        return 0
def main():
    print("Begin main")
    info = client.info()
    print(info,"\n")

    if 'errors' in info:
        print(info['errors'])
        
    else:
        dirname = info['user']['name']
        blogurl = info['user']['blogs'][0]['url']
        likescount = info['user']['likes']
        offset = 0
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        while 1:
            try:
                mylikes = client.likes(limit=20, offset=offset)
                if not mylikes:
                    print('No Likes Found')
                    return
                media_download(mylikes, dirname, client)
                offset += 20
            except urllib.error.URLError as e: 
                print(e)
                break
        list = os.listdir(dirname)
        number_files = len(list)
        print(number_files, " Files Downloaded")

if __name__ == '__main__':
    main()
    print('Done!')