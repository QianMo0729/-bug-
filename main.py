'''地图设置说明：
点击开始游戏，过完剧情动画后，显示加载中。下方代码栏出现键入动画。键入的是import部分。
然后人物渐渐浮现，随之快速键入__init__函数。
后面说的代码块都是保留的。
bot_say是机器人讲的话
system_prompt在中间短暂淡入后淡出
进入每个对应区块才解锁每个区块的代码浏览权限。

设定改变：CPU的温度不是随着时间增加而增加的，而是根据进度增加的。然后新增一个时间参量，也会跟着进度增加。然后新增结局：时间超过三个小时（暂定）之后触发boss战：睡意。需要接住咖啡，避免“zzz”。上方有一个睡意条，随着时间增加而增加，正常是20秒的时间。喝咖啡可以减少睡意，碰到zzz增加睡意。坚持40秒退出boss战，可以继续游戏流程，如果继续流程修好了bug，那么触发结局：不眠之夜。没坚持40秒则触发结局：睡在公司。
'''
import function
import agent_bot
import bug_maker
import game_setup
import current_role

from maybe_bug import MaybeBug

# ===== 初始化 =====
current_role.set_role(name="TuTu", age=18, sex="unknown")
game_setup.set_scene("main")

time = 0.0
temp = 45

agent_bot.bot_say("你醒在 main.py 里。程序会从上往下执行，先创建角色，再布置场景。")


# ===== if条件分支与while循环 =====
role_location = current_role.get_role_location()

agent_bot.bot_say("你前面面临一个分岔路，在python中叫做条件语句，会判断给出的条件。")

if role_location == "Right": # 如果角色位置走入了右侧的房间
    while True:
        function.some_founction()  # 一些代码功能，不用管他

        agent_bot.bot_say("你走入了一个while循环模块。")
        agent_bot.system_prompt("时间+0.2h，温度+5℃")

        time += 0.2
        temp += 5
        
        agent_bot.bot_say("True是一个布尔值，表示条件永远为真。")
        agent_bot.bot_say("因此，这个循环将无限执行下去，除非被打断，例如break语句。")
        agent_bot.bot_say("拾取这个break代码块，粘贴上去！")
        # 这里可以用来添加代码
        agent_bot.system_prompt("你又回到了原点，打破这个循环！")
elif role_location == "Left": # 如果角色位置走入了左侧的房间
    function.some_founction()  # 一些代码功能，不用管他

    agent_bot.bot_say("看起来你的运气不好，走到了一个无意义的房间。(时间+0.2h)")
    agent_bot.system_prompt("好像浪费了一点时间，重新回到分岔路口吧！")

    time += 0.2
    

# ===== 列表与下标 =====
agent_bot.bot_say("恭喜你走出了if判断！继续寻找bug在哪吧！")
agent_bot.bot_say("接下来要讲的是列表。列表的位置是从左到右数的，但要注意它从0开始数。")

NPCs = ["NPC0", "NPC1", "NPC2", "NPC3", "NPC4", "NPC5", "NPC6"]

agent_bot.bot_say("你可以用append方法在列表末尾添加元素，用insert方法在指定位置添加元素，用remove方法删除列表中的元素。")
agent_bot.bot_say("在这个房间里，每个NPC都有自己的位置，想办法走进下一个房间。")
agent_bot.system_prompt("持续深入（温度+2℃）")

temp += 2

game_setup.set_npcs_location(NPCs)

# 这里可以用来添加代码

agent_bot.bot_say("恭喜你成功进入了下一个房间！观察一下这个房间的代码和注释，想办法走出这儿吧！")


# ===== 尝试运用 =====
while True:
    role_move = current_role.get_how_role_move(4)   # 获取角色后四步的移动情况

    if role_move == "UURD":  # 如果角色后四步的移动情况是上上右下
        game_setup.set_next()  # 开启下一关的传送门
        break
    elif role_move == "ULDR":  # 如果移动情况是上左下右
        can_out = False

        while not can_out:
            current_role.go_to("Room Bug 1")

            agent_bot.system_prompt("你误入了一个有bug的房间！（时间+0.5h，温度+5℃）")
            agent_bot.bot_say("看起来你找到了一个bug。但你没有删除权限，看看手头有没有能用的代码跳过这个bug吧？")

            time += 0.5
            temp += 5

            can_out = True
            # 这里可以贴入代码
            bug_maker.unresponed_bug()  # 这个方法是造成无响应的bug
            can_out = False
    else:
        agent_bot.system_prompt("时间还在不断流逝……（时间+0.1h,温度+1℃）")

        time += 0.1
        temp += 1

# ===== 类与对象 =====
agent_bot.bot_say("python支持面对对象编程。")
agent_bot.bot_say("MaybeBug有着一类事物的共同的属性，称作类。")
agent_bot.bot_say("而maybe_bug是MaybeBug这个模板新建出来的某个具体对象。")

maybe_bug = MaybeBug(time = time, temp = temp)  # 创建对象

maybe_bug.maybe_creat_bug()  # 调用对象的方法

time = maybe_bug.time
temp = maybe_bug.temp

agent_bot.bot_say("我们只能看见它在main.py里面调用了这个方法，但这个方法做了什么还看不出来。")
agent_bot.bot_say("用command功能键，进去看看它做了什么吧？")  #此处转场时提示小贴士：在编译器里，按住 Command（Mac）或 Ctrl（Windows），再左键点击方法名、类名或变量名，通常可以快速跳转到它的定义位置。
