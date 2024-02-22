# print filename
rtc=machine.RTC()
timestamp=rtc.datetime()
timestringfilename="FromFish%04d%02d%02d_%02d%02d%02d.csv"%(timestamp[0:3] + timestamp[4:7])
print(timestringfilename)