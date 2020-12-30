from screeninfo import get_monitors, Enumerator
for m in get_monitors(Enumerator.OSX):
    print(str(m))