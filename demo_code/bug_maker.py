'''
================================================================================
 bug_maker.py —— 隐藏副本 / 真·结局（推理链的收束点）
================================================================================
【这一关在游戏里怎么表现】
- 集齐 4 片碎片后，main.py 旁一直灰着的 bug_maker.py 标签亮起，可点入。
- 场景切到 *红色崩坏风格* 的大地图（idea.md）：地块拼出一个被严重破坏的
  函数轮廓——那正是 _trace() 的"残骸"。玩家走到崩坏处，把手里的
  4 片碎片按顺序"嵌回"地形，函数被复原（代码面板逐行点亮拼合过程）。
- 复原后让玩家**修掉 _trace 自身的一个 bug**（is → ==，呼应"代码自己也会有bug"），
  再运行它，比对全部已记录 bug 的作者 → 全部命中同一签名 = 老板。证据闭合，开战。

【为什么这一关能让玩家信服（思维链闭合）】
  动机异常(main) → 有人在造(maybe_bug) → 具体某人改过(function)
  → 此人在掩盖证据(runtime_guard) → 签名 B055 = BOSS → 全部 bug 同一作者(本关)
  每一步都比上一步更具体，是单调收敛的推理，没有巧合或跳跃。

【教学点】
  1) is vs ==：is 比较"是否同一对象"，== 比较"值是否相等"。
     小整数/驻留字符串有时 is 也"碰巧"为真，但语义上比较值必须用 ==——
     这正是 _trace 里那个隐蔽 bug：bug.author is sig 在签名是长字符串时会漏判。
  2) 把前面所有知识点（list/dict/函数/异常）汇总成一次"反注入"实战。
================================================================================
'''
import agent_bot
import game_setup
import current_role


# ---- 全程被各关登记进来的 bug 台账（main/maybe_bug/function 都往这里写）----
ALL_BUGS = []        # 每个元素带 .author / .error / .where

class _BugRecord:
    def __init__(self, where, author, error):
        self.where, self.author, self.error = where, author, error


def log_bugs(items):           # maybe_bug 关调用：登记发现的 bug
    for w in items:
        ALL_BUGS.append(_BugRecord(where=w, author="B055", error=RuntimeError(w)))

def log_patch(where, author):  # function 关调用：登记一次"人为篡改"
    ALL_BUGS.append(_BugRecord(where=where, author=author, error=RuntimeError("patched")))

def dump_logged_bugs():        # runtime_guard 关调用：回放报错（其实作者全是 B055）
    return ALL_BUGS

def unresponed_bug():          # main.py 调用的"造成无响应的 bug"——现在知道它从哪来了
    agent_bot.system_prompt("一个无响应 bug 被'主动'制造出来……是谁下的指令？")


# ============================================================================
#  碎片复原：把 4 片拼回 _trace()（玩家在地图上嵌回地形 = 取消注释/补全）
# ============================================================================
AUTHOR = "B055"                       # 碎片④泄露的签名（leetspeak: B0SS）

def _trace(sig):                      # 碎片①：函数头
    found = []                        # 碎片②：收集容器
    for bug in ALL_BUGS:              # 碎片②：遍历全部已记录 bug
        if bug.author == sig:         # 碎片③（已修）：== 比较值；原版误用 is 会漏判
            found.append(bug)         # 碎片③：命中收集
    return found                      # 碎片③：返回命中列表


def _trace_BROKEN(sig):
    '''玩家刚拼好、尚未修复的版本：用 is 比较两个长字符串，命中数为 0 →
    屏幕提示"查无此人"，引导玩家想起 function 关学的 is/== 区别再来修。'''
    found = []
    for bug in ALL_BUGS:
        if bug.author is sig:         # ← bug：长字符串 is 不保证同一对象，漏判
            found.append(bug)
    return found


# ============================================================================
#  实锤 + 真 Boss
# ============================================================================
def confront():
    '''房间表现：复原并修好 _trace 后，自动以 AUTHOR 运行，命中数 == 全部 bug 数。
    屏幕把每个 bug 连到同一个签名 B055，光线汇聚成老板的剪影。'''
    agent_bot.bot_say("把四片碎片嵌回地形……_trace 复原了。先用 == 修好它自己的 bug，再跑一次。")

    hits = _trace(AUTHOR)
    if len(hits) == len(ALL_BUGS) and len(ALL_BUGS) > 0:
        agent_bot.system_prompt(f"命中 {len(hits)}/{len(ALL_BUGS)} —— 所有 bug 都是同一只手！")
        agent_bot.bot_say("签名 B055……解码出来就是 BOSS。原来源源不断的 bug，是老板亲手种的。")

        # —— 真 Boss 战：综合关，用前面学的招拆解老板的 bug 弹幕 ——
        agent_bot.bot_say("老板（啤酒肚，攥着一沓钞票）走过来：")
        agent_bot.bot_say("『竟然被你发现了吗？我就是想源源不断创造新 bug，让你们全都加班！』")
        agent_bot.bot_say("主角：『我一定要打败你这个黑心老板！』")
        won = game_setup.start_boss("the_boss")        # 清空老板的 bug 队列即获胜
        return "ENDING_TRUE" if won else "ENDING_CRASH"

    # 没修 is/== 就来跑：命中 0，给一次"回去想想"的引导
    agent_bot.system_prompt("查无此人？_trace 里用了 is 比较长字符串，回想 function 关——该用 == 比较值。")
    return "RETRY_TRACE"
