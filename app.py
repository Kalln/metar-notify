import requests, datetime, time, threading
from termcolor import colored, cprint

metarUrl = "http://wx.ivao.aero/metar.php"
testing = False

# This basically prints stuff and displays it in terminal.
def printStuff(col, aerodrome, altimeter):
    cprint(aerodrome + " QNH:" + altimeter, col, attrs=['bold'])

#
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

def metarRequest():
    r = requests.get(metarUrl)
    Metar = r.text

    if (testing):
        with open("metar.txt", "r") as f:
            print(f.read())
        print("Loading local information")
        f.close()
    else:
        # Copy content of metar.txt to metarold.txt
        with open("metar.txt") as f:
            with open("oldmetar.txt", "w+") as copy:
                for line in f:
                    copy.write(line)
        f.close()
        copy.close()

        # Delete content of metar.txt, otherwise it will just add it to the other content.
        f = open("metar.txt", "w")
        f.close()

        # Content from website is saved in metar.txt
        with open("metar.txt", "r+") as f:
            for items in Metar:
                f.write(items)
            print(f.read())
        print("Using information from live server")
        f.close()

# Logic to look for when to look for a new METAR
# Starts by looking at current METAR and takes the current time and adds a requestedTime that is METAR +35 minutes.
def WhenToRequest():
    with open("metar.txt", "r") as f:
        for line in f:
            if line.startswith("ESSA"):
                dayOfMetar = line[5:7]
                latestTime = line[7:11]
                hour = latestTime[0:2]
                minute = latestTime[2:4]
                timestamp = datetime.timedelta(hours = int(hour), minutes = int(minute))
                addedTime = datetime.timedelta( minutes = 35)
                requestedTime = timestamp + addedTime
    f.close()

    print("METAR RECORDED DAY",dayOfMetar,"OF CURRENT MONTH")
    print("AT TIME",timestamp)
    print("NEXT METAR REQUESTED", requestedTime)

# Gets the current time of computer to compare to requestedTime.
    now = datetime.datetime.utcnow()
    dt_string = now.strftime("%H:%M:%S")
    currentTimeHour = dt_string[0:2]
    currentTimeMinute = dt_string[3:5]
    currentTime = datetime.timedelta(hours = int(currentTimeHour), minutes = int(currentTimeMinute))
    print("CURRENT TIME:", currentTime)
    print("SHOULD I LOOK FOR NEW METAR?", currentTime >= requestedTime)

# Used later for when to see for how long program has waited to run this.
    i = 1

# While PC time is less then requestedTime => sleep 10 seconds => IF the statement is more => We request new METAR.
# The PC time is requested every 10 seconds to get a updated time.
# A thread is used here so we can still do stuff at the same with another thread if we really want to.
    while not (currentTime >= requestedTime):
        now = datetime.datetime.utcnow()
        dt_string = now.strftime("%H:%M:%S")
        currentTimeHour = dt_string[0:2]
        currentTimeMinute = dt_string[3:5]
        currentTime = datetime.timedelta(hours = int(currentTimeHour), minutes = int(currentTimeMinute))
        
        if (currentTime >= requestedTime):
            print("IT'S TIME TO DO STUFF")
            break
        else:
            print("WAITING.... NOT YET")
            time.sleep(10)
            i += 1
            timeSlept = i * 10
            print("I have waited for a total of", timeSlept, "seconds.")

t1 = threading.Thread(target=WhenToRequest)  

t1.start()        

## TODO
## COMPARE OLD QNH WITH NEW QNH, AND DISPLAY RED COLOR
## SOMEWAY TO ACKNOWLEDGE THAT THERE HAS BEEN A NEW QNH, EITHER BY WRITING OR BY CLICKING.
## 
