#!/usr/bin/python3
#coding=utf-8

import re
import os
import bs4
import time
import json
import pytube
import requests

from pytube import exceptions
from urllib.parse import urlparse
from urllib.parse import unquote

ua = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"

for i in ['/video','/video/YouTube','/video/Facebook','/video/Instagram','/video/XNXX','/video/Like','/video/Snack Video']:
  try:
    os.mkdir('/sdcard'+i)
  except FileExistsError:
    pass

def File_size(path):
  if os.path.isfile(path):
    byte = os.stat(path).st_size
    for i in ['B','KB','MB','GB','TB']:
      if byte > 1024.0:
        byte /= 1024.0
      else:
        return "%3.2f %s" % (byte, i)

def YouTube():
  try:
    url = input ("[+] Enter URL : ")
    yt = pytube.YouTube(url)
    title = yt.title
    print ("\n[✓] Author : "+yt.author)
    print ("[✓] Title : "+title)
    print ("[✓] Views : "+str(yt.views))
    res = input("\n[+] Choose Resolution\n\n[H] High Resolution\n[L] Low Resolution\n\n[?] Select : ").upper()
    reso = yt.streams.get_highest_resolution() if res == 'H' else yt.streams.first()
    reso = reso.url
    req = requests.get(reso, stream = True)
    save = os.path.join('/sdcard','video','YouTube',yt.video_id + '.mp4')
    with open(save,'wb') as file:
      print ("[!] Downloading Video...")
      for data in req.iter_content(chunk_size=1024):
        file.write(data)
    print ("\n[✓] Download Complete")
    print ("[✓] File Name : "+os.path.basename(save))
    print ("[✓] File Size : "+File_size(save))
    print ("[✓] File Path : "+os.path.realpath(save))
    input ("\n[+] Press Enter To Go Back")
    Main()
  except exceptions.RegexMatchError:
    print ("\n[!] Invalid URL!")
    input ("[+] Press Enter To Go Back")
    Main()
  except exceptions.VideoUnavailable:
    print ("\n[!] Video Not Found!")
    input ("[+] Press Enter To Go Back")
    Main()

def Facebook():
  try:
    url = input("[+] Enter URL : ")
    host = urlparse(url).netloc
    if host in ['www.facebook.com','mbasic.facebook.com','m.facebook.com']:
      url = url.replace('m.facebook','mbasic.facebook').replace('www.facebook','mbasic.facebook')
      a = requests.get(url)
      if 'video_redirect' in a.text:
        b = unquote(a.text.split('?src=')[1].split('"')[0])
        c = re.findall('<title>(.*?)<\/title>',a.text)[0]
        au = c.split(' - ')[0]
        print ("\n[✓] Author : "+au)
        print ("[✓] Title  : "+c.split(' - ')[1].replace('| Facebook',''))
        lanjut = input("\n[?] Download Video [Y/n] ").upper()
        if lanjut == 'Y':
          save = os.path.join('/sdcard','video','Facebook',c.split(' - ')[1] + '.mp4')
          with open(save,'wb') as file:
            print ("[!] Downloading Video...")
            d = requests.get(b,stream = True)
            for data in d.iter_content(chunk_size=1024):
              file.write(data)
          print ("\n[✓] Download Complete")
          print ("[✓] File Name : "+os.path.basename(save))
          print ("[✓] File Size : "+File_size(save))
          print ("[✓] File Path : "+os.path.realpath(save))
          input ("\n[+] Press Enter To Go Back")
          Main()
        else:
          time.sleep(0.5) ; Main()
      else:
        print ("\n[!] Video Not Found!")
        input ("[+] Press Enter To Go Back")
        Main()
    else:
      print ("\n[!] Invalid URL")
      input ("[+] Press Enter To Go Back")
      Main()
  except IndexError:
    print ("\n[!] Error")
    input ("[+] Press Enter To Go Back")
    Main()

