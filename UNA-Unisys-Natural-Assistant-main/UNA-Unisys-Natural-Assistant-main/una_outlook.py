import win32com.client
import datetime
from collections import namedtuple

from O365 import Account, MSGraphProtocol


event = namedtuple("event", "Start Subject Duration")
#from here


CLIENT_ID = 'b80afe77-d004-4533-ae32-9a44b81bfa4b'
SECRET_ID = 'pVp5~Oc-oNLd2L6R8m~Qw~C_vXO59o2hTT'
credentials = (CLIENT_ID, SECRET_ID)



protocol = MSGraphProtocol() 
scopes = ['Calendars.Read']
account = Account(credentials, protocol=protocol)

if account.authenticate(scopes=scopes):
   print('Authenticated!')


def parse_event(event):
    event_str = str(event)
    start_index = event_str.find('from') + 6
    start = event_str[start_index: start_index + 8]
    start_obj = datetime.datetime.strptime(start, '%H:%M:%S') - datetime.timedelta(hours = 5, minutes = 30)
    end_index = event_str.find('to') + 4
    end = event_str[end_index: end_index + 8]
    end_obj = datetime.datetime.strptime(end, '%H:%M:%S') - datetime.timedelta(hours = 5, minutes = 30)
    sub_index = event_str.find(':')
    brac_index = event_str.find('(')
    subject = event_str[sub_index+1:brac_index]
    new_event = {"subject": subject, "from" : start_obj.time(), "to" : end_obj.time()}
    return(new_event)


'''q = calendar.new_query('start').greater_equal(datetime.datetime.today())
q.chain('and').on_attribute('end').less_equal(datetime.timedelta(days=1) + datetime.datetime.today())'''
schedule = account.schedule()
calendar = schedule.get_default_calendar()
events = calendar.get_events(include_recurring=False)
for event in events:
    new_event = parse_event(event)
    print(new_event["subject"], new_event["from"], new_event["to"])

print(calendar)