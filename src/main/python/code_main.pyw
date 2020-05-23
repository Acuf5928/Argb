import gui_systray

from appContext import AppContext

if __name__ == '__main__':
    appctxt = AppContext()       # 1. Instantiate ApplicationContext
    gui_systray.main(appctxt)

