"""
Script to generate a txt file that contains the names of all the songs contained in 'MiBotiquin2024' folder
Contributor:
    Celina Soto
"""
# Import required modules
import os
import sys 
from pathlib import Path
from tinytag import TinyTag
import datetime



class AudioFilesList:
    ''' Description goes here'''

    def __init__(self):
        self.directory: str = r"C:\Users\dona_\Documents\Drive\Musicoterapia\IMMH\MiBotiquin2024"
        self.song_path: str = None
        self.song_title: str = None
                
    # Function to create files list 
    def create_list(self):
        # Assign directory
        #c:\Users\dona_\Documents\Python\Musicoterapia\MiBotiquinLista
        print(f"main directory: {self.directory}")
 
        # Create Error_Exec_Log_ActualDate.txt filename
        #log_file = os.path.join(self.directory, f"Error_Exec_Log_{datetime.date.today()}.txt")
        #log_file_path = os.path.join(self.directory, log_file) 
        #print(f"logs file path: {log_file_path}")

        for root, dirs, files in os.walk(self.directory, topdown=True):

            for file in files:
                self.song_path = os.path.join(root, file)
                print(f"song path: {self.song_path}")
      
                try:
                    #Read audio file metadata: Title
                    tag: TinyTag = TinyTag.get(self.song_path)
                    self.song_title = tag.title
                    print(f"Song title: {self.song_title}")
                
                except:
                    print(f"{self.song_path} is not am mp3 file")





Filelist = AudioFilesList()
Filelist.create_list()