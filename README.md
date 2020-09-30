# sap_automation
Personal Projects related to SAP Automation
Required libs: sys, win32com.client, pyautogui
Win32com Recordings can be parsed from regular SAPGUI recordings - or manually made using the screen reader external program found on sapnote# 1441550

1) GetJobs automated data analysis tool - UI to trigger pyautogui automation to fetch custom jobs for last week, extracting the data into html, converting the html to csv for easier-to-handle dataset and the option to iterate through the data set to extract each failed job's log into separate csv files, grouped by date and named according to job_date for easier analysis.  -- this automation program doesnt require SAP scripting to be enabled.

2) SAP_guiscript_interaction - simple script that uses SAP's own 'recordings', the recordings are win32 ready and this is a sample of how to use them with python (it requires proper autorization in the system that you plan to execute - and sap scripting needs to be enabled)
