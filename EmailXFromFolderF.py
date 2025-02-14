import win32com.client  #pywin23


class GetEmailX_FromFolderF:
    def __init__(self, x: int, f: str):
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        folders=f.split("\\")
        if len(folders)==2: self.inbox = outlook.Folders[folders[0]].Folders[folders[1]]
        if len(folders)==3: self.inbox = outlook.Folders[folders[0]].Folders[folders[1]].Folders[folders[2]]
        if len(folders)==4: self.inbox = outlook.Folders[folders[0]].Folders[folders[1]].Folders[folders[2]].Folders[folders[3]]
        self.messages = self.inbox.Items
        self.message = self.messages[len(self.messages)-x] #vorletzter Eintrag
        self.head_content = self.message.Subject #Betreff
        self.body_content = self.message.body #Inhalt
        self.order_info = self.body_content.split("{message}")[1] #filtert benötigte Infos, welche am Ende der Mail stehen
                                                                #nur wichtig für xml datei profekt



