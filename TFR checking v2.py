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
import numpy as np
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
            url = 'https://tfr.faa.gov/save_pages/detail_'+ nr.split('/')[0] + '_'+ nr.split('/')[1] +'.html'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            res2 = soup.find('table', attrs = {'width':'830', 'border':'0', 'cellpadding':'2'})
            temp = res2.text
            temp = temp.split('Altitude:')[1]
            temp = temp.split('Effective Date')[0]
            temp = temp.split('\n')[0]
            Notamnew.append(nr)
            tfrs.append(results.text.replace('\r', '') + temp)
            Notamnew.append(nr)
            tfrs.append(results.text)
    return Notamnew, tfrs

def checkTFR():
    try:
        temp = np.load('Notams.npz')
        temp = temp['arr_0']
        Notamold = temp.tolist()
        del temp
    except FileNotFoundError:
        Notamold = []
    try:
        temp = np.load('tfrs.npz')
        temp = temp['arr_0']
        tfrsold = temp.tolist()
        del temp
    except FileNotFoundError:
        tfrsold = []
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
            if temp[k] != '' and temp[k] != ' New  ':
                tfrsnew[i] = tfrsnew[i] + ', ' + temp[k]
    for i in news:
        note = 'New TX Space Ops TFR' + tfrsnew[i] + '\n'
        if len(Notamold) != 0:
            toaster.show_toast("FAA new TFR", Notamnew[i])
        print(note)
    for i in cancs:
        note = 'TX Space Ops TFR' + tfrsold[i] +'\n' + 'has been cancelled \n'
        toaster.show_toast("FAA cancelled TFR", Notamold[i])
        print(note)

    np.savez('Notams', Notamnew)
    np.savez('tfrs', tfrsnew)
    try:
        temp = np.load('Text.npz')
        temp = temp['arr_0']
        TextOld = temp.tolist()
        del temp
    except FileNotFoundError:
        TextOld = ''
    try:
        temp = np.load('Date.npz')
        temp = temp['arr_0']
        DateOld = temp.tolist()
    except FileNotFoundError:
        DateOld = ''
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
                toaster.show_toast("SpaceX change", "SpaceX has changed the Starship NET Date")
                print("SpaceX has changed the Starship NET Date")
            else:
                toaster.show_toast("SpaceX change", "SpaceX has changed the Starship Website")
                print("SpaceX has changed the Starship Webpage")
    np.savez('Text', txt)
    np.savez('Date', txt2[0])
    print('Last Checked at', time.ctime())
    threading.Timer(3600, checkTFR).start()


        
