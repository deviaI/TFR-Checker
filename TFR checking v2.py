# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 14:17:29 2021

@author: Lukas Knöppel
"""

import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import threading
import time
def get_current_Tfrs():
    Notamnew = []
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
    return Notamnew

def check(oldNotam):
    Notamold = oldNotam
    Notamnew = get_current_Tfrs()
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
        
    for i in news:
        note = 'New TX Space Ops TFR ' + Notamnew[i]
        toaster.show_toast("FAA TFR", note)
        print(note)
    for i in cancs:
        note = 'TX Space Ops TFR ' + Notamold[i] + ' has been cancelled'
        toaster.show_toast("FAA TFR", note)
        print(note)
    print('Last Checked at', time.ctime())
    threading.Timer(900, check, args = [Notamnew]).start()