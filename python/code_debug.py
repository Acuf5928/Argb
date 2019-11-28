import _thread
import time

class debug:
    def __init__(self, debug_clean_time, debug_clean_element):
        self.data = {}
        _thread.start_new_thread(self.update, (debug_clean_time, debug_clean_element))

    def add(self, string, value = 0):
        self.data.update({str(string): value})

    def return_data(self):
        return self.data
    
    def clean(self):
        self.data = {}

    def update(self, sec, n_element):
        while True:
            if len(self.data) > n_element:
                len_data = len(self.data)
                n_delete = len_data - n_element
                self.data = self.data[n_delete:-1] 
                
            if sec == 0:
                break
            
            else:
                time.sleep(sec)
