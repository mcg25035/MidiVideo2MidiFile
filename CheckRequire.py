import os

def check_installed(package):
    try:
        __import__(package)
        return True
    except:
        return False

def check_pip():
    if os.system("pip") != 0:
        print("pip not found , install below packages manually :")
        print("midiutil")
        print("opencv-python")
        print("after install , run this script again")
    return False

def install_package(package):
    os.system("pip install " + package)

def correct_midiutil():
    print("correcting midiutil package...")
    target = __import__(name="midiutil")
    path = target.__file__.split("__init__.py")[0]
    os.remove(path+"MidiFile.py")

    with open("./MidiFile.py", "r") as f:
        midiutil_string = f.read()
    
    with open(path+"MidiFile.py", "w") as f:
        f.write(midiutil_string)
    
    with open(path+"repaired.tag", "w") as f:
        f.write("")

    print("midiutil package corrected")


def main():
    installed = {}
    print("checking installed packages...")
    installed["midiutil"] = check_installed("midiutil")
    print("1/2 scanned")
    installed["opencv-python"] = check_installed("cv2")
    print("2/2 scanned")
    if not (installed["midiutil"] and installed["opencv-python"]):
        print("checking pip...")
        if not check_pip():
            return
    i = 0
    for package in installed:
        if not installed[package]:
            print("installing packages...")
            install_package(package)
            i+=1
            print(str(i) + "/? installed")
    print("all packages installed")
    print("checking midiutil...")
    target = __import__(name="midiutil")
    path = target.__file__.split("__init__.py")[0]
    if not os.path.exists(path+"repaired.tag"):
        correct_midiutil()

    with open("./checked.tag", "w") as f:
        f.write("")


    print("preparing done , now you can run main.py!")

main()

    

    
    




    