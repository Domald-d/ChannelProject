
import random
import os
import datetime
import json
from DataManager import DataManager
dm = DataManager()
now = datetime.datetime.now()
class ScriptVariables:
    pb_game_DiabloII = "D2DV"
    pb_game_DiabloIIExp = "D2XP"

    def __init__(self):
        self.pbUsers = None
        self.pbTopUsers = None
        self.pbActive = None
        self.pbLogged = None
        self.pbLastGameRequest = None
        self.pbLastRulesRequest = None
        self.pbLastProfileUpdate = None
        self.pbLastConnect = None
        self.ToldTodaytop = None
        self.TopUserRuns = None
        self.DailyResetDone = True


class pb_Game:
    def __init__(self):
        self.Name = ""
        self.Host = ""
        self.Started = now

    def Duration(self):
        current_time = datetime.datetime.now()
        duration = abs((current_time - self.Started).total_seconds())
        return duration
    
    def Class_Initialize(self):
        self.Started = now


class pb_Active:
    
    def __init__(self):
        self.Username = ""
        self.Nickname = ""
        self.Nametitle = ""
        self.InGame = False
        self.InGameNoLog = False
        self.GameObject = None
        self.Level = 0

        self.Runs = 0
        self.AvgRuns = 0
        self.RunsToday = 0
        self.Time = 0
        self.AvgTime = 0
        self.LastTime = 0
        self.LastGameName = ""

        self.Left = ""
        self.LastLog = ""

    def EmptyGame(self):
        if not self.InGame:
            return
        self.GameObject = pb_Game()
        self.InGame = False
        self.LastTime = self.GameObject.Duration()
        self.LastGameName = self.GameObject.Name
    
    def FormatString(self,Message, Game):
        m = Message
        try:
            if Game:
                a = ["%user","%name","%title","%nick","%lvl","%avg","%cavg","%runs","%gametime","%game"]
                b = [self.PreferedName(), self.Username, self.Nametitle, self.Nickname, self.Level,
                     self.pb_FmtTime(self.Average()), self.pb_FmtTime(self.CurrAverage()), self.Runs,
                     self.pb_FmtTime(self.GameObject.Duration()), self.GameObject.Name]
            else:
                a = ["%user", "%name", "%title", "%nick", "%lvl",
                     "%avg", "%runs"]
                b = [self.PreferedName(), self.Username, self.Nametitle, self.Nickname, self.Level,
                     self.pb_FmtTime(self.Average()), self.Runs]
        except Exception as e:
            data = {"error_message": f"[Bo$$] Format Error {str(e)}"}
            Serial = json.dumps(data)
            print(f"[Bo$$] Format error: {str(e)}")
            return m

        for i in range(len(a)):
            m = m.replace(a[i], b[i])

        return m
    
    def GameTimeOK(self,d):
        if d < pb_Get("main","MinGame") or d > pb_Get("main","MaxGame"):
            return False
        return True
    
    def Save(self):
        if self.Nickname == "":
            self.Nickname = self.Username
        
        dm.uppfaeraNotenda(self.Username,self.Nickname,self.Nametitle,self.Level,self.Runs,self.RunsToday,self.Time)

    def MutualFriend(self):
        return self.pb_Mutual(self.Username)
    
    def Friend(self):
        return self.pb_Friend(self.Username)
    

    def pb_Mutual(self, Username):
        pb_Mutual = False
        for Friend in Friends:
            if Friend.Name.lower() == Username.lower():
                if Friend.IsMutual:
                    pb_Mutual = True
                    break
        return pb_Mutual

    def pb_Friend(self, Username):
        pb_Friend = False
        for Friend in Friends:
            if Friend.Name.lower() == Username.lower():
                pb_Friend = True
                break
        return pb_Friend
    
    def Average(self):
        if self.Runs == 0 or self.Time == 0:
            return 0
        return int(self.Time/self.Runs)
    
    def CurrAverage(self):
        if self.AvgRuns == 0 or self.AvgRuns == 0:
            return 0
        return int(self.AvgTime/self.AvgRuns)
    
    def PreferedName(self):
        if self.Nametitle == "":
            return self.Nickname
        return f"{self.Nametitle} {self.Nickname}"
    
    def Class_Initialize(self):
        self.Nametitle = ""
        self.InGame = False
        self.GameObject = None
        self.Runs = 0
        self.RunsToday = 0
        self.Time = 0
        self.LastTime = 0
        self.AvgRuns = 0
        self.AvgTime = 0
        self.LastGameName = "Invalid"
        self.LastLog = self.DateAdd("s", -self.pb_Get("main", "MsgNoSpam"), now)


class pb_User:
    def __init__(self):
        self.Username = ""
        self.Runs = 0

def AddActive(Username, fcreate):
    if Username in pb_Active:
        return True
    
    user_exists = dm.UserExists(Username)

    if user_exists:
        user_data = dm.GetUserByUsername(Username)
        if user_data:
            ScriptVariables.pbActive[Username] = pb_Active()
            active = ScriptVariables.pbActive[Username]
            active.Username = user_data[0]
            active.Nickname = user_data[1]
            active.Nametitle = user_data[2]
            active.Level = user_data[3]
            active.Runs = user_data[4]
            active.RunsToday = user_data[5]
            active.Time = user_data[6]
            active.AvgRuns = 0
            active.AvgTime = 0
            return True
    if fcreate:
        dm.BuaTilNotanda(Username,Username,"",1,0,0,0.0)

        user_data = dm.GetUserByUsername(Username)

        if user_data:
            ScriptVariables.pbActive[Username] = pb_Active()
            active = ScriptVariables.pbActive[Username]
            active.Username = user_data[0]
            active.Nickname = user_data[1]
            active.Nametitle = user_data[2]
            active.Level = user_data[3]
            active.Runs = user_data[4]
            active.RunsToday = user_data[5]
            active.Time = user_data[6]
            active.AvgRuns = 0
            active.AvgTime = 0
            return True

    return False

    '''path = f"bcp_users/{Username.lower()}.user"

    if os.path.exists(path):
        ScriptVariables.pbActive[Username] = pb_Active()
        active = ScriptVariables.pbActive[Username]
        active.Username = Username
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                if key == "Nickname":
                    active.Nickname = value
                elif key == "Nametitle":
                    active.Nametitle = value
                elif key == "Level":
                    active.Level = int(value)
                elif key == "Runs":
                    active.Runs = int(value)
                elif key == "RunsToday":
                    active.RunsToday = int(value)
                elif key == "Time":
                    active.Time = int(value)
        active.AvgRuns = 0
        active.AvgTime = 0
        return True
    elif fcreate:
        ScriptVariables.pbActive[Username] = pb_Active()
        active = ScriptVariables.pbActive[Username]
        active.Username = Username
        active.Nickname = Username
        active.Nametitle = ""
        active.Level = 1
        return True
    else:
        return False
    '''
    