def Instagram():
  try:
    url = input("[+] Enter URL : ")
    host = urlparse(url).netloc
    if host in ['www.instagram.com']:
      a = requests.get(url,params = {'__a':'1'},headers = {'user-agent':ua})
      b = json.loads(a.text)['graphql']['shortcode_media']
      if b['is_video']:
        print ("\n[✓] Author : "+b['owner']['username'])
        print ("[✓] Title  : "+str(b['title']))
        print ("[✓] Views  : "+str(b['video_view_count']))
        lanjut = input ("\n[?] Download Video [Y/n] ").upper()
        if lanjut == 'Y':
          save = os.path.join('/sdcard','video','Instagram',b['id'] + '.mp4')
          with open(save,'wb') as file:
            print ("[!] Downloading Video...")
            c = requests.get(b['video_url'],stream = True)
            for data in c.iter_content(chunk_size=1024):
              file.write(data)
          print ("\n[✓] Download Complete")
          print ("[✓] File Name : "+os.path.basename(save))
          print ("[✓] File Size : "+File_size(save))
          print ("[✓] File Path : "+os.path.realpath(save))
          input ("\n[+] Press Enter To Go Back")
          Main()
        else:
          time.sleep(0.5) ; Main()
      else:
        print ("\n[!] Video Not Found")
        input ("[+] Press Enter To Go Back")
        Main()
    else:
      print ("\n[!] Invalid URL")
      input ("[+] Press Enter To Go Back")
      Main()
  except KeyError:
    print ("\n[!] Error")
    input ("[+] Press Enter To Go Back")
    Main()

def xnxx():
  try:
    print ("[!] Please Turn On VPN Before Continue\n")
    url = input('[+] Enter URL : ')
    host = urlparse(url).netloc
    if host in ['www.xnxx.com']:
      a = requests.get(url).text
      if 'View Low Qual' in a and 'View High Qual' in a:
        title = re.findall('<title>(.*?)<\/title>',a)[0].replace('- XNXX.COM','')
        views = bs4.BeautifulSoup(a,'html.parser').find(class_="metadata").text.replace('\n','').replace('\t','').split('-')[2]
        rating = bs4.BeautifulSoup(a,'html.parser').find(class_='rating-box').text
        print ("\n[✓] Title : "+title)
        print ("[✓] Views : "+views)
        print ("[✓] Rating : "+rating)
        res = input("\n[+] Choose Resolution\n\n[H] High Resolution\n[L] Low Resolution\n\n[?] Select : ").upper()
        html = bs4.BeautifulSoup(a,'html.parser')
        if res == 'H':
          url = html.find('a',string = 'View High Qual')['href']
        else:
          url = html.find('a',string = 'View Low Qual')['href']
        save = os.path.join('/sdcard','video','XNXX',title + '.mp4')
        with open(save,'wb') as file:
          print ("[!] Downloading Video...")
          r = requests.get(url,stream = True)
          for data in r.iter_content(chunk_size=1024):
            file.write(data)
        print ("\n[✓] Download Complete")
        print ("[✓] File Name : "+os.path.basename(save))
        print ("[✓] File Size : "+File_size(save))
        print ("[✓] File Path : "+os.path.realpath(save))
        input ("\n[+] Press Enter To Go Back")
        Main()
      else:
        print ("\n[!] Video Not Found")
        input ("[+] Press Enter To Go Back")
        Main()
    else:
      print ("\n[!] Invalid URL")
      input ("[+] Press Enter To Go Back")
      Main()
  except TypeError:
    print ("\n[!] Error")
    input ("[+] Press Enter To Go Back")
    Main()
  except requests.exceptions.SSLError:
    print ("\n[!] Connection Error")
    input ("[+] Press Enter To Go Back")
    Main()

def like():
  try:
    url = input("[+] Enter URL : ")
    host = urlparse(url).netloc
    if host in ['likee.video']:
      a = requests.get(url,headers = {'User-Agent':ua}).text
      b = bs4.BeautifulSoup(a,'html.parser').find('script',type = 'application/ld+json').contents[0]
      c = json.loads(b)
      print ("\n[✓] Author: "+c['creator']['name'])
      print ("[✓] Title : "+c['name'])
      print ("[✓] Upload Date : "+c['uploadDate'])
      lanjut = input ("\n[?] Download Video [Y/n] ").upper()
      if lanjut == 'Y':
        save = os.path.join('/sdcard','video','Like',re.findall('[0-9]+',c['url'])[0] + '.mp4')
        mp4 = urlparse(c['contentUrl'])._replace(scheme = 'https').geturl()
        with open(save,'wb') as file:
          print ("[!] Downloading Video...")
          r = requests.get(mp4,stream = True)
          for data in r.iter_content(chunk_size=1024):
              file.write(data)
        print ("\n[✓] Download Complete")
        print ("[✓] File Name : "+os.path.basename(save))
        print ("[✓] File Size : "+File_size(save))
        print ("[✓] File Path : "+os.path.realpath(save))
        input ("\n[+] Press Enter To Go Back")
        Main()
      else:
        time.sleep(0.5) ; Main()
    else:
      print ("\n[!] Invalid URL")
      input ("[+] Press Enter To Go Back")
      Main()
  except KeyError:
    print ("\n[!] Error")
    input ("[+] Press Enter To Go Back")
    Main()

