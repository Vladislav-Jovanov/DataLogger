#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:19:18 2022

@author: tzework
"""
from matplotlib.figure import Figure

class container():
    pass


class FigureE60(Figure):
    def __init__(self):
        super().__init__()
        #matplotlib muliplies axes size with large figure size that is why you always divide with large figure size
        figwidth=10#fullfigure size
        figheight=8#fullfigure size
        x0=2#relative to large figure
        y0=2#relative to large figure
        w=7#small fig size in percentage of large figure
        h=5#small fig size in percentage of large figure

        self.set_size_inches((figwidth/2.54,figheight/2.54))
        self.ax=self.add_axes([x0/figwidth,y0/figheight,w/figwidth,h/figheight])
        self.ax.tick_params(labelsize=8)
        self.ax.set_xlabel('wavelength (nm)',fontsize=10, position=(0.5,0),labelpad=5)
        self.ax.set_ylabel('',fontsize=10,  position=(0,0.5),labelpad=5)
        self.ax.set_xlim(200,1200)
        
            
            
class Figure_top_bottom(Figure):
    def __init__(self):
        #matplotlib muliplies axes size with large figure size that is why you always divide with large figure size
        super().__init__()
        xdim=9.5
        ydim=14
        axx=7
        axy=5
        axx0=1.5
        axy0=1.5
        spacing=1.5
        
        self.set_size_inches((xdim/2.54,ydim/2.54))
        self.axb=self.add_axes((axx0/xdim,axy0/ydim,axx/xdim,axy/ydim))
        self.axb.tick_params(labelsize=8)
        self.axb.set_xlabel('wavelength (nm)',fontsize=10, position=(0.5,0),labelpad=5)
        self.axb.set_ylabel('Absorbance (%)',fontsize=10,  position=(0,0.5),labelpad=5)
        
                               
        self.axt=self.add_axes([axx0/xdim,(axy0+axy+spacing)/ydim,axx/xdim,axy/ydim])
        self.axt.tick_params(labelsize=8)
        self.axt.set_xlabel('wavelength (nm)',fontsize=10, position=(0.5,0),labelpad=5)
        self.axt.set_ylabel('All contributions (%)',fontsize=10,  position=(0,0.5),labelpad=5)
        #self.axt.legend(['1-R','T'],loc='upper right',bbox_to_anchor=(1.1, 1.15),framealpha=0.5)