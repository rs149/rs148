import  msvcrt

while True:
    if msvcrt.kbhit():
        a = msvcrt.getch()
        print(a)