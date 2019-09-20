from tkinter import *

root = Tk()
metar = []

def metarGetter(wMetar):
    with open("metar.txt", "r") as f:
        for items in f:
            if items.startswith(wMetar):
                metarList.insert(END, items)

def metarRequest():
    metarList.delete(0, END)
    wanted = location.get()
    metarGetter(wanted)

def metarUpdater():
    return 0

metarList = Listbox(root)
metarList.pack(fill=X)

location = Entry(root)
location.pack()

metarBtn = Button(root, text="UPDATE", command=metarRequest)
metarBtn.pack()

l = Label(root, text="ESSA => NEW QNH 1008 ", fg="red")
l.pack()
l2 = Label(root, text="ESSB => QNH 1008 ", fg="green")
l2.pack()


root.mainloop()

# TODO Update METAR every 30 minutes. (Be able to look when the latest metar was taken and update +35 min after it).
# TODO Be able to see when new QNH comes in.