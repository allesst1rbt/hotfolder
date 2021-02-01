import sys 
import time
import os
import win32api
import win32print
import logging
import shutil
import ntpath
from glob import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path


def on_created(event):
    time.sleep(1)
    print('created '+ event.src_path)
    path =str(event.src_path)
    arraypath = path.split('\\')
    if path.find(".pdf") == -1:
        print("Ne pdf naum")
    else:
        if path.find('nota') == -1:
            print('nao e nota fiscal') 
        else: 
            impressoraVeia =win32print.GetDefaultPrinter()
            win32print.SetDefaultPrinter('Brother DCP-L5652DN Printer') 
        
            dst = os.path.join(r"C:/Users/Public/notas/",arraypath[-1])
            dst = dst.replace('/', '\\')
            src =(os.path.normpath(path_pai + arraypath[-1]))
            src = src.replace('/', '\\')
            copy2(src,dst)
            win32api.ShellExecute(0, "print", dst, None,  ".",  0) 
            win32print.SetDefaultPrinter(impressoraVeia) 
      
         
       
def copy2(src, dst, iteration=1000):
   for x in range(iteration):
	    with open(src, 'rb') as fsrc:
	        with open(dst, 'wb') as fdst:
		        fdst.write(fsrc.read())           

if __name__ == '__main__':
    event_handler = FileSystemEventHandler()

    event_handler.on_created = on_created
    global path_pai
    path_pai =str(Path.home())+'\\Downloads\\'
    observer = Observer()
    observer.schedule(event_handler,path_pai,recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('bye')
        observer.stop()
    observer.join()
