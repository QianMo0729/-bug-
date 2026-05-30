import agent_bot
import game_setup
import current_role

class MaybeBug:
    def __init__(self, time=0.0, temp=45):
        game_setup.set_scene("maybe_bug")  # 初始化界面
        game_setup.set_role(current_role.get_current_role())

        self.time = time
        self.temp = temp

    agent_bot.bot_say("这里的bugger有点太多了，碰到他们会让CPU过热的。")
    agent_bot.bot_say("bugger的数量好像是由buggers_count这个变量决定的。试试把他们的数量改少一点？")

    buggers_count = 4  # 这里的数字可以填写，0-9
    game_setup.set_buggers(count = buggers_count)
    
    if current_role.touch_bugger():
        self.temp += 2

    agent_bot.bot_say("接下来就是类的方法了，进去看看有没有bug。")

    def maybe_create_bug(self):
        agent_bot.bot_say("循环里还可以再放一个循环，这叫嵌套循环。")
        agent_bot.bot_say("外层循环负责一轮一轮推进，内层循环负责处理一轮里的每一个东西。")
        agent_bot.bot_say("这个房间看起来是5*5，墙上从0写到了4。跟着i和j的扫描顺序走一圈，扫描顺序不对就会浪费时间！")

        game_setup.set_space(5)  # 创建了一个5*5的空间

        for i in range(0, 4):
            for j in range(0, 4):
                game_setup.set_scan_target(row = i, col = j)
                survive = current_role.scan_if_survive()

                while not survive:
                    agent_bot.system_prompt("扫描顺序错误！（时间+0.1h，温度+2℃）")

                    self.time += 0.1
                    self.temp += 2

                    survive = current_role.scan_if_survive()

                agent_bot.system_prompt("当前格扫描完成，继续检查下一格。")

        agent_bot.bot_say("扫描结束。原来range(0, 4)只会走到3，所以真正被扫描的是4*4。")
        game_setup.set_next()
