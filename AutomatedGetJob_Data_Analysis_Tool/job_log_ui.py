from tkinter import *
import get_jobs_from_sap as jobslist
import os, sys
import datetime
import data_reports as rpt


def build_report():
    if len(v_filepath.get()) == 0:
        v_filepath.set(str(os.path.dirname(sys.argv[0])))
    if len(v_filename.get()) == 0:
        v_filename.set('JOBLIST_')

    rpt.build_html_rpt(v_filepath.get(), v_filename.get())

def get_jobs():
    if len(v_filepath.get()) == 0:
        v_filepath.set(str(os.path.dirname(sys.argv[0])))
    if len(v_filename.get()) == 0:
        v_filename.set('JOBLIST_')
    if len(v_user.get()) == 0:
        v_user.set(str(os.getlogin()))
    if len(v_sid.get()) == 0:
        v_sid.set('QTA')

    # the function will run the automation and return a list of tuples with jobs
    list_jobs = jobslist.get_jobs(v_filepath.get(), v_filename.get(), v_user.get(), v_sid.get())
    print(list_jobs)
    print('Job list created')


def get_canceled():
    if len(v_filepath.get()) == 0:
        v_filepath.set(str(os.path.dirname(sys.argv[0])))
    if len(v_filename.get()) == 0:
        minus_days = datetime.timedelta(days=6)  # a day object to be used to substract from entry
        default_date = datetime.datetime.today()
        newdate = default_date - minus_days  # create a newdate object with entry date minus the days specified
        newdate = newdate.strftime('%m%d%Y')
        v_filename.set(f'JOBLIST_{newdate}')
    if len(v_user.get()) == 0:
        v_user.set(str(os.getlogin()))
    if len(v_sid.get()) == 0:
        v_sid.set('QTA')

    jobslist.error_logs(v_filepath.get(), v_filename.get(), v_user.get(), v_sid.get())
    print('Canceled list created')


window = Tk()
window.wm_title('Job Log Importer')

lbl_user = Label(window, text='User Name: ')
lbl_user.grid(row=0, column=0)

lbl_sid = Label(window, text='SID/Server: ')
lbl_sid.grid(row=0, column=2)

lbl_filepath = Label(window, text='Save to: ')
lbl_filepath.grid(row=1, column=0)

lbl_filename = Label(window, text='FileName (w/o ext.): ')
lbl_filename.grid(row=1, column=2)

# v_optional = IntVar()
# chk_optional = Checkbutton(window, text='Get Canceled Jobs', variable=v_optional)
# chk_optional.grid(row=2, column=3)

v_user = StringVar()
p_user = Entry(window, textvariable=v_user)
p_user.grid(row=0, column=1)

v_sid = StringVar()
p_sid = Entry(window, textvariable=v_sid)
p_sid.grid(row=0, column=3)

v_filepath = StringVar()
p_filepath = Entry(window, textvariable=v_filepath)
p_filepath.grid(row=1, column=1)

v_filename = StringVar()
p_filename = Entry(window, textvariable=v_filename)
p_filename.grid(row=1, column=3)

btn_getjobs = Button(window, text='Step 1: Get Jobs', width=17, command=get_jobs)
btn_getjobs.grid(row=3, column=0)

btn_getcanc = Button(window, text='Step 2: Get Canceled', width=17, command=get_canceled)
btn_getcanc.grid(row=3, column=1)


btn_bldrpt = Button(window, text='Step 3: Build Report', width=17, command=build_report)
btn_bldrpt.grid(row=3, column=2)

window.mainloop()
#--End | github.com/eabdiel