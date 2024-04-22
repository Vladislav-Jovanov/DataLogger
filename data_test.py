#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 23:05:06 2024

@author: tze
"""
from tkWindget.tkWindget import AppFrame, OnOffButton
from tkinter import Frame
import os
import time
from threading import Thread


class DataTest(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.data=[]
        self.appgeometry=(900,600,10,10)
        self.scriptdir=os.path.dirname(__file__)
        self.btn_list={}
        self.command_list={'data':{'on':self.data_collect,'off':self.stop_data_collect},'display':{'on':self.display_function,'off':self.placeholder}}
        
        rowcount=1
        for idx, item in enumerate(self.command_list.keys()):
            tmp=OnOffButton(parent=self.root,imagepath=os.path.join(self.scriptdir,'images'),images=[f'{item}_{image}' for image in ['on.png','off.png']],command=lambda litem=item: self.press_test(litem))
            tmp.grid(row=rowcount,column=1+idx)
            self.btn_list[item]=tmp
        self.btn_list['data'].enable_press()
        
    
    def press_test(self,item):
        self.command_list[item][self.btn_list[item].get_state()]()
    
    def placeholder(self):
        pass
    
    def data_collect(self):
        self.btn_list['display'].enable_press()
        #self.T1 = Thread(target=self.data_read, args=())
        #self.T1.daemon = True
        #self.T1.start()
        #self.T1.join()
        self.data_read()
        
    def stop_data_collect(self):
        self.data=[]
        self.btn_list['display'].change_state('off')
        self.btn_list['display'].disable_press()
        
    
    def data_read(self):
        if self.btn_list['data'].get_state()=='on':
            print(f'Data_time:{time.time()}')
            if not self.data:
                self.data.append(1)
            else:
                self.data.append(self.data[-1]+1)
            self.root.after(100,self.data_read)
    
    def display_function(self):
        #self.T2 = Thread(target=self.update_display, args=())
        #self.T2.daemon = True
        #self.T2.start()
        self.update_display()
    
    def update_display(self):
        if self.btn_list['display'].get_state()=='on':
            print(f'Display_data:{self.data[-5:]}')
            print(f'Display_time:{time.time()}')
            time.sleep(2)
            self.root.after(1000,lambda:self.update_display)
            #self.root.after(3,self.update_display)
    
DataTest().init_start()