import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from datetime import datetime, date

from week import week
import json

with open('vkInfo.json') as info:
    vkInfo = json.load(info)

user = vk_api.VkApi(vkInfo['userLogin'], vkInfo['userPassword'])
user.auth()
vkUser = user.get_api()


bh = vk_api.VkApi(token = vkInfo['token'])
give = bh.get_api()
longpoll = VkBotLongPoll(bh, group_id=vkInfo['groupID'])

class Bot():
    
    def __init__(self, schedule):
        self.isPostedSchedule = False
        self.schedule = schedule

    def posting(self):
        post = self.createPost()
        if post: 
            vkUser.wall.post(
                message='Расписание на завтра:\n{}'.format(post), 
                from_group=True, 
                owner_id = -1 * vkInfo['groupID']
            )
        self.isPostedSchedule = True

    def createPost(self):
        weekD = (datetime.today().weekday() + 1) % 8
        if self.schedule.days[weekD][2]:
            post = '\n'.join(list(map(lambda x: x[0] if x else '', self.schedule.days[weekD][2])))
        return post    

    def sendMessage(self, updateDays):
        message = 'Изменения в расписании \n{}'.format(self.createMessage(updateDays))
        give.messages.send(
            chat_id = 1,
            message = message,
            random_id = 0,
            )

    def createMessage(self, indexesOfDays):
        message = []
        for i in range(len(indexesOfDays)):
            w = 'текущей' if self.schedule.days[i][0][-1] == '1' else 'следующей'
            mes = '{} {} недели'.format(week[self.schedule.days[i][0][:-1]], w)
            message.append(mes)
        return '\n'.join(message)
