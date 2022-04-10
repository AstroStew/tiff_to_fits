# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 12:10:15 2022

@author: mstew
"""

import PySimpleGUI as sg
import os
import os.path
from astropy.nddata import CCDData
from pathlib import Path
import PIL
from tqdm import tqdm
from itertools import chain

def gui():
    windowopen = False
    sg.theme("Default1")
    
    
    inputcameraparams_tab=[[sg.Text('Define Parameters'),
                            
                            sg.Radio("Input","RADIO2",default=True,key='defined_params_bool'),
                            sg.Radio("file","RADIO2",default=False,key='file_params_bool'),
                            ],
                           [sg.Text("Input Camera Parameters",justification='center')],
                           [sg.T("X Binning"),sg.InputText('1',key='xbinning')],
                           [sg.T("Y Binning"),sg.InputText('1',key='ybinning')],
                           [sg.T('Pixel Size(um)'),sg.InputText('7.2',key='pix_size')],
                           [sg.T("Latitude:"), sg.InputText('47.492',key='lat')],
                           [sg.T("Longtitude:"), sg.InputText('-52978',key='long')],
                           [sg.T("Focal Length (mm):"), sg.InputText('952',key='focal_len')],
                           [sg.T("Gain (e/ADU):"),sg.InputText('1',key='egain')],
                           [sg.T("Exposure Time(s)"),sg.InputText('5',key='exptime')],
                           [sg.T("Filter(i.e B,G,R,V)"),sg.InputText('V',key='filter')],
                           
                           [sg.Text("Camera Prams file"),sg.Input
                           (r'C:/Users/mstew/Documents/GitHub/Astro2/Reference Star Files/Reference_stars_2022_02_17_d.txt',
                            key="camera_params_file", change_submits=True),
                           sg.FileBrowse(key="camera_params_file2")],
                           
                           [sg.Text("Light Image Directory"),
                            sg.Input(r'C:\Users\mstew\Documents\School and Work\Dec 24 testing\lights',
                                     key='light_img_dir',change_submits=True),sg.FolderBrowse(key='light_img_dir2')],
                           [sg.Text("Flat Image Directory"),
                            sg.Input(r'C:\Users\mstew\Documents\School and Work\Dec 24 testing\Flats',
                                     key='flat_img_dir',change_submits=True),sg.FolderBrowse(key='flat_img_dir2')],
                           [sg.Text("Dark Image Directory"),
                            sg.Input(r'C:\Users\mstew\Documents\School and Work\Dec 24 testing\darkflats',
                                     key='dark_img_dir',change_submits=True),sg.FolderBrowse(key='dark_img_dir2')],
                           [sg.Text("Bias Image Directory"),
                            sg.Input(r'C:\Users\mstew\Documents\School and Work\Dec 24 testing\Bias',
                                     key='bias_img_dir',change_submits=True),sg.FolderBrowse(key='bias_img_dir2')],
                           [sg.Button('Convert'),sg.Cancel()]
                           
                          ]
    if windowopen is False:
        window=sg.Window('Tiff to fits',inputcameraparams_tab)
        windowopen = True
    while True:
        window.Refresh()
        event,values=window.read()
        if event=="Convert":
            # TODO: Finish this code
            if values['defined_params_bool'] is True:
                # Do something
                print('Taking in Camera Params from GUI')
                camera_params={'Latitude':values['lat'],
                               'Longitude':values['long'],
                               'Focal Lenght': values['focal_len'],
                               'Gain': values['egain'],
                               'Filter':values['filter'],
                               'Xbinning':values['xbinning'],
                               'Ybinning': values['ybinning'],
                               'Pixel Size': values['pix_size'],
                               'Exposure Time': values['exptime']
                               }
                convert_image(camera_params,values['flat_img_dir'],values['light_img_dir'],values['dark_img_dir'],values['bias_img_dir'])
                
            elif values['file_params_bool'] is True:
                # Read File
                print('Reading File')
                with open(values['camera_params_file'],'r') as reader:
                    file = reader.read()
                    for line in file:
                        camera_params[line.split(':')[0]]=line.split(':')[1]
                        
                        
                        
                        
                        
                
                #TODO: Ceate Standard for File
                
            
            
            
        if event == sg.WIN_CLOSED or event == "Exit" or sg.Cancel():
            window.close()
            break 
        
def convert_image(camera_params,light_img_directory,flat_image_directory,dark_image_directory,bias_image_directory):
    file_suffix=(".tiff",".tif")
    
    validdirs=[directory for directory in [light_img_directory,flat_image_directory,dark_image_directory,bias_image_directory] if (directory != '' and os.path.exists(directory))]
    
    for root,dirs,files in os.walk(chain(validdirs)):
        for file in tqdm(files):
            
                
            print('Converting Images')
        
GUI= gui()            