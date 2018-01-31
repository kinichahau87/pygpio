import re
import os, errno


class Kpygpio():


    def setMode(self, mode):
        try:
            self.MODES.index(mode)
        except ValueError as e:
            raise ValueError('mode speficied does not exist: ' + mode)

    def __findVersion(self):
        fd = os.open(self.CPU_PROC_PATH, os.O_ASYNC | os.O_RDONLY)
        regex = r"Revision\s*:\s*[0-9a-f]*([0-9a-f]{4})"
        matches = 0
        line = os.read(fd, 4)
        cpuInfo = line
        while line != '':
            line = os.read(fd, 4)
            cpuInfo = cpuInfo + line
        os.close(fd)
        #match regular expression
        if re.search(regex,cpuInfo):
            itMatches = re.finditer(regex, cpuInfo)

            for matchNum, match in enumerate(itMatches):
                matchNum = matchNum + 1
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
            #match = re.search(regex,cpuInfo)
            print(int(match.group(groupNum), 16))
            if int(match.group(groupNum), 16) < 4:
                self.CURRENT_PIN = self.version1
            else:
                self.CURRENT_PIN = self.version2
            matches = 1

        return matches


    def __init__(self, mode=None):
        self.MODES = ["mode_rpi", "mode_bcm"]
        self.CURRENT_MODE = None
        self.CURRENT_PIN = None
        self.DIRECTIONS = {"in", "out", "low", "high"}
        self.EDGES = {"none", "rising", "falling", "both"}
        self.GROUND = "ground"
        self.GPIO_PATH = "/sys/class/gpio"
        self.CPU_PROC_PATH = "/proc/cpuinfo"
        self.version1 = {
            1: None, # 1=3.3v
            2: None, # 2=5v
            3: 0,
            4: None, # 4=5v
            5: 1,
            6: self.GROUND,
            7: 4,
            8: 14,
            9: self.GROUND,
            10: 15,
            11: 17,
            12: 18,
            13: 21,
            14: self.GROUND,
            15: 22,
            16: 23,
            17: None, # 17=3.3v
            18: 24,
            19: 10,
            20: self.GROUND,
            21: 9,
            22: 25,
            23: 11,
            24: 8,
            25: self.GROUND,
            26: 7
            }
        self.version2 = {
            1: None, # 1=3.3v
            2: None, # 2=5v
            3: 0,
            4: None, # 4=5v
            5: 1,
            6: self.GROUND,
            7: 4,
            8: 14,
            9: self.GROUND,
            10: 15,
            11: 17,
            12: 18,
            13: 21,
            14: self.GROUND,
            15: 22,
            16: 23,
            17: None, # 17=3.3v
            18: 24,
            19: 10,
            20: self.GROUND,
            21: 9,
            22: 25,
            23: 11,
            24: 8,
            25: self.GROUND,
            26: 7,
            27: None, # 27=ID_SD
            28: None, # 28=ID_SC
            29: 5,
            30: self.GROUND,
            31: 6
        }
        #setup gpio
        if mode != None:
            self.setMode(mode)
        else:
            self.setMode("mode_rpi")

        if self.__findVersion() == 0:
            raise ValueError('revision not found in proc path')

    def __exportPin(self, pin):
        path = GPIO_PATH + "/export"
        fd = os.open(path, os.O_ASYNC | os.O_RDWR)
        os.write(fd, pin)
        os.close(fd)

    def __setDirection(self, pin, direction):
        path = GPIO_PATH + "/gpio" + pin
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        fd = os.open(path + "/direction", os.O_ASYNC | os.O_RDWR)
        os.write(fd, direction)
        os.close(fd)

    def __setEdge(self, pin, edge):
        path = GPIO_PATH + "gpio" + pin
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        fd = os.open(path + "/edge", os.O_ASYNC | os.O_RDWR)
        os.write(fd, edge)
        os.close(fd)

    def __unexport(self, pin):
        path = GPIO_PATH + "/unexport"
        fd = open(path, os.O_ASYNC | os.O_RDWR)
        os.write(fd, pin)
        os.close(fd)

    def setup(self, channel, direction, edge=None):
        currentDirection = None
        currentEdge = None
        if (self.CURRENT_PIN[channel] == self.GROUND):
            print("pin is ground")
            raise ValueError("pin is used as ground")
        else if(self.CURRENT_PIN[channel] == None):
            print("pin is reserved")
        else:
            try:
                currentDirection = self.DIRECTIONS[direction]
            except ValueError as e:
                raise ValueError("invaid direction specified")

            try:
                if (edge != None):
                    currentEdge = self.EDGES[edge]
            except ValueError as e:
                raise ValueError("invalid edge specified")
            #consider BCM
            self.__exportPin(channel)
            self.__setDirection(channel, currentDirection)
            if (currentEdge != None):
                self.__setEdge(channel, currentEdge)

    def read(self, channel):
        path = self.GPIO_PATH + "/gpio" + channel
        fd = os.open(path, os.O_ASYNC | os.O_RDONLY)
        line = os.read(fd, 8)
        os.close(fd)
        return line

    def write(self, channel):
        path = self.GPIO_PATH + "/gpio" + channel
        fd = os.open(path, os.O_ASYNC | os.O_RDWR)
        los.write(fd, 8)
        os.close(fd)
