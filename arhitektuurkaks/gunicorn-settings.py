#bind = "0.0.0.0:8000"
bind = "unix:/tmp/gunicorn_arhitektuurkaks.sock"

workers = 2
proc_name = "arhitektuurkaks"
#loglevel = 'debug'
