import sys
from termcolor import colored, cprint

print_green_bold = lambda x: cprint(x, 'green', attrs=['bold'], end='')
print_red_bold = lambda x: cprint(x, 'red', attrs=['bold'], end='')


def printStuff(col, aerodrome, altimeter):
    cprint(aerodrome + " QNH:" + altimeter, col, attrs=['bold'])

def printQNH():
    with open("metar.txt", "r") as f:
        for items in f:
            if items.startswith("ES"):
                apAltimeterIndex = items.find("Q1") or items.find("Q0")
                apAltimeterIndex = apAltimeterIndex + 1
                apAltimeterIndexEnd = apAltimeterIndex + 4
                QNH = items[apAltimeterIndex:apAltimeterIndexEnd]

                printStuff("green", items[0:4], str(QNH))
    f.close()

printQNH()