from globals import datetime, pytz, time_format

print(datetime.now(pytz.timezone("Asia/Calcutta")).strftime(time_format))