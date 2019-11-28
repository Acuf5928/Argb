import os
import _thread
import time
import json

class language:
    def __init__(self, language_file, data):
        #salvo la posizione del db
        self.db_str = language_file
        self.data = data
        #effettuo un primo update
        self.update()

    def update(self):
        try:
            with open(self.db_str, "r") as read_file:
                self.db = json.load(read_file)

        except Exception as ex:
            self.data.debug_class.add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.data.language_class.r_string(self.data.s_language(), "language_error") + str(ex), 1)

    def r_string(self, language, string):
        
        try:
            return self.db[language][string]

        except Exception as es:
            try:
                self.data.debug_class.add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.data.language_class.r_string(self.data.s_language(), "language_error_2") + str(es), 1)
                return self.db["eng"][string]
            
            except Exception as es:
                self.data.debug_class.add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.data.language_class.r_string(self.data.s_language(), "language_error_2") + str(es), 1)
                return "STRING NOT FOUND"         