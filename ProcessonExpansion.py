import requests
import json
import re


class User:
    API = {
        "login": "https://www.processon.com/login",
        "createFlow": "https://www.processon.com/diagraming/new?category=flow",
        "MaxChart": "https://www.processon.com/view/privatefilecount",
        "mvTrash": "https://www.processon.com/folder/to_trash",
        "delete": "https://www.processon.com/folder/remove_from_trash",
        "dolike": "https://www.processon.com/view/dolike"
    }

    def setHelpList(self, helperList):
        """
        帮忙点赞的小号列表
        :param helperList:
        """
        self.helperList = helperList

    def expand(self):
        """
        扩容一次
        """
        # 创建流程图
        result = currentUser.createFlow()
        serchObj = re.search(r'var chartId = "([a-zA-Z0-9]*)"', result.text)
        # 找到图表的ID
        chartId = serchObj.group(1)
        # 小号开始点赞扩容
        for user in self.helperList:
            user.dolike(chartId)

        # 大号自己给自己点赞
        self.dolike(chartId)
        # 最大容量
        maxChart = self.getMaxChart()
        print("扩容一次完成,当前最大容量:%d" % maxChart)

        # 删除新建的图表
        currentUser.deleteChart(chartId)

    def login(self):
        """
        登录
        """
        postData = {
            'login_email': self.login_email,
            'login_password': self.login_password,
            'window': True
        }
        print("用户 %s 开始登录..." % self.login_email)
        result = self.s.post(User.API['login'], data=postData)
        msg = json.loads(result.text)
        if msg['msg'] != "success":
            print("用户:账号【%s】或密码【%s】错误,请检查!!" % (self.login_email, self.login_password))
            exit(-1)
        else:
            print("用户 %s 登录成功" % self.login_email)

    def createFlow(self):
        """
        创建流程图
        """
        return self.s.get(User.API['createFlow'])

    def dolike(self, chartId):
        """
        点赞
        :param chartId:
        """
        for index in range(0, 2):
            postData = {
                'chartId': chartId
            }
            result = self.s.post(User.API['dolike'], data=postData)
            msg = json.loads(result.text)
            if msg["result"]:
                # print("给 %s 点赞成功!" % chartId)
                break

    def getMaxChart(self):
        """
        获取最大容量
        """
        result = self.s.get(User.API['MaxChart'])
        resultObj = json.loads(result.text)
        return resultObj['totalcount']

    def deleteChart(self, chartId):
        """
        删除指定图表
        """
        postData = {
            "fileType": "chart",
            "fileId": chartId,
            "resource": ""
        }
        # 删除创建的空流程图
        self.s.post(User.API['mvTrash'], data=postData)
        self.s.post(User.API['delete'], data=postData)

    def __init__(self, login_email, login_password):
        self.s = requests.Session()
        self.login_email = login_email
        self.login_password = login_password
        self.login()
        self.helperList = []


if __name__ == "__main__":

    # 获取必要信息
    login_email = input("请输入您的账号:")
    login_password = input("请输入您的密码:")
    # 登陆后的小号列表
    loginedUserList = []

    # 小号初始化
    print("小号开始初始化...")
    with open("users.json") as config:
        configStr = config.read()
        userList = json.loads(configStr)
    for item in userList:
        user = User(item['name'], item['passwrod'])
        loginedUserList.append(user)

    print("大号开始初始化...")
    currentUser = User(login_email, login_password)
    currentUser.setHelpList(loginedUserList)
    # 开始扩容
    print("开始扩容...")
    # currentUser.expand()
    while True:
        currentUser.expand()

pass
