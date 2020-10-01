# sap_automation
Personal Projects related to SAP Automation
Required libs: sys, win32com.client, pyautogui
Win32com Recordings can be parsed from regular SAPGUI recordings - or manually made using the screen reader external program found on sapnote# 1441550

1) AutomatedGetJob_Data_Analysis_Tool - UI to trigger pyautogui automation to fetch custom jobs for last week, extracting the data into html, converting the html to csv for easier-to-handle dataset and the option to iterate through the data set to extract each failed job's log into separate csv files, grouped by date and named according to job_date for easier analysis.  -- this automation program doesnt require SAP scripting to be enabled.

  Expected job_log output csv format   - ZJOBNAME,USER_THAT_EXECUTED,STATUS,MM/DD/YYYY,TIME:HH:MM:SS
  Expected canceled_job_log csv format - JobName,JobCreatedB,Status,Startdate,StartTime,Duration(sec.),Delay(sec.)
  
  Report module will create a graph with cancelation tendencies - based on each week's worth of information, the report is generated and exported to html with three data models 

2) SAP_guiscript_interaction - simple script that uses SAP's own 'GUI recordings', the recordings are win32 ready and this is a sample of how to use them with python (it requires proper autorization in the system that you plan to execute - and sap scripting needs to be enabled)
