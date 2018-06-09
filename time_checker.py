"""This is a module to check the time"""
import datetime

class CheckTime():
    """
    現在時刻とボスの湧き時間をチェックして返信を生成する
    """

    def __init__(self, json_data):
        self.json_data = json_data
        timedict = json_data["time"]
        self.time_a = datetime.time(int(timedict["a"].split(":")[0]), \
        int(timedict["a"].split(":")[1]))
        self.time_b = datetime.time(int(timedict["b"].split(":")[0]), \
        int(timedict["b"].split(":")[1]))
        self.time_c = datetime.time(int(timedict["c"].split(":")[0]), \
        int(timedict["c"].split(":")[1]))
        self.time_d = datetime.time(int(timedict["d"].split(":")[0]), \
        int(timedict["d"].split(":")[1]))
        self.time_e = datetime.time(int(timedict["e"].split(":")[0]), \
        int(timedict["e"].split(":")[1]))
        self.time_12am = datetime.time(0, 0)


    def info(self, weekday):
        """
        infoコマンドの返信を生成
        """
        title = "{}曜日のボスPOP".format(self.json_data["weekday"][str(weekday)])
        description = ""
        for key, value in sorted(self.json_data["time"].items()):
            bossname = self.json_data[str(weekday)][key]
            line = "\n**{0}** \n{1}".format(value, bossname)
            description += line

        return title, description


    def check_before30(self, now, time_key, weekday):
        """
        現在時刻が30分前、10分前かどうかを調べる
        30分前じゃなかったらres = Noneで返信無し
        ボス名Noneは無視
        """
        timedict = self.json_data["time"]
        poptime = datetime.time(int(timedict[time_key].split(":")[0]), \
        int(timedict[time_key].split(":")[1]))
        after30min = now + datetime.timedelta(minutes=30)
        time_after30 = datetime.time(after30min.hour, after30min.minute)
        after10min = now + datetime.timedelta(minutes=10)
        time_after10 = datetime.time(after10min.hour, after10min.minute)

        if self.json_data[str(weekday)][time_key] == "None":
            res = None

        else:
            if poptime == time_after30:
                res = "30分後に{}がわくよ！準備は良い？"\
                .format(self.json_data[str(weekday)][time_key])

            elif poptime == time_after10:
                res = "10分後に{}がわくよ！準備は良い？"\
                .format(self.json_data[str(weekday)][time_key])

            else:
                res = None

        return res


    def change_presence(self, time_key, weekday):
        """
        最短で湧くボスの時間を表示させる
        """
        poptime = self.json_data["time"][time_key]
        bossname = self.json_data[str(weekday)][time_key]

        nowplay = "{0} {1}　　　　　　　　　　　　　　　　　　　　."\
        .format(poptime, bossname)

        return nowplay


    def check_nextpop(self, now):
        """
        次の湧き時間を確認
        """
        nowtime = datetime.time(now.hour, now.minute)
        weekday = now.weekday()
        #比較
        if self.time_12am < nowtime <= self.time_a:
            time_key = "a"

        elif self.time_a < nowtime <= self.time_b:
            time_key = "b"

        elif self.time_b < nowtime <= self.time_c:
            time_key = "c"

        elif self.time_c < nowtime <= self.time_d:
            time_key = "d"

        elif self.time_d < nowtime <= self.time_e:
            time_key = "e"

        else:
            time_key = "a"
            weekday += 1

        return time_key, weekday
