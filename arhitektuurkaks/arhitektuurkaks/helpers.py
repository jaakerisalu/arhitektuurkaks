import datetime


def fake_log(string):
    with open("/home/jerisalu/Apps/arhitektuurkaks/arhitektuurkaks/static/log.txt", "a") as text_file:
        print("[{}]: {}".format(datetime.datetime.now().strftime("%H:%M @ %d/%m/%y"), string), file=text_file)
    text_file.close()
