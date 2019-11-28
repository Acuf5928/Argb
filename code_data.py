import os
import _thread
import time
import json

import code_language
import code_helper
import code_debug
import gui_errordb

class data:
    def __init__(self, db):
        #salvo la posizione del db
        self.db = db
        self.cont = True
        self.stop_order = False

        self.language_class = code_language.language("db_language.json", self)

        #effettuo un primo update
        self.update(sec = 0)

        if self.data["sep"] == "":                        
            self.sep_value = os.sep 

        #se l'utente non ha specificato un path il programma se lo ricava in autonomia
        #il primo check verrà fatto qui perchè in update fallirà dato che sep_value non è ancora calcolato
        if self.data["DownloadFolderPath"] == "":
            self.folderPath_value = code_helper.get_download_path() + self.sep_value

        self.debug_class = code_debug.debug(self.debug_clean_time(), self.debug_clean_element()) 
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "db_active"))                    
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "sep") + self.sep_value)                    
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "folder_path") + self.folderPath_value)

    def debug_add(self, txt, val = 0):
        try:
            self.debug_class.add(txt, val)
        except:
            pass

    def start_update(self, sec = 100):
        '''avvia l'update di tutti i dati ogni sec dato in un nuovo thread, se sec = 0 si aggiorna una sola volta'''
        _thread.start_new_thread(self.update, (sec, ))

    def update(self, sec):
        '''avvia l'update di tutti i dati ogni sec dato nel thread attuale, se sec = 0 si aggirna una sola volta, 
        non consigliato usare questa funzione direttamente ma solo attraverso start_update'''
        while True:
            try:
                with open(self.db, "r") as read_file:
                    self.data = json.load(read_file)                    
                    self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "db_read") + self.db) 

                    #se l'utente non ha specificato un path il programma se lo ricava in autonomia
                    #il primo check fallirà perchè sep_value non è ancora stato calcolato, il primo check verrà fatto in __init__
                    try:
                        if self.data["DownloadFolderPath"] == "":
                            self.folderPath_value = code_helper.get_download_path() + self.sep_value
                    except Exception:
                        pass        

                    self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "folder_path") + self.folderPath_value)
                    self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "update_complete"))
            
            except FileNotFoundError as ex:
                self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": db_error" + str(ex), 1)
                iWillSurvive = gui_errordb.Error_database()
                if iWillSurvive.spawn() == True:
                    self.update(0)

            except Exception as ex:
                self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "db_error") + str(ex), 1)

            if sec == 0:
                break
            
            else:
                time.sleep(sec)

            if self.cont == False:
                break
    
    def return_all(self):
        return self.data

    def set_all(self, new):
        self.data = new
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "restore_all"))

    def save(self):
        try:
            with open(self.db, "w") as write_file:
                json.dump(self.data, write_file, indent=4)
                self.language_class.update()
                self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "db_update"))
        
        except Exception as ex:
            self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "db_error") + str(ex), 1)

    def icon_color(self):
        return self.data["icon_color"]

    def gui(self):
        return self.data["gui"]

    def sep(self):
        return self.sep_value
    
    def debug_clean_time(self):
        return self.data["debug_clean_time"]

    def debug_clean_element(self):
        return self.data["debug_clean_element"]

    def s_language(self):
        return self.data["language"]
    
    def white_icon(self):
        return self.data["icon_white_theme"]

    def black_icon(self):
        return self.data["icon_black_theme"]

    def set_language(self, new):
        self.data["language"] = new
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "set_value") + "language: " + str(new))
 
    def set_debug_clean_time(self, new):
        self.data["debug_clean_time"] = new
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "set_value") + " debug_clean_time: " + str(new))

    def set_debug_clean_element(self, new):
        self.data["debug_clean_element"] = new
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "set_value") + " debug_clean_element: " + str(new))
    
    def set_sep(self, new):
        self.data["sep"] = new
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "set_value") + "sep: " + str(new))
    
    def set_database_update_cycle_wait_time(self, new):
        self.data["database_update_cycle_wait_time"] = new
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "set_value") + "database_update_cycle_wait_time: " + str(new))
    
    def set_gui(self, new):
        self.data["gui"] = new
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "set_value") + "gui: " + str(new))
    
    def set_icon_color(self, new):
        self.data["icon_color"] = new
        self.debug_add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.language_class.r_string(self.s_language(), "set_value") + "icon_color: " + str(new))
    