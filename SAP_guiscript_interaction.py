# Script will attach to a currently logged in sap gui session - and execute a guiscript recording

# Similar recordings can be made with SAP Gui recorder (Download stand-alone version from sapnote# 1441550)

# -Libs
import sys, win32com.client


# -Main subroutine
def main():
    try:
        #We have to parse the original guirecording and initialize the variables;
        #-------------Initialization steps: this part would be needed on every standalone script and its the same
        #                                   for every recording

        SapGuiAuto = win32com.client.getObject("SAPGUI")
        if not type(SapGuiAuto) == win32com.client.CDispatch:
            return

        application = SapGuiAuto.GetScriptingEngine
        if not type(application) == win32com.client.CDispatch:
            SapGuiAuto = None
            return

        connection = application.Children(0)
        if not type(connection) == win32com.client.CDispatch:
            application = None
            SapGuiAuto = None
            return

        session = connection.Children(0)  # 0 for active session
                                          # if more than one session you can use name of login serv
        if not type(session) == win32com.client.CDispatch:
            connection = None
            application = None
            SapGuiAuto = None
            return
        #---------------End of initialization

        #actual recording starts here
        session.findById("wnd[0]/tbar[0]/okcd").text = "/nse16"
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/usr/ctxtDATABROWSE-TABLENAME").text = 'TADIR'
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/tbar[1]btn[8]").press()
    except:
        print(sys.exc_info()[0])  # this is just a general error = usually happens if the script
        # cant find the correct session, or a field name is wrong
    finally:
        session = None
        connection = None
        application = None
        SapGuiAuto = None


# Main
if __name__ == "__main__":
    main()

# End-- https://github.com/eabdiel
