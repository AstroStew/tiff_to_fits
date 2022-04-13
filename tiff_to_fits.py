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
from PIL import Image, TiffTags, ExifTags
from tqdm import tqdm
from itertools import chain
from astropy.io import fits


def gui():
    windowopen = False
    sg.theme("Default1")

    inputcameraparams_tab=[[sg.Text('Define Parameters'),
                            
                            sg.Radio("Input","RADIO2",default=True,key='defined_params_bool'),
                            sg.Radio("file","RADIO2",default=False,key='file_params_bool'),
                            ],
                           [sg.Checkbox('Overwrite Meta Data',default=False,key='overwrite_meta')],
                           [sg.Text("Input Camera Parameters",justification='center')],
                           [sg.T("X Binning"),sg.InputText('1',key='xbinning')],
                           [sg.T("Y Binning"),sg.InputText('1',key='ybinning')],
                           [sg.T('Pixel Size(um)'),sg.InputText('7.2',key='pix_size')],
                           [sg.T("Latitude:"), sg.InputText('47.492',key='lat')],
                           [sg.T("Longtitude:"), sg.InputText('-52.978',key='long')],
                           [sg.T("Focal Length (mm):"), sg.InputText('952',key='focal_len')],
                           [sg.T("Gain (e/ADU):"),sg.InputText('1',key='egain')],
                           [sg.T("Exposure Time(s)"),sg.InputText('5',key='exptime')],
                           [sg.T("Filter(i.e B,G,R,V)"),sg.InputText('V',key='filter')],
                           
                           [sg.Text("Camera Params file"),sg.Input
                           (r'C:/Users/mstew/Documents/GitHub/Astro2/Reference Star Files/Reference_stars_2022_02_17_d.txt',
                            key="camera_params_file", change_submits=True),
                           sg.FileBrowse(key="camera_params_file2")],
                           
                           [sg.Text("Light Image Directory"),
                            sg.Input(r'',
                                     key='light_img_dir',change_submits=True),sg.FolderBrowse(key='light_img_dir2')],
                           [sg.Text("Flat Image Directory"),
                            sg.Input(r'',
                                     key='flat_img_dir',change_submits=True),sg.FolderBrowse(key='flat_img_dir2')],
                           [sg.Text("Dark Image Directory"),
                            sg.Input(r'',
                                     key='dark_img_dir',change_submits=True),sg.FolderBrowse(key='dark_img_dir2')],
                           [sg.Text("Bias Image Directory"),
                            sg.Input(r'',
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
                               'Exposure Time': values['exptime'],
                               'Over Write Meta': values['overwrite_meta']
                               }
                convert_image(camera_params,values['light_img_dir'],values['flat_img_dir'],values['dark_img_dir'],values['bias_img_dir'])
                
            elif values['file_params_bool'] is True:
                # Read File
                print('Reading File')
                with open(values['camera_params_file'],'r') as reader:
                    file = reader.read()
                    for line in file:
                        camera_params[line.split(':')[0]]=line.split(':')[1]
                #TODO: Ceate Standard for File
                
            
            
            
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            break 
        
def convert_image(camera_params,light_img_directory,flat_image_directory,dark_image_directory,bias_image_directory):
    file_suffix=(".tiff",".tif")
    
    validdirs=[directory for directory in [light_img_directory,flat_image_directory,dark_image_directory,bias_image_directory] if (directory != '' and os.path.exists(directory))]
    
# =============================================================================
#     for root,dirs,files in os.walk((path) for path in validdirs):
# =============================================================================
    for root,dirs,files in chain.from_iterable(os.walk(path) for path in validdirs):
        for file in tqdm(files):
            if file.endswith(file_suffix):
                fits_image= fits.PrimaryHDU(data=Image.open(os.path.join(root,file)))
                
                # Search through exif to find Exposure, 
                img = Image.open(os.path.join(root,file))
                exifdata=img.getexif()
                
                
                # Set from Camera_Params
                fits_image.header['XBINNING']=int(camera_params['Xbinning'])
                fits_image.header['YBINNING']=int(camera_params['Ybinning'])
                fits_image.header['FILTER']=str(camera_params['Filter'])
                fits_image.header['XPIXSZ']=float(camera_params['Pixel Size'])
                fits_image.header['YPIXSZ']=float(camera_params['Pixel Size'])
                fits_image.header['EXPTIME']=float(camera_params['Exposure Time'])
                fits_image.header['EGAIN']=float(camera_params['Gain'])
                fits_image.header['SITELAT']=float(camera_params['Latitude'])
                fits_image.header['SITELONG']=float(camera_params['Longitude'])
                
                # Extracts Meta information to Store in Dictionary  
                meta_dict={}
                for tag_id in exifdata:
                    tag=ExifTags.TAGS.get(tag_id,tag_id)
                    data=exifdata.get(tag_id)
                    if isinstance(data,bytes):
                        data.decode()
                    meta_dict[tag]= data
                img.close()
                
                
                
                if  'FocalLength' in meta_dict.keys() and camera_params['Over Write Meta'] is False:
                    fits_image.header['FOCALLEN']=meta_dict['FocalLength']
                if 'ExposureTime' in meta_dict.keys() and camera_params['Over Write Meta'] is False:
                    fits_image.header['EXPTIME']=meta_dict['ExposureTime']
                if 'ExposureTime' in meta_dict.keys() and camera_params['Over Write Meta'] is False:
                    fits_image.header['EXPTIME']=meta_dict['ExposureTime']

                # TODO: Add More Search Tags
                
                
                # FITS FILE TYPE
                if root==light_img_directory:
                    fits_image.header['IMAGETYP']='LIGHT'
                elif root==flat_image_directory:
                    fits_image.header['IMAGETYP']='FLAT'
                elif root==dark_image_directory:
                    fits_image.header['IMAGETYP']='DARK'
                elif root==bias_image_directory:
                    fits_image.header['IMAGETYP']='BIAS'
                
                
                fits_image.writeto(os.path.join(root,file.split('.')[0]+'.fits'))
                
                
GUI= gui()