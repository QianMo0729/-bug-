'''
================================================================================
 runtime_guard.py —— 第 4 关：运行时守卫 / 结局闸口
================================================================================
【这一关在游戏里怎么表现】
- 场景是一间"机房控制室"：墙上两块大表——
    左表 = time（小时），右表 = temp（CPU 温度℃）。两块表只随进度跳，不随真实时间。
- 房间中央是一台 try/except"防护闸"：程序运行到风险代码时，异常会顺着管道
  流进 except 处理器。玩家要给闸门"配线"，决定异常被怎么处理。
- 这一关是所有结局的总闸：走到出口前，finalize() 根据 time/temp/碎片 判定结局。

【教学点（异常处理）】
  1) try/except 基本结构：把可能出错的代码包起来，出错时走 except 而不是崩溃。
  2) ☠ 裸 except: pass —— 把异常"吞掉"什么都不说，是最危险的反模式
     （bug 被悄悄掩盖，正是本关线索）。
  3) except 要捕获具体异常类型，并且至少把它打印/记录出来。

【推理链线索（承上启下）—— 实锤前最后一环：掩盖证据】
- 控制室的异常日志被人动过手脚：有一个 `except: pass` 专门**吞掉**某个作者
  签名的报错——说明那个人知道自己在造 bug，并刻意销毁证据。
- 玩家把 `except: pass` 改成打印异常后，被吞掉的报错显形，泄露出
  【碎片④】= AUTHOR = "B055"（看着像乱码，其实是 BOSS 的 leetspeak 签名）。
- 至此四片集齐：动机异常→有人造→具体某人→此人在掩盖→签名是 B055。
================================================================================
'''
import agent_bot
import game_setup
import current_role
import bug_maker


# ============================================================================
#  教学：try/except —— 把风险代码包起来，别让它崩掉整个程序
# ============================================================================
def guarded_run(risky):
    '''房间表现：风险代码块是一段带电的红线。不包 try 直接踩 = 全屏崩红；
    包进 try、配好 except 管道 = 异常被导流到处理器，程序继续。'''
    agent_bot.bot_say("有些代码注定可能出错。把它放进 try，出错时就跳到 except，而不是整个崩掉。")
    try:
        return risky()
    except ValueError as e:                  # ← 正确：捕获具体类型，并保留异常信息
        agent_bot.system_prompt(f"逮到一个 ValueError：{e}（已安全处理）")
        return None


# ============================================================================
#  ☠ 反模式 + 线索④：被裸 except 吞掉的报错
# ============================================================================
# 这是控制室里"被人动过手脚"的异常日志处理器。
def swallow_errors_BROKEN():
    '''房间表现：一个标着 "log" 的闸门，红线穿进去却什么都不输出——
    异常被 except: pass 整个吃掉。玩家"修"这个闸门（把 pass 换成打印），
    被吞的那条报错才会从管道里喷出来，露出作者签名 → 碎片④显形。'''
    bugs = bug_maker.dump_logged_bugs()      # 之前几关登记进来的 bug
    for b in bugs:
        try:
            raise b.error                     # 重放每个 bug 的报错
        except:                               # ← bug：裸 except 把一切吞掉，证据全被掩盖
            pass


def reveal_errors_FIXED():
    '''玩家粘贴的正解：except 捕获具体异常并打印，证据现形。'''
    bugs = bug_maker.dump_logged_bugs()
    revealed_author = None
    for b in bugs:
        try:
            raise b.error
        except Exception as e:                # 捕获并暴露，而不是 pass
            agent_bot.system_prompt(f"显形：{e}  作者签名={b.author}")
            revealed_author = b.author        # 所有报错的签名竟然一模一样

    # —— 被吞的签名泄露，【碎片④】显形 ——
    game_setup.spawn_fragment(4, lines=[
        f'AUTHOR = "{revealed_author}"   # 被掩盖的作者签名，看着像乱码，其实是 leetspeak',
    ])
    agent_bot.bot_say("四片碎片到齐了。main.py 旁边那个一直灰着的 bug_maker.py 标签，亮了。")
    agent_bot.bot_say("用 command 点进去，把这个查作者的函数拼回原样——我们去抓真凶。")
    return revealed_author


# ============================================================================
#  结局闸口：纯函数判定（便于单测），输入全局进度量
# ============================================================================
# 结局优先级见 _DESIGN_碎片与结局.md 的状态机：
#   temp 触顶 > time 超时 > 碎片集齐 > 仅修表面bug
def finalize(time, temp, fragments, bug_fixed):
    '''房间表现：走到控制室出口时触发。先看温度表是否爆表、再看时间表是否超时，
    再看碎片是否集齐，最后才落到"加班"这个默认坏结局。'''
    if temp >= 100:
        return _boss_overheat()                      # → 崩溃 / 险胜后继续
    if time > 3.0:
        return _boss_drowsy()                         # → 不眠之夜 / 倒头就睡
    if len(fragments) >= 4:
        agent_bot.bot_say("证据链闭合。真正的 bug 源头，在 bug_maker.py 里等着。")
        return "HIDDEN_UNLOCKED"                       # → 进隐藏副本（见 bug_maker.py）
    if bug_fixed:
        return _ending_overtime()                     # → 加班（治标不治本）
    return "CONTINUE"


def _boss_overheat():
    '''CPU 过热 Boss：节奏点击"散热片"压温度。压回安全区→险胜继续；点不过来→崩溃。'''
    agent_bot.system_prompt("⚠ CPU 温度触顶！进入散热 Boss——跟着节奏点散热片！")
    survived = game_setup.start_boss("overheat")
    return "CONTINUE" if survived else "ENDING_CRASH"   # 崩溃结局


def _boss_drowsy():
    '''睡意 Boss：横版接咖啡☕/躲 zzz，睡意条 20s 基线，撑 40s 通过。'''
    agent_bot.system_prompt("🌙 已经熬了 3 小时……睡意 Boss 来袭！接住咖啡，躲开 zzz。")
    held = game_setup.start_boss("drowsy", hold_seconds=40)
    if not held:
        return "ENDING_SLEEP"                           # 倒头就睡
    agent_bot.bot_say("你硬撑了过去。如果接着把 bug 修好，就是不眠之夜。")
    return "CONTINUE_INSOMNIA"                          # 撑过→若后续修好bug则不眠之夜


def _ending_overtime():
    '''加班结局：表面 bug 修了，但没顺碎片链查真凶，红色报错重新淹没屏幕。'''
    agent_bot.bot_say("终于修好 Bug 了，回家睡觉！")
    agent_bot.system_prompt("……可红色报错弹窗开始疯狂弹出，淹没了整个屏幕。")
    agent_bot.bot_say("究竟是怎么回事！（你只修了表面，真正造 bug 的人还在。）")
    return "ENDING_OVERTIME"
