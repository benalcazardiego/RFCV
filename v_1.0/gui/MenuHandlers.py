#GUI_menu_handlers_for_file_management

from utils import save_ui_file
from utils import restore_ui_file
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QApplication 

    ## Lacks save option
def handle_save_as(ui):
    file_name = QFileDialog.getSaveFileName(ui.centralwidget, "Nombre del archivo", "~/untitled.config", "config files (*.config)")
    save_ui_file(ui, file_name)
    
def handle_save(ui):
    file_name = QFileDialog.getSaveFileName(ui.centralwidget, "Nombre del archivo", "~/untitled.config", "config files (*.config)")
    save_ui_file(ui, file_name)

def handle_open(ui):
    file_name = QFileDialog.getOpenFileName(ui.centralwidget, "Nombre del archivo", "~", "config files (*.config)")
    restore_ui_file(ui, file_name)

def handle_close(ui):
    QApplication.quit() 
