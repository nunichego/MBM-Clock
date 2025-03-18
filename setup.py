from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["PyQt5"],
}

setup(
    name = "hello_world",
    version = "0.1",
    description = "Hello World PyQt5 App",
    options = {"build_exe": build_exe_options},
    executables = [Executable("hello_world.py", base="Win32GUI")]
)