def SnackVideo():
  try:
    url = input("[+] Enter URL : ")
    host = urlparse(url).netloc
    if host in ['www.snackvideo.com']:
      header = {'Host':'www.snackvideo.com',
                'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
		'sec-ch-ua-mobile':'?1',
		'upgrade-insecure-requests':'1',
		'user-agent':ua,
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'sec-fetch-site':'none',
		'sec-fetch-mode':'navigate',
		'sec-fetch-user':'?1',
		'sec-fetch-dest':'document',
		'accept-encoding':'gzip, deflate, br',
		'accept-language':'en-GB,en;q=0.9'
               }
      a = requests.get(url,headers = header).text
      b = bs4.BeautifulSoup(a,'html.parser').find('script',type = 'application/json',id = '__NEXT_DATA__').contents[0]
      c = json.loads(b)
      #print (c)
      print ("\n[✓] Author : "+c['props']['pageProps']['videoList'][0]['userName'])
      print ("[✓] Title : "+c['props']['pageProps']['videoList'][0]['caption'])
      print ("[✓] Platfrom : "+c['props']['pageProps']['platform'])
      lanjut = input ("\n[?] Download Video [Y/n] ").upper()
      if lanjut == 'Y':
        save = os.path.join('/sdcard/','video','Snack Video',c['props']['pageProps']['videoList'][0]['caption'] + '.mp4')
        with open(save,'wb') as file:
          r = requests.get(c['props']['pageProps']['videoList'][0]['src'],stream = True)
          for data in r.iter_content(chunk_size=1024):
            file.write(data)
        print ("\n[✓] Download Complete")
        print ("[✓] File Name : "+os.path.basename(save))
        print ("[✓] File Size : "+File_size(save))
        print ("[✓] File Path : "+os.path.realpath(save))
        input ("\n[+] Press Enter To Go Back")
        Main()
      else:
        time.sleep(0.5) ; Main()
    else:
      print ("\n[!] Invalid URL")
      input ("[+] Press Enter To Go Back")
      Main()
  except KeyError:
    print ("\n[!] Error")
    input ("[+] Press Enter To Go Back")
    Main()

def Main():
  os.system('clear')
  try:
    pilih = int(input("[+] SELAMAT DATANG BWANG [+]\n\n[1] YouTube\n[2] Facebook\n[3] Instagram\n[4] XNXX\n[5] Like\n[6] Snack Video\n[0] Keluar\n\n[?] Pilih : "))
    if pilih == 1:
      YouTube()
    elif pilih == 2:
      Facebook()
    elif pilih == 3:
      Instagram()
    elif pilih == 4:
      xnxx()
    elif pilih == 5:
      like()
    elif pilih == 6:
      SnackVideo()
    elif pilih == 0:
      os.abort()
    else:
      raise ValueError
  except ValueError:
    print ("[!] Input Tidak Valid :(")
    time.sleep(1.5)
    Main()
  except KeyboardInterrupt:
    exit("\n[!] Exit")
  except EOFError:
    os.abort()
  except requests.exceptions.ConnectionError:
    print ("\n[!] No Connection")
    exit("[!] Exit!")
  except requests.exceptions.Timeout:
    print ("\n[!] The request timed out")
    exit("[!] Exit!")
  except requests.exceptions.ConnectTimeout:
    print ("\n[!] The request timed out while trying to connect to the remote server")
    exit("[!] Exit!")
  except Exception as err:
    print ("\n[!] "+str(err))
    exit("[!] Exit!")

if __name__ == "__main__":
  Main()
