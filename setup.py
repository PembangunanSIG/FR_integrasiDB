from cx_Freeze import setup, Executable

base = None    

executables = [Executable("mainwindow.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "FR_final-1",
    options = options,
    version = "0.1",
    description = 'cuakse',
    executables = executables
)
