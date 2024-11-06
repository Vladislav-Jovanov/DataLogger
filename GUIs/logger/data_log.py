#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 23:05:06 2024

@author: tze
"""
from tkWindget.tkWindget import AppFrame, OnOffButton, FigureFrame, IPEntry
from RW_data.RW_files import Files_RW
from tkinter import Frame, Button, Label, StringVar, IntVar, DoubleVar, OptionMenu, _setit, DISABLED, NORMAL
import os
import time
from tkinter.filedialog import asksaveasfilename
import numpy as np
from Figure.Figure import FigureE60
import socket


#two approached to test either with prolonged time after you get hit, or with whilelooping

class Logger(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,appgeometry=(900,600,10,10))
        self.init_variables()
        try:
            tmp=Files_RW().check_IV_measure_ini(self.scriptdir,self.ini_name,Files_RW.split)
            self.savedir=tmp.savedir
        except:
            self.savedir='Documents'
            self.write_to_ini()
        try:
            filename=self.ini_name.split('.')[0]+'.instr'
            self.ipaddr,self.sockport=Files_RW().check_IV_measure_inst_file(self.scriptdir,filename,self.split)    
        except:
            self.ipaddr='192.168.1.210'
            self.sockport=5025
            self.write_to_instr()
        self.init_frames()
        self.init_commandframe()
        
    def write_to_ini(self):
        write=[]
        write.append(f'save_file_path{Files_RW.split}{self.savedir}')
        Files_RW().write_to_file(self.scriptdir,self.ini_name,write)
    
    def write_to_instr(self):
        write=[]
        write.append(f'ip_address{Files_RW.split}{self.ipaddr}')
        write.append(f"port{Files_RW.split}{self.sockport}")
        Files_RW().write_to_file(self.scriptdir,self.ini_name.split('.')[0]+'.instr',write)
        
        
    def init_variables(self):
        self.scriptdir=os.path.dirname(__file__)
        self.ini_name=os.path.basename(__file__).replace(os.path.basename(__file__).split('.')[-1],'ini')
        self.variables={"quantity":StringVar(),
                        "range":StringVar(),
                        "unit":StringVar(),
                        "delay":DoubleVar(),
                        "integration":DoubleVar(),
                        "type":StringVar(),
                        "samples":IntVar()}
        self.quantities_details={"Voltage":{"name":"VOLT", "DC":[100e-3,1,10,100,1000],"AC":[100e-3,1,10,100,750]},"Current":{"name":"CURR", "DC":[100e-6,1e-3,10e-3,100e-3,1,3], "AC":[100e-6,1e-3,10e-3,100e-3,1,3]}}
        self.quantities=[key for key in self.quantities_details.keys()]
        self.types=["DC","AC"]
        self.xname="Time"
        self.units={"Voltage":"V","Current":"A","Time":"s"}
        self.takt=1/50;
        self.now=0;
        #self.test=0
        self.measurement_init=False
        self.command_list={'connect':{'on':self.connect,'off':self.disconnect},'collect':{'on':self.collect_plot,'off':self.stop_collect_plot}}
        self.command_elements={}
        
    def update_time_between(self):
        if self.command_elements["zrck"].get_state()=="on":    
            self.time_between_points=self.takt*(self.variables['integration'].get()*2+self.variables["delay"].get()) #seconds
        else:
            self.time_between_points=self.takt*(self.variables['integration'].get()+self.variables["delay"].get())
        self.sample_time=np.linspace(-(self.variables['samples'].get()-1)*self.time_between_points,0,self.variables['samples'].get())
        
        
    def init_frames(self):
        self.commandframe = Frame(self.frameroot)
        self.commandframe.grid(column=0,row=0)
        self.commandframe.columnconfigure(0, weight = 1)
        self.commandframe.rowconfigure(0, weight = 1)
        self.figure=FigureFrame(parent=self.frameroot,figclass=FigureE60)
        self.figure.grid(row=0,column=1)
        self.figure.columnconfigure(0, weight = 1)
        self.figure.rowconfigure(0, weight = 1)
        self.figure.plot.ax.set_xlim(0,1)
        self.figure.plot.ax.set_xlabel(f'{self.xname} ({self.units[self.xname]})',fontsize=10, position=(0.5,0),labelpad=5)
        self.figure.plot.ax.locator_params(axis='x', nbins=4)
        
    def init_commandframe(self):
        rowcount=1
        self.command_elements['ip']=IPEntry(parent=self.commandframe,address=f"{self.ipaddr}:{self.sockport}")
        self.command_elements['ip'].grid(row=rowcount,column=1)
        rowcount+=1
        tmpframe=Frame(self.commandframe)
        tmpframe.grid(row=rowcount,column=1)
        Label(tmpframe,text="Quantity",width=12,anchor='w').grid(row=1,column=0,sticky="W")
        Label(tmpframe,text="Unit",width=5,anchor='w').grid(row=1,column=1,sticky="W")
        Label(tmpframe,text="Range",width=10,anchor='w').grid(row=1,column=2,sticky="W")
        Label(tmpframe,text="Type",width=8,anchor='w').grid(row=1,column=3,sticky="W")
        self.command_elements['quantity']=OptionMenu(tmpframe,self.variables['quantity'],*self.quantities,command=self.update_quantity)
        self.command_elements['quantity'].grid(row=2,column=0,sticky="W") 
        Label(tmpframe,textvariable=self.variables['unit']).grid(row=2,column=1,sticky="W")
        self.command_elements['type']=OptionMenu(tmpframe,self.variables['type'],*self.types,command=self.update_range)
        self.command_elements['type'].grid(row=2,column=3,sticky="W")
        self.command_elements['range']=OptionMenu(tmpframe,self.variables["range"],*self.quantities_details[self.quantities[0]][self.types[0]])
        self.command_elements['range'].grid(row=2,column=2,sticky="W")
        self.set_defaults()
        
        
        rowcount+=1
        tmpframe=Frame(self.commandframe)
        tmpframe.grid(row=rowcount,column=1)
        Label(tmpframe,text="Integration",width=12,anchor='w').grid(row=1,column=0,sticky="W")
        Label(tmpframe,text="Delay",width=5,anchor='w').grid(row=1,column=1,sticky="W")
        Label(tmpframe,text="Autozero",width=10,anchor='w').grid(row=1,column=2,sticky="W")
        Label(tmpframe,text="Samples",width=8,anchor='w').grid(row=1,column=3,sticky="W")
        #Label(tmpframe,text="Delay: ", borderwidth=2,relief=GROOVE).grid(row=1,column=0)
        self.command_elements['integration']=OptionMenu(tmpframe,self.variables['integration'],*[0.2,1,10,100])
        self.command_elements['integration'].grid(row=2,column=0)
        self.command_elements['delay']=OptionMenu(tmpframe,self.variables['delay'],*[0,0.2,1,10,100,1000])
        self.command_elements['delay'].grid(row=2,column=1)
        self.command_elements['zrck']=OnOffButton(parent=tmpframe,imagepath=os.path.join(self.scriptdir,'images'),images=[f'zrck_{image}' for image in ['on.png','off.png']])
        self.command_elements['zrck'].grid(row=2,column=2)
        self.command_elements['zrck'].enable_press()
        self.command_elements['samples']=OptionMenu(tmpframe,self.variables['samples'],*[1,50,100,1000,5000])
        self.command_elements['samples'].grid(row=2,column=3)
        
        rowcount+=1
        tmpframe=Frame(self.commandframe)
        tmpframe.grid(row=rowcount,column=1)
        for idx, item in enumerate(self.command_list.keys()):
            tmp=OnOffButton(parent=tmpframe,imagepath=os.path.join(self.scriptdir,'images'),images=[f'{item}_{image}' for image in ['on.png','off.png']],command=lambda litem=item: self.press_test(litem))
            tmp.grid(row=1,column=idx)
            self.command_elements[item]=tmp
        self.command_elements['connect'].enable_press()
        rowcount+=1
        self.command_elements['save']=Button(self.commandframe, text="Save Data", width=12, command=self.save_data)
        self.command_elements['save'].grid(row=rowcount,column=0,columnspan=2)
        self.command_elements['save'].configure(state="disabled")
        self.set_defaults()
    
    def set_defaults(self):
        self.variables['quantity'].set(self.quantities[0])
        self.variables['type'].set(self.types[0])
        self.variables['unit'].set(self.units[self.quantities[0]])
        self.variables['range'].set(self.quantities_details[self.quantities[0]][self.types[0]][-1])
        self.variables['integration'].set(1)
        self.variables['delay'].set(1)
        self.variables['samples'].set(100)
        
    
    def update_range(self,var):
        self.change_options(self.command_elements["range"], self.variables["range"], self.quantities_details[self.variables["quantity"].get()][var])
        if self.variables["range"].get() not in [str(item) for item in self.quantities_details[self.variables["quantity"].get()][var]]:
            self.variables["range"].set(self.quantities_details[self.variables["quantity"].get()][var][-1])
        
    
    def update_quantity(self,var):
        self.variables["unit"].set(self.units[var])
        self.change_options(self.command_elements["range"], self.variables["range"], self.quantities_details[var][self.variables["type"].get()])
        if self.variables["range"].get() not in [str(item) for item in self.quantities_details[var][self.variables["type"].get()]]:
            self.variables["range"].set(self.quantities_details[var][self.variables["type"].get()][-1])
        
    def change_options(self,menu,var,new_choices):
        menu['menu'].delete(0, 'end')
        for choice in new_choices:
            menu['menu'].add_command(label=choice, command=_setit(var, choice))
    
    
    def press_test(self,item):
        self.command_list[item][self.command_elements[item].get_state()]()
    
    def placeholder(self):
        pass
    
    def save_data(self):
        header=[]
        text='#comment'
        header.append(text)
        text="#setup"
        header.append(text)
        text='#data_header'
        header.append(text)
        text=f'{self.xname}\t{self.variables["quantity"].get()}'
        header.append(text)
        text=f'{self.units[self.xname]}\t{self.units[self.variables["quantity"].get()]}'
        header.append(text)
        text='#data_table'
        header.append(text)
        data=np.append(self.datatime[:,np.newaxis],self.data[:,np.newaxis],axis=1)
        fmtlist=['%.6e','%.6e']
        filename = asksaveasfilename(title="Select the folder to save the processed data.", initialdir=self.savedir,filetypes=[("Tab sep file","*.log")],initialfile='Measured_IV')
        if filename:
            Files_RW().write_header_data(os.path.dirname(filename),os.path.basename(filename),header,data,fmtlist)
            self.savedir=os.path.dirname(filename)
            #self.write_to_ini()
            self.command_elements['save'].config(state=DISABLED)
    
    def connect(self):
        self.sock=socket.socket()
        self.update_time_between()
        try:
            self.sock.connect((self.command_elements["ip"].get_address(), self.command_elements["ip"].get_port()))
            
        except:
            self.command_elements['connect'].change_state('off')
        if self.command_elements["connect"].get_state()=="on":
            self.init_plot_data()
            self.command_elements['collect'].enable_press()
            self.figure.plot.ax.set_ylabel(f"{self.variables['quantity'].get()} ({self.units[self.variables['quantity'].get()]})")
            self.figure.canvas.draw()
            self.command_elements['ip'].disable()
            self.command_elements['zrck'].disable_press()
            self.command_elements['quantity'].config(state=DISABLED)
            self.command_elements['type'].config(state=DISABLED)
            self.command_elements['range'].config(state=DISABLED)
            self.command_elements['integration'].config(state=DISABLED)
            self.command_elements['delay'].config(state=DISABLED)
            self.command_elements['samples'].config(state=DISABLED)
            self.sock.send("*RST\n".encode('utf-8'))
            #CONF:VOLT:DC 10\n
            self.sock.send(f"CONF:{self.quantities_details[self.variables['quantity'].get()]['name']}:{self.variables['type'].get()} {self.variables['range'].get()}\n".encode('utf-8')) #sets the range
            #VOLT:NPLC 1\n
            self.sock.send(f"{self.quantities_details[self.variables['quantity'].get()]['name']}:{self.variables['type'].get()}:NPLC {self.variables['integration'].get()}\n".encode('utf-8')) #sets the aperture and resolution
            self.sock.send(f"SAMP:COUN {self.variables['samples'].get()}\n".encode('utf-8')) #sets number of sample counts
            self.sock.send("TRIG:SOUR IMM\n".encode('utf-8')) #sets trigger source to be INIT command
            self.sock.send(f"TRIG:DEL {self.variables['delay'].get()*self.takt}\n".encode('utf-8'))
            #VOLT:DC:ZERO:AUTO ON\n
            self.sock.send(f"{self.quantities_details[self.variables['quantity'].get()]['name']}:{self.variables['type'].get()}:ZERO:AUTO {self.command_elements['zrck'].get_state()}\n".encode('utf-8'))
            
            
            
            
        
    def disconnect(self):
        self.sock.close()
        self.command_elements['collect'].change_state('off')
        self.command_elements['collect'].disable_press()
        self.command_elements['ip'].enable()
        self.command_elements['zrck'].enable_press()
        self.command_elements['quantity'].config(state=NORMAL)
        self.command_elements['type'].config(state=NORMAL)
        self.command_elements['range'].config(state=NORMAL)
        self.command_elements['integration'].config(state=NORMAL)
        self.command_elements['delay'].config(state=NORMAL)
        self.command_elements['samples'].config(state=NORMAL)
        
    
    def update_time(self,data_points):
        #if data_points==self.variables["samples"].get():
        timearray=self.sample_time[-(data_points-1):0]
        #else:
        #    timearray=np.linspace(-(data_points-1)*self.time_between_points,0,data_points)
        self.datatime=np.append(self.datatime,timearray+time.time()-self.now)
                 
    def update_min_max(self):
        if np.shape(self.data)==np.shape(np.array([])):
            self.datamin=np.min(self.new_data)
            self.datamax=np.max(self.new_data)+1e-6
        else:
            self.datamin=min(self.datamin,np.min(self.new_data))
            self.datamax=max(self.datamax,np.max(self.new_data))
            
    
    def collect_plot(self):
        if self.command_elements['collect'].get_state()=="on":
            #initialization of a new measurement
            if not self.measurement_init:
                self.now=time.time()
                self.sock.send("INIT\n".encode('utf-8')) #old data deleted and new is being stored into reading memory
                self.measurement_init=True
                self.frameroot.after(int(self.variables["samples"].get()*self.time_between_points*1000*0.7),self.collect_plot)
            #checking of the number of data after initialization
            else:
                self.sock.send("ABOR\nDATA:POIN?\n".encode('utf-8'))
                data_points=int(self.sock.recv(1024).decode('utf-8'))
                self.sock.send("FETC?\nINIT\n".encode('utf-8'))
                #print(data_points)
                #self.test+=1
                #if data_points==self.variables["samples"].get():
                #if self.test==self.sample_points:
                self.update_time(data_points)
                    #self.sock.send("FETC?\nINIT\n".encode('utf-8'))
                    #self.sock.send("INIT\n".encode('utf-8')) #old data deleted and new is being stored into readingmemory    
                self.get_all_data(data_points)
                self.update_min_max()
                self.data=np.append(self.data,self.new_data)
                self.update_plot()
                self.frameroot.after(int(self.variables['samples'].get()*self.time_between_points*1000*0.7),self.collect_plot)
                #    return
                #elif data_points>self.variables["samples"].get()-3:
                #    self.frameroot.after(int(self.time_between_points*1000/4),self.collect_plot)
                #else:
                #    self.frameroot.after(int(self.time_between_points*1000),self.collect_plot)
                    #print(time.time(),"out if")
      
    
    def get_all_data(self,data_points):
        data=''
        while len(data.strip().split(','))!=data_points or data=='':
            data=data+self.sock.recv(2048).decode('utf-8')
        self.new_data=np.array(data.strip().split(',')).astype(float)
        
        

    def stop_collect_plot(self):
        self.sock.send("ABOR\nDATA:POIN?\n".encode('utf-8'))
        #self.sock.send("DATA:POIN?\n".encode('utf-8'))
        data_points=int(self.sock.recv(1024).decode('utf-8'))
        #print(data_points)
        if data_points!=0:
            self.sock.send("FETC?\n".encode('utf-8'))
            self.update_time(data_points)
            #self.sock.send("FETC?\n".encode('utf-8'))
            self.get_all_data(data_points)      
            self.update_min_max()
            self.data=np.append(self.data,self.new_data)
            self.update_plot()
        self.measurement_init=False;
        self.command_elements['collect'].change_state('off')
        self.command_elements['collect'].disable_press()
        self.command_elements['connect'].change_state('off')
        self.command_list["connect"][self.command_elements["connect"].get_state()]()
        self.command_elements['save'].configure(state="active")
        
    def init_plot_data(self):
        self.data=np.array([])
        self.datatime=np.array([]) 
        self.figure.plot.ax.plot(self.datatime,self.data)
        
    def update_plot(self):
        if len(self.figure.plot.ax.lines)!=0:
            self.figure.plot.ax.lines[0].set_xdata(self.datatime)
            self.figure.plot.ax.lines[0].set_ydata(self.data)
        
        
        self.figure.plot.ax.set_ylim(self.datamin,self.datamax)
        self.figure.plot.ax.set_xlim(0,self.datatime[-1])
        self.figure.canvas.draw()    
    
