import time
import adafruit_connection_manager
import adafruit_ntp
import wifi
from adafruit_magtag.magtag import MagTag

'''
TODO:
- date comparison (it's prints the complete list, for now)
- turn on deep sleep
- download schedule file: https://www.stsci.edu/files/live/sites/www/files/home/jwst/science-execution/observing-schedules/_documents/20240715_report_20240712.txt
- code clean up
'''

magtag = MagTag()

magtag.add_text(
    text_position=(
        10, 50,
#        (magtag.graphics.display.width // 2) - 1,
#        (magtag.graphics.display.height // 2) - 20,
    ),
    #text_color=0xFFFFFF,
    #text_wrap=44,
    #text_maxlen=180,
    #line_spacing=1.0,
    #text_anchor_point=(0.5, 0.5),
    text_scale=1,
)


def jwst_sched_parse():
    sched_file = open('20240715_report_20240712.txt', 'r')
    Lines = sched_file.readlines()
    line_count=0

    sched = { }
    for line in Lines:
        line_count+=1
        if len(line) > 1 and line_count > 4:
            start_time = line[58:78]
            duration = line[80:91]
            instrument = line[93:144]
            target = line[145:176]
            category = line[178:208]
            comment = line[210:]
            sched[line_count] = {"start_time": start_time,
                                 "duration": duration,
                                 "instrument": instrument,
                                 "target": target,
                                 "category": category,
                                 "comment": comment
                                }
            #time.sleep(5)
    return sched

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0)
sched = jwst_sched_parse()
print(ntp.datetime)
print(dir(ntp.datetime)) # 2024-07-15T06:03:54Z
current_time = (str(ntp.datetime.tm_year)+"-"+
                str("{:02d}".format(ntp.datetime.tm_mon))+"-"+
                str("{:02d}".format(ntp.datetime.tm_mday))+"T"+
                str("{:02d}".format(ntp.datetime.tm_hour))+":"+
                str("{:02d}".format(ntp.datetime.tm_min))+":"+
                str("{:02d}".format(ntp.datetime.tm_sec))+"Z"
               )
print(current_time)

#print(sched)
count = 5
while True:
    sched_line = sched[count]
    magtag.set_text("Current time: " + current_time + "\n" +
                    sched_line["start_time"] + " during: " + 
                    sched_line["duration"] + "\n" +
                    sched_line["instrument"] + "\n" +
                    sched_line["target"] + "\n" +
                    sched_line["category"] + "\n" +
                    sched_line["comment"])
    count+=1
    time.sleep(10)
#magtag.exit_and_deep_sleep(10)
