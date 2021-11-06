from datetime import datetime


def RealTime_Nama():
        now = datetime.now()
        dtString = now.strftime('%H%M%S')
        return dtString
def RealDate_Nama():
    now = datetime.now()
    dtString = now.strftime('%d%m%y')
    return dtString

def RealTime():
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        return dtString
def RealDate():
    now = datetime.now()
    dtString = now.strftime('%d/%m/%y')
    return dtString

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

def logDatang(name):
    with open('log/logData.csv', 'a') as f:
        if (name != 'unknown'):
            f.writelines(f'\n{RealDate()},{RealTime},{name},DATANG')
def logPulang(name):
    with open('log/logData.csv', 'a') as f:
        if (name != 'unknown'):
            f.writelines(f'\n{RealDate()},{RealTime},{name},PULANG')