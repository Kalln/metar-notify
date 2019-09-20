import datetime, time, threading

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

    now = datetime.datetime.utcnow()
    dt_string = now.strftime("%H:%M:%S")
    currentTimeHour = dt_string[0:2]
    currentTimeMinute = dt_string[3:5]
    currentTime = datetime.timedelta(hours = int(currentTimeHour), minutes = int(currentTimeMinute))
    print("CURRENT TIME:", currentTime)
    print("SHOULD I LOOK FOR NEW METAR?", currentTime >= requestedTime)

    i = 1

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
