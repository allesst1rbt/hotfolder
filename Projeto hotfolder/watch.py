import sys 
import time
import os
import win32api
import win32print
import logging
import shutil
from glob import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def on_created(event):
    print('created '+ event.src_path)
    path =str(event.src_path)
    arraypath = path.split('.')
    if path.find(".pdf") == -1:
        print("Ne pdf naum")
    else:
        impressoraVeia =win32print.GetDefaultPrinter()
        win32print.SetDefaultPrinter('EPSON L365 Series')
        pdf_dir = path
        shutil.move(pdf_dir, "C:/Users/Public/notas"+arraypath[1].strip('/\/')+'.'+arraypath[2].strip('/\/'))
        for f in glob("C:/Users/Public/notas"+arraypath[1].strip('/\/')+'.'+arraypath[2].strip('/\/'), recursive=True):
           win32api.ShellExecute(0, "print", f, None,  ".",  0)   
        win32print.SetDefaultPrinter(impressoraVeia) 
    exit          

if __name__ == '__main__':
    event_handler = FileSystemEventHandler()

    event_handler.on_created = on_created
  

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    observer.schedule(event_handler,path,recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('bye')
        observer.stop()
    observer.join()