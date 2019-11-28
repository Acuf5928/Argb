import os
import platform
from glob import glob

#questo file contiene varie funzioni utili

def get_download_path():
    """Version changes by me of the script that is located at https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder\n
    Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            return winreg.QueryValueEx(key, downloads_guid)[0]
    
    else:
        try:
            from gi.repository import GLib
            return GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
        except:
            return os.path.join(os.path.expanduser('~'), 'downloads')

def get_app_theme():
    """Returns the apps theme for windows"""
    import winreg
    sub_key = r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    key = 'AppsUseLightTheme'
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as s_key:
        return winreg.QueryValueEx(s_key, key)[0]

#apro il file dato e restituisco un array
def aprifile(percorso):
    try:
        with open(percorso, "r") as ptrfile:
            settings = ptrfile.readlines()
            return (settings)

    except:
        print("File non trovato")
        exit()

#aggiunge il testo dato al file dato
def scrivifile(text, percorso):
    try:
        with open(percorso, "a") as ptrfile:
            ptrfile.write("\n")
            ptrfile.write(str(text))

    except Exception as es:
        print("Impossibile scrivere il file" + str(es))

#restituisce una lista di file se il path dato contiene con *
#cartelle se folder è inpostato su True
#anche le sottocartelle se recursivee è su True e il path dato contiene con **
def list_file(folderPath, recursivee = False, folder = False):
    if folder == False:
        return glob(folderPath + ".*", recursive=recursivee)
    else:
        return glob(folderPath, recursive=recursivee)
    
#restituisce la data di creazione del file
def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime