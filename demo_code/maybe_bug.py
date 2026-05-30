'''
================================================================================
 maybe_bug.py —— 第 2 关：类与对象 / "方法小房间" 群
================================================================================
【这一关在游戏里怎么表现】
- 传送动画结束，页面从黑显现，代码面板键入 import + __init__。
- 进入是一个小房间（init 区），代码停在 __init__。
- 往前是一条 3 格宽长走廊，红色 buggers 巡逻（由 buggers_count 控制）：
    4 个=横向交叉极速移动；8 个=四横四竖；9 个=3×3 静止方阵（安全）。
    ——把"调参数"变成解谜：玩家必须把 buggers_count 改到 9 才能安全穿过去，
      顺手在走廊尽头死角拿到【碎片②】。
- 走廊尽头是"大房间"，里面用围墙隔出若干**小房间，每间=一个方法**，
  门楣上写方法名。走进门 = ctrl点击进入该方法的子关卡。

【这一关的 4 个方法小房间（每间一个常见 Python bug 教学）】
  1) maybe_create_bug —— 嵌套循环 / range 边界 off-by-one
  2) clean_list       —— 遍历列表时删除元素，导致漏删（边遍历边改）
  3) read_config      —— 字典访问不存在的键 KeyError，用 .get() 兜底
  4) dig_deeper       —— 递归缺少基线条件 → 栈溢出（无限递归）

【推理链线索（承上启下）】
- 上一关只是"有 bug"。这一关 main.py 调用了 bug_maker.unresponed_bug()，
  程序居然**主动制造** bug —— 从"有 bug"升级为"有人在造 bug"。
- 碎片②是 _trace() 的"收集容器 + 遍历"两行（见 _DESIGN_碎片与结局.md）。
================================================================================
'''
import agent_bot
import game_setup
import current_role
import bug_maker          # 注意：又见到这个"造 bug"的模块，线索在累积


class MaybeBug:
    def __init__(self, time=0.0, temp=45):
        game_setup.set_scene("maybe_bug")              # 初始化界面
        game_setup.set_role(current_role.get_current_role())

        self.time = time
        self.temp = temp
        self.found_bugs = []                            # 本关记录到的 bug，真结局会用到

        # ---------- init 房间 / buggers 走廊 ----------
        agent_bot.bot_say("这里的 bugger 有点太多了，碰到他们会让 CPU 过热的。")
        agent_bot.bot_say("bugger 的数量好像是由 buggers_count 这个变量决定的。试试把数量改一改？")
        agent_bot.system_prompt("提示：填 9 时它们会排成 3×3 不动的阵列，留出安全缝隙。")

        buggers_count = 4                               # 玩家可改：0-9
        game_setup.set_buggers(count=buggers_count)

        if current_role.touch_bugger():                 # 蹭到就升温
            self.temp += 2

        agent_bot.bot_say("走廊尽头那个发光的青色方块……好像是段代码？捡起来看看。")  # 碎片②

    # ========================================================================
    #  方法房间 1：嵌套循环 / range 边界
    # ========================================================================
    def maybe_create_bug(self):
        '''房间表现：5×5 空间，墙上从 0 写到 4。门进入即上锁变红，
        强制弹窗教学："按住 Enter 按 i/j 扫描顺序移动，地上蓝线记录轨迹；
        松开 Enter 不记录。走对线变绿、门开；走错线变红消失。"'''
        agent_bot.bot_say("循环里还能再放一个循环，这叫嵌套循环。")
        agent_bot.bot_say("外层一轮一轮推进，内层处理一轮里的每个东西。")
        agent_bot.bot_say("房间是 5×5，墙上 0 到 4。跟着 i、j 的扫描顺序走一圈，顺序错了会浪费时间！")

        game_setup.set_space(5)

        for i in range(0, 4):                           # ← 玩家要发现这里的边界 bug
            for j in range(0, 4):
                game_setup.set_scan_target(row=i, col=j)
                survive = current_role.scan_if_survive()

                while not survive:                      # 走错就卡在原地重扫
                    agent_bot.system_prompt("扫描顺序错误！（时间+0.1h，温度+2℃）")
                    self.time += 0.1
                    self.temp += 2
                    survive = current_role.scan_if_survive()

                agent_bot.system_prompt("当前格扫描完成，继续下一格。")

        agent_bot.bot_say("扫描结束……可第 4 行 / 第 4 列从没被点亮。")
        agent_bot.bot_say("原来 range(0, 4) 只走到 3，真正扫的是 4×4，漏了一整圈！")
        agent_bot.system_prompt("把 range(0, 4) 改成 range(0, 5) 才覆盖整张 5×5。")
        self.found_bugs.append("off_by_one@maybe_create_bug")

    # ========================================================================
    #  方法房间 2：遍历列表时删除元素（边遍历边改）
    # ========================================================================
    def clean_list(self):
        '''房间表现：地上排着一列红色 bug 方块（trash 列表）。玩家站在传送带上，
        每"清理"一个就把它从列表移除。直接边走边删时，传送带会跳格——
        被删元素后面的那个会被"跳过"，留下没清干净的 bug（可视化漏删）。
        正解：遍历副本 list(trash) 或用列表推导重建，房间才会全清、门变绿。'''
        agent_bot.bot_say("这一排红色方块是待清理的 bug，存在 trash 列表里。")
        agent_bot.bot_say("直觉是：一边遍历一边把它从列表里删掉。试试看？")

        trash = ["bug", "ok", "bug", "bug", "ok"]
        game_setup.set_conveyor(trash)

        # —— 玩家先体验"错误写法"：边遍历边删，索引错位导致漏删 ——
        for item in trash:
            if item == "bug":
                trash.remove(item)                      # ← bug：改变了正在遍历的列表
                self.temp += 1
        agent_bot.system_prompt(f"清理后还剩：{trash} —— 怎么还有漏网的 bug？（温度+1℃）")
        agent_bot.bot_say("删掉一个后，后面的元素整体前移，循环的下标却照常 +1，于是跳过了一个。")

        # —— 正解：遍历副本，或重建新列表（玩家拾取“[ ]推导式”代码块贴上）——
        agent_bot.bot_say("规则：不要在遍历一个列表的同时修改它。遍历它的副本，或干脆重建一个。")
        cleaned = [x for x in trash if x != "bug"]      # 玩家粘贴的正解
        game_setup.set_conveyor(cleaned)
        agent_bot.system_prompt("全部清理干净，门开了。")
        self.found_bugs.append("mutate_while_iterate@clean_list")

    # ========================================================================
    #  方法房间 3：字典 KeyError（访问不存在的键）
    # ========================================================================
    def read_config(self):
        '''房间表现：三扇门，门楣分别写着字典的键名 "speed" / "lang" / "theme"。
        config 里只有前两个键。走向 "theme" 门会触发 KeyError——门"砸"下来弹回玩家，
        屏幕红闪。正解：把直接取值 config["theme"] 换成 config.get("theme", 默认值)，
        缺失的门会显示默认值并安全打开。教"先判断/给默认值"的防御式取值。'''
        agent_bot.bot_say("字典像一排带标签的抽屉，用键去取值。")

        config = {"speed": 2, "lang": "py"}             # 注意：没有 "theme"
        game_setup.set_doors(list(config.keys()) + ["theme"])

        # —— 错误写法：直接索引不存在的键 ——
        agent_bot.bot_say("想打开 theme 这扇门，直觉是 config[\"theme\"]。")
        agent_bot.system_prompt("KeyError: 'theme' —— 抽屉根本不存在，程序直接报错！（温度+2℃）")
        self.temp += 2

        # —— 正解：.get() 给默认值，或先 in 判断 ——
        agent_bot.bot_say("用 config.get(\"theme\", \"dark\") ：有就取值，没有就退回默认，不会崩。")
        theme = config.get("theme", "dark")             # 玩家粘贴的正解
        game_setup.open_door("theme", label=theme)
        agent_bot.system_prompt(f"theme 缺省为 {theme}，门安全打开。")
        self.found_bugs.append("keyerror@read_config")

    # ========================================================================
    #  方法房间 4：递归缺少基线条件（无限递归 → 栈溢出）
    # ========================================================================
    def dig_deeper(self, depth=0):
        '''房间表现：一扇门里套着一扇更小的门，无限向纵深缩小（递归的视觉化）。
        没有"停下来"的条件时，玩家会被一层层吸入，右侧出现不断增高的"调用栈"塔，
        塔顶撞顶 = RecursionError 崩溃红屏。正解：加一个基线条件（depth>=3 就返回），
        塔到 3 层封顶、最深处亮起出口。教"递归必须有能终止的 base case"。'''
        agent_bot.bot_say("一个函数可以调用它自己，这叫递归。")
        agent_bot.bot_say("但每次调用都要更接近一个能停下来的'底'，否则会一直钻下去。")

        game_setup.push_call_stack(depth)               # 右侧调用栈塔 +1 层

        # —— 基线条件（玩家拾取并粘贴的关键一行）——
        if depth >= 3:                                  # ← 缺了它就是无限递归
            agent_bot.system_prompt("触到底了！开始一层层返回。")
            game_setup.open_exit()
            return depth

        agent_bot.system_prompt(f"再往里钻一层…当前第 {depth} 层（时间+0.1h）")
        self.time += 0.1
        return self.dig_deeper(depth + 1)               # 向"底"靠近

    # ========================================================================
    #  本关收束：把记录到的 bug 交给 main 流程，并提示真相的下一环
    # ========================================================================
    def report(self):
        agent_bot.bot_say("这些 bug 我都记下来了……但奇怪，它们不像是'写错'，倒像是被'放进来'的。")
        agent_bot.bot_say("main.py 里那句 bug_maker.unresponed_bug()，是程序在'主动'造 bug。")
        agent_bot.bot_say("到底是谁让它这么干的？用 command 点 function，去函数小镇查查。")
        bug_maker.log_bugs(self.found_bugs)             # 把线索登记进 bug_maker（真结局比对用）
        return self.found_bugs
