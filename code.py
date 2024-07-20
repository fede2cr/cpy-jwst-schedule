import time
import adafruit_connection_manager
import adafruit_ntp
import wifi
from adafruit_datetime import datetime, date
from adafruit_magtag.magtag import MagTag

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
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0)
ntp_time = ntp.datetime

def jwst_sched_parse():
    '''
    Format is: chars and column
    13 VISIT ID
    10 PCS MODE
    29 VISIT TYPE
    58:79 SCHEDULED START TIME
    80:91 DURATION
    51 SCIENCE INSTRUMENT AND MODE
    31 TARGET NAME
    30 CATEGORY
    32 KEYWORDS
    '''
    sched_file = open('20240715_report_20240712.txt', 'r')
    Lines = sched_file.readlines()
    line_count=0
    reg_count=0

    sched = { }
    for line in Lines:
        line_count+=1
        find_date = line.find('2024')
        if len(line) > 1 and line_count > 4 and find_date != -1:
            start_time = line[58:78]
            duration = line[80:91]
            instrument = line[93:144]
            target = line[145:176]
            category = line[178:208]
            comment = line[210:]
            #print("|"+comment+"|")
            sched[reg_count] = {"start_time": time_parse(start_time),
                                 "duration": duration,
                                 "instrument": instrument,
                                 "target": target,
                                 "category": category,
                                 "comment": comment
                                }
            reg_count+=1
            #time.sleep(5)
    return sched

def time_parse(file_time):
    return time.struct_time((int(file_time[0:4]),
                             int(file_time[5:7]), int(file_time[8:10]),
                             int(file_time[11:13]), int(file_time[14:16]), int(file_time[17:19]),
                             0, 0, -1))    

sched = jwst_sched_parse()
count = 0

while True:
    sched_line = sched[count]
    if time.mktime(ntp_time) > time.mktime(sched_line["start_time"]):
        print(">")
    else:
        print("<")

        magtag.set_text("Current time: " + str(datetime.fromtimestamp(time.mktime(ntp_time))) + "\n" +
                    "Duration: " + sched_line["duration"] + "\n" +
                    "Instrument: " + sched_line["instrument"] + "\n" +
                    "Target: " + sched_line["target"] + "\n" +
                    "Category: " + sched_line["category"] + "\n" +
                    "Comment: " + sched_line["comment"])
        time.sleep(120)
        magtag.exit_and_deep_sleep(1800)

    count+=1
#    time.sleep(1)

