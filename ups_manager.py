#! /usr/bin/python

import subprocess
import datetime
import os

time_log = '/var/log/time_log.log'
current_time = datetime.datetime.now() 
minute_limit = 15


def ShutDown():
    '''Handles shutting down the server once the time limit has been reached.
    '''
    
    print '[%s] CyberPower | Power has been out for greater than: %s minutes. Shutting Down!' % (current_time, minute_limit)
    os.system("shutdown now -h")


def GetUpsStatus():
    '''Parses the UPS status.
    Args:
        N/A
    Returns:
        ups_status - A string
    '''

    print '[%s] CyberPower | Checking UPS and home power status' % current_time
    ups_string = subprocess.check_output(['/usr/local/bin/pwrstat', '-status']).splitlines()[11]
    ups_status = ' '.join(ups_string.split(' ')[-2:])
    
    return ups_status


def CheckTimeLog():
    '''Checks if the time log is empty.
    Args:
        N/A
    Returns:
        True - If time log is empty
        False - If time log is not empty
    '''

    return(os.stat(time_log).st_size != 0)


def CheckUpsStatus(ups_status):
    '''Detects if there is a power outage.
    Args:
        ups_status - A string that determines if power is up or not.
    Returns:
        have_power - True if power is normal. False if there is a power outage.
        CheckTimeLog() - A function - See the function above for more info.
    '''

    have_power = True
    if ups_status != 'Utility Power':
        print '[%s] CyberPower | Power outage detected! Checking %s' % (current_time, time_log)
        have_power = False
    else:
        print '[%s] CyberPower | Power is normal' % current_time
       
    return (have_power, CheckTimeLog())


def ManageTimeLog(have_power, time_log_status):
    '''Manages the time log, and will also handle shutting down the server.

    If the time limit set by the variable minute_limit has been reached, the
    server will be shut down.

    Args:
        have_power - A boolean determining if power is lost or not.
        time_log_status - A boolean determining if the log is empty or not.
    Returns:
        N/A
    '''

    if have_power and time_log_status:
        print '[%s] CyberPower | Power has restored. Clearing time log: %s' % (current_time, time_log)
        open(time_log, 'w').close()
    elif not have_power:
        with open(time_log) as f:
            minutes = f.readlines().length
        if minutes > minute_limit:
            ShutDown()
        else:
            print '[%s] CyberPower | Power is still out. Logging to time log: %s' % (current_time, time_log)
            time_file = open(time_log, 'a')
            time_file.write('Power Out! =(')
            time_file.close()
        

def main():
    ups_stat = GetUpsStatus()
    stats = CheckUpsStatus(ups_stat)
    ManageTimeLog(stats[0], stats[1])


if __name__ == '__main__':
    main()
