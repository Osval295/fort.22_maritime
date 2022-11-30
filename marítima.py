import pandas as pd
from glob import glob
from tkinter import filedialog, ttk, messagebox
import os
import tkinter as tk

def load_folder():
    return filedialog.askdirectory()

def load_wgrib2():
    ruta_file = filedialog.askopenfilename(initialdir = "{os.getcwd()}",
                                      title = "Seleccione el fichero wgrib2.exe",
                                      filetypes = (("Fichero wgrib2", "wgrib2.exe"), ))
    return os.path.dirname(ruta_file)

def run1():
    global wgrib2
    wgrib2 = load_wgrib2()

def run2(wgrib2):
    global folder, f0_list,ii, salida,fort22
    folder = load_folder()
    os.chdir(folder)
    f0_list = [ii for ii in glob('*.f0*') if len(ii.split('.')[-1]) == 4]
    os.chdir(wgrib2)
    for ii in f0_list:
        subprocess.run(['wgrib2', os.path.join(folder,ii), '-csv', os.path.join(folder,ii) + '.csv'],
                       shell=True, capture_output=True, text=True)
    os.chdir(folder)
    files = glob('*.csv')
    fort22 = pd.DataFrame()
    for ii in files:
        file = pd.read_csv(ii, header=None)
        UGRD = file.copy()[file[2] == 'UGRD'].sort_values(by=[4,5,4], ascending=[True,False,True], ignore_index=True)[6].rename('UGRD')
        VGRD = file.copy()[file[2] == 'VGRD'].sort_values(by=[4,5,4], ascending=[True,False,True], ignore_index=True)[6].rename('VGRD')
        PRMSL = file.copy()[file[2] == 'PRMSL'].sort_values(by=[4,5,4], ascending=[True,False,True], ignore_index=True)[6].rename('PRMSL')
        salida = pd.concat([UGRD, VGRD, PRMSL], axis=1)
        salida.to_csv(ii[:-4] + '.txt', index=False, header=False)
        fort22 = pd.concat([fort22,salida])
    fort22.to_csv('fort.22', index=False, header=False)
    fiche = os.path.join(folder, "fort.22").replace('\\','/')
    messagebox.showinfo('Resultado: Ejecución completada',f'Revise el fichero\n{fiche}\n\nAllí encontrará los datos')
root = tk.Tk()
l1 = ttk.Label(text='Busque la carpeta donde se encuentra el fichero wgrib2.exe')
b1 = ttk.Button(text='Explorar', comman=lambda:run1())
l2 = ttk.Label(text='Busque la ubicación de los ficheros')
b2 = ttk.Button(text='Explorar y ejecutar', comman=lambda:run2(wgrib2))
l1.pack()
b1.pack()
l2.pack()
b2.pack()
root.mainloop()
