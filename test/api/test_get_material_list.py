from wechat.robot import robot

Client = robot.client
result = Client.get_media_list("news", 0, 20)
print result