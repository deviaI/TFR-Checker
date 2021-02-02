# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:58:48 2021

@author: Lukas Knöppel
"""
import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import threading
import time
def get_current_Tfrs():
    Notamnew = []
    tfrs = []
    topNotam = ''
    url = 'https://tfr.faa.gov/tfr2/list.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for results in soup.findAll('tr', attrs = {'valign':'top', 'height':"40"}):
        nr = ''
        st = ''
        ty = ''
        topNotam = results.text
        zeilen = [line for line in topNotam]
        for i in range(17,23):
            nr = nr + zeilen[i]
        for i in range(32,34):
            st = st + zeilen[i]
        for i in range(37,42):
            ty = ty + zeilen[i]
        if st == 'TX' and ty == 'SPACE':  #You can insert any state you want, or simply remove the check for st to get results for space ops tfrs outside of texas
            Notamnew.append(nr)
            tfrs.append(results.text)
    return Notamnew, tfrs

def checkTFR(oldNotam, oldtfrs):
    Notamold = oldNotam
    tfrsold = oldtfrs
    Notamnew, tfrsnew = get_current_Tfrs()
    toaster = ToastNotifier()
    i = 0
    news = []
    cancs = []
    while i < len(Notamnew):
        k = 0
        t_f = 0
        while k < len(Notamold):
            if Notamnew[i] == Notamold[k]:
                t_f = 1
            k = k + 1
        if t_f == 0:
            news.append(i)
        i = i + 1
    i = 0
    while i < len(Notamold):
        k = 0
        t_f = 0
        while k < len(Notamnew):
            if Notamold[i] == Notamnew[k]:
                t_f = 1
            k = k + 1
        if t_f == 0:
             cancs.append(i)
        i = i + 1
    for i in range(0, len(tfrsnew)):
        temp = tfrsnew[i].split('\n')
        tfrsnew[i] = ''
        for k in range(3, len(temp)):
            if temp[k] != '':
                tfrsnew[i] = tfrsnew[i] + ', ' + temp[k]
    for i in news:
        note = 'New TX Space Ops TFR' + tfrsnew[i] + '\n'
        if Notamold[0] != '0':
            toaster.show_toast("FAA new TFR", Notamnew[i])
        else:
                checkSpaceX('','')
        print(note)
    for i in cancs:
        if Notamold[0] != '0':
            note = 'TX Space Ops TFR ' + tfrsold[i] + ' has been cancelled \n'
            toaster.show_toast("FAA cancelled TFR", Notamold[i])
            print(note)
        else:
            checkSpaceX('','')
    print('Last Checked at', time.ctime())
    threading.Timer(900, checkTFR, args = [Notamnew, tfrsnew]).start()
    
    
def checkSpaceX(TextOld, DateOld):
    url = 'https://www.spacex.com/vehicles/starship/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find('div', attrs={'class':'text-columns'})
    txt = result.text
    txt2 = txt.split('the SpaceX team')
    toaster = ToastNotifier()
    if TextOld != '':
        if result.text != TextOld:
            if DateOld != txt2[0]:
                toaster.show_toast("SpaceX change", "SpaceX has changed the SN9 NET Date")
            else:
                toaster.show_toast("SpaceX change", "SpaceX has changed the SN9 Website")
    threading.Timer(900, checkSpaceX, args = [txt, txt2[0]]).start()


        
