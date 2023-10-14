import pathlib
import re
import json


class JsonRead:
    def __init__(self):
        self.__Path = pathlib.Path.cwd()  # 获取当前文件夹路径
        self.__PathJson = []
        self.__PathJsonValue = []
        self.__PathJsonDir = {}

    def GetPathJson(self):  # 获取当前程序所在文件的所有json文件地址
        self.__PathJson = []
        for x in pathlib.Path(self.__Path).rglob('*.json'):
            self.__PathJson.append(x)
        return self.__PathJson

    def GetPathJsonValue(self):
        r = r"[\w]{0,}.json$"
        self.__PathJsonValue = []
        for x in pathlib.Path(self.__Path).rglob(r'*.json'):
            self.__PathJsonValue.append(re.search(r, str(x)).group())
        return self.__PathJsonValue

    def GetPathJsonDir(self):  # 生成{文件名:文件地址}的字典
        JsonValue = self.GetPathJsonValue()
        JsonPath = self.GetPathJson()
        n = 0
        for x in JsonValue:
            self.__PathJsonDir.setdefault(x, x)
            self.__PathJsonDir[x] = JsonPath[n]
            n += 1
        return self.__PathJsonDir


class OpenFile:
    def __init__(self):
        self.__Keys = []
        self.__file = None
        self.__json = {}

    def GetFileValue(self, filepath, retype):  # 获取文件信息
        with pathlib.Path(filepath).open(mode='r+', encoding='UTF-8') as file:
            self.__file = file.read()
        try:
            self.__json = json.loads(self.__file)
        except json.decoder.JSONDecodeError as e:
            print('空文件')
        if retype:
            return self.__json  # 返回dict
        else:
            return self.__file  # 返回字符串

    def CreateFile(self, filename, filedata):
        # filename 文件夹名称
        with pathlib.Path(filename).open(mode='w+', encoding='UTF-8') as f:
            json.dump(filedata, f, indent=4, ensure_ascii=False)

    def DictZJson(self, SDict):
        return json.dumps(SDict, indent=4, ensure_ascii=False)

    def StringZList(self, string):
        list1 = []
        str1 = ''
        for x in string:
            if x == '\n':
                list1.append(str1)
                str1 = ''
                continue
            str1 += x
        else:
            list1.append(str1)
        return list1
