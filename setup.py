from cx_Freeze import setup, Executable

setup(
        name="main",
        version=0.3,
        description="Gestor de Personagens",
        executables=[Executable(
                "main.py",
                base="Win32GUI",
                #icon="icon.ico",
                targetName='main.exe')])
