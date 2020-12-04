#Notes: SM37 layout shouldnt include spool and jobdoc columns; recommended to change layout if report button is to
#       be used.

#Modules
import pyautogui as pgui
import time as t
import pyperclip
import datetime as DT
import bs4
import csv


def get_jobs(filepath, filename, username, serversid):
    # open SAP
    pgui.hotkey("win")
    t.sleep(5)
    pgui.typewrite("SAP Logon")
    t.sleep(1)
    pgui.hotkey("Enter")
    # give enough time for sap logon pad to open; default 5 seconds
    t.sleep(5)
    # after loading, press ctrl+f to go to search bar
    pgui.hotkey("ctrl", "f")
    t.sleep(3)
    backcounter = 0
    while backcounter < 10:
        pgui.hotkey("backspace")
        backcounter += 1

    # wait a few seconds to move cursor - then type server or SID name
    t.sleep(2)
    pgui.typewrite(serversid)
    pgui.hotkey('enter')
    # wait a few seconds for buffer to finish loading, then press enter to login
    t.sleep(2)
    pgui.typewrite('010')
    pgui.hotkey("Tab")
    pgui.typewrite(username)
    # submit a few times in case an informational popup appears
    entersleep = 0
    while entersleep < 5:
        t.sleep(1)
        pgui.hotkey('enter')
        entersleep += 1

    # SAP Automation Steps start here ---
    pgui.hotkey('ctrl', '/')
    t.sleep(3)
    pgui.typewrite('/nsm37')
    pgui.hotkey('enter')
    t.sleep(3)
    pgui.typewrite('Z80*')
    pgui.hotkey('tab')
    t.sleep(3)
    pgui.typewrite('*')
    pgui.hotkey('tab')  # move from user name field
    pgui.hotkey('tab')  # move from shed field
    pgui.hotkey('tab')  # move from released field
    pgui.hotkey('tab')  # move from ready field
    pgui.hotkey('tab')  # move from active field
    pgui.hotkey('tab')  # move from finished field
    pgui.hotkey('tab')  # move from cancelled field
    t.sleep(1)  # give a few seconds to ctrl - copy
    pgui.hotkey('ctrl', 'a')  # select date
    pgui.hotkey('ctrl', 'c')  # copy from date
    t.sleep(1)

    # Start- Input Date formatting
    paste_date = pyperclip.paste()  # paste date in MMDDYYYY
    date = DT.datetime.strptime(paste_date, '%m/%d/%Y')  # convert to date object
    minus_days = DT.timedelta(days=30)  # a day object to be used to substract from entry
    newdate = date - minus_days  # create a newdate object with entry date minus the days specified
    newdate_formatted = newdate.strftime('%m/%d/%Y')  # new formatted day should be pasted date - 6 days
    filenamedate = newdate.strftime('%m%d%Y')
    # End- Input Date formatting


    # Continue automation
    t.sleep(1)
    pgui.hotkey('ctrl', 'a')
    pgui.typewrite(newdate_formatted)
    pgui.hotkey('f8')
    t.sleep(1)

    # at this point we should be at the sm37 job results screen
    pgui.hotkey('altleft', 'a')  # go to 'extras'
    t.sleep(1)
    pgui.typewrite('e')
    t.sleep(1)
    pgui.typewrite('l')
    t.sleep(1)
    pgui.hotkey('down')
    pgui.hotkey('down')
    pgui.hotkey('down')
    pgui.hotkey('enter')  # save to html
    t.sleep(2)
    pgui.press('right')
    pgui.press('up')
    t.sleep(1)
    pgui.hotkey('ctrl', 'a')
    t.sleep(2)
    path = filepath
    t.sleep(1)
    pgui.typewrite(path)
    t.sleep(1)
    pgui.hotkey('tab')
    t.sleep(1)
    pgui.typewrite(f'{filename}{filenamedate}.html')
    t.sleep(1)
    pgui.hotkey('enter')
    t.sleep(3)
    pgui.hotkey('ctrl', 's')
    t.sleep(1)
    pgui.hotkey('alt', 'f4')
    t.sleep(1)
    pgui.hotkey('tab')
    t.sleep(1)
    pgui.hotkey('enter')  # close sap

    # Data processing step here
    data = []
    soup = bs4.BeautifulSoup(open(f'{filename}{filenamedate}.html'), 'html.parser')
    table = soup.find('table', attrs={'class': 'list'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    # data here has the values from the table in the html
    # save this to csv for easier data analysis later
    data[0].pop(1) #spool not needed
    data[0].pop(1) #doc number not needed
    data[0][0] = 'JobName'
    data[0][1] = 'CreatedBy'
    data[0][2] = 'Status'
    data[0][3] = 'StartDate'
    data[0][4] = 'StartTime'
    data[0][5] = 'Duration'
    data[0][6] = 'Delay'
    with open(f'{filename}{filenamedate}.txt', 'w', newline='') as fou:
        cw = csv.writer(fou)
        cw.writerows(data)
    return data


def error_logs(filepath, filename, username, serversid):
    # Data processing step here
    data = []
    soup = bs4.BeautifulSoup(open(f'{filename}.html'), 'html.parser')
    table = soup.find('table', attrs={'class': 'list'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    data[0].pop(1)
    data[0].pop(1)
    data[0][0] = 'JobName'
    data[0][1] = 'CreatedBy'
    data[0][2] = 'Status'
    data[0][3] = 'StartDate'
    data[0][4] = 'StartTime'
    data[0][5] = 'Duration'
    data[0][6] = 'Delay'
    # data here has the values from the table in the html
    # save this to csv for easier data analysis later
    with open(f'{filename}.txt', 'w', newline='') as fou:
        cw = csv.writer(fou)
        cw.writerows(data)

    # open SAP once
    pgui.hotkey("win")
    t.sleep(5)
    pgui.typewrite("SAP Logon")
    pgui.hotkey("Enter")
    # give enough time for sap logon pad to open; default 5 seconds
    t.sleep(3)
    # after loading, press ctrl+f to go to search bar
    pgui.hotkey("ctrl", "f")
    t.sleep(2)
    backcounter = 0
    while backcounter < 10:
        pgui.hotkey("backspace")
        backcounter += 1

    # wait a few seconds to move cursor - then type server or SID name
    t.sleep(2)
    pgui.typewrite(serversid)
    pgui.hotkey('enter')
    # wait a few seconds for buffer to finish loading, then press enter to login
    t.sleep(2)
    pgui.typewrite('010')
    pgui.hotkey("Tab")
    pgui.typewrite(username)
    # submit a few times in case an informational popup appears
    entersleep = 0
    while entersleep < 4:
        t.sleep(1)
        pgui.hotkey('enter')
        entersleep += 1

    # iterate through the csv file where lines = cancelled
    # perform screen loop to get separate files for each 'cancelled' job
    for job in data:
        if job[2] == 'Canceled':

            job_name = job[0]
            start_date = job[3]
            start_time = job[4]

            # Start- Input Date formatting
            date = DT.datetime.strptime(start_date, '%m/%d/%Y')  # convert to date object
            filenamedate = date.strftime('%m%d%Y')
            # End- Input Date formatting

            # SAP Automation Steps start here ---
            pgui.hotkey('ctrl', '/')
            t.sleep(1)
            pgui.typewrite('/nsm37')
            pgui.hotkey('enter')
            t.sleep(1)
            pgui.typewrite(job_name)  # jobname here
            pgui.hotkey('tab')
            t.sleep(1)
            pgui.typewrite('*')
            pgui.hotkey('tab')  # move from user name field
            pgui.hotkey('tab')  # move from shed field
            pgui.hotkey('space')  # clear released field
            pgui.hotkey('tab')  # move from released field
            pgui.hotkey('space')  # clear ready field
            pgui.hotkey('tab')  # move from ready field
            pgui.hotkey('space')  # clear active field
            pgui.hotkey('tab')  # move from active field
            #pgui.hotkey('space')  # clear finished field
            pgui.hotkey('tab')  # move from finished field
            pgui.hotkey('tab')  # move from cancelled field
            t.sleep(1)  # give a few seconds to ctrl - copy
            pgui.hotkey('ctrl', 'a')  # select date
            pgui.hotkey('ctrl', 'c')  # copy from date
            t.sleep(1)

            t.sleep(1)
            pgui.hotkey('ctrl', 'a')
            pgui.typewrite(start_date)
            pgui.hotkey('tab')
            pgui.hotkey('ctrl', 'a')
            pgui.typewrite(start_date)
            pgui.hotkey('tab')
            t.sleep(2)
            # Input Time formatting
            v_time = DT.datetime.strptime(start_time, '%H:%M:%S')
            minus_second = DT.timedelta(seconds=1)
            v_timeminusone = v_time - minus_second
            v_start_time = v_timeminusone.strftime('%H:%M:%S')
            # End - input time formatting
            pgui.typewrite(v_start_time)
            pgui.hotkey('tab')
            pgui.typewrite(start_time)
            pgui.hotkey('f8')
            t.sleep(1)

            # at this point we should be at the sm37 job results screen
            pgui.hotkey('f5')  # go to 'extras'
            t.sleep(1)
            pgui.hotkey('ctrl', 'shift', 'f11')
            t.sleep(1)
            pgui.hotkey('shift', 'f6')
            t.sleep(1)
            pgui.hotkey('down')
            pgui.hotkey('down')
            pgui.hotkey('down')
            pgui.hotkey('enter')  # save to html
            t.sleep(2)
            pgui.press('right')
            pgui.press('up')
            t.sleep(1)
            pgui.hotkey('ctrl', 'a')
            t.sleep(1)
            path = filepath
            pgui.typewrite(f'{path}/Job_Reports/Error_Logs/{filenamedate}')
            t.sleep(1)
            pgui.hotkey('tab')
            pgui.typewrite(f'{job_name}_{filenamedate}.html')
            t.sleep(1)
            pgui.hotkey('enter')
            t.sleep(5)
            pgui.hotkey('ctrl', 's')
            t.sleep(1)

            # Data processing step here
            data = []
            soup = bs4.BeautifulSoup(open(f'{filepath}/Job_Reports/Error_Logs/{filenamedate}/{job_name}_{filenamedate}.html'), 'html.parser')
            table = soup.find('table', attrs={'class': 'list'})
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            # data here has the values from the table in the html
            # save this to csv for easier data analysis later
            with open(f'{filepath}/Job_Reports/Error_Logs/{filenamedate}/{job_name}_{filenamedate}.txt', 'w', newline='') as fou:
                cw = csv.writer(fou)
                cw.writerows(data)
        else:
            continue
#--End | github.com/eabdiel
