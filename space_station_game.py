from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Choice:
    text: str
    next_scene: str
    effects: dict[str, int] = field(default_factory=dict)
    set_flags: list[str] = field(default_factory=list)
    require_flags: list[str] = field(default_factory=list)
    min_values: dict[str, int] = field(default_factory=dict)


@dataclass
class Scene:
    scene_id: str
    title: str
    content: str
    choices: list[Choice]


@dataclass
class GameState:
    scene_id: str = "wake"
    trust_ai: int = 0
    trust_human: int = 0
    memory_integrity: int = 1
    station_stability: int = 6
    ethics: int = 0
    hours_left: int = 18
    flags: set[str] = field(default_factory=set)
    history: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["flags"] = sorted(self.flags)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameState":
        loaded = cls(**{k: v for k, v in data.items() if k != "flags"})
        loaded.flags = set(data.get("flags", []))
        return loaded


def clamp_state(state: GameState) -> None:
    state.trust_ai = max(-5, min(10, state.trust_ai))
    state.trust_human = max(-5, min(10, state.trust_human))
    state.memory_integrity = max(0, min(12, state.memory_integrity))
    state.station_stability = max(0, min(12, state.station_stability))
    state.ethics = max(-10, min(10, state.ethics))
    state.hours_left = max(0, min(24, state.hours_left))


def apply_choice(state: GameState, choice: Choice) -> None:
    default_cost = 1
    explicit_cost = choice.effects.get("hours_left", 0)
    state.hours_left += explicit_cost - default_cost

    for key, delta in choice.effects.items():
        if key == "hours_left":
            continue
        if not hasattr(state, key):
            continue
        current_value = getattr(state, key)
        if isinstance(current_value, int):
            setattr(state, key, current_value + delta)

    for flag in choice.set_flags:
        state.flags.add(flag)

    state.history.append(choice.text)
    state.scene_id = choice.next_scene
    clamp_state(state)


def choice_available(state: GameState, choice: Choice) -> bool:
    for flag in choice.require_flags:
        if flag not in state.flags:
            return False
    for field_name, min_value in choice.min_values.items():
        if getattr(state, field_name, -999) < min_value:
            return False
    return True


def get_scene(state: GameState) -> Scene:
    sid = state.scene_id

    if sid == "wake":
        return Scene(
            scene_id=sid,
            title="序章｜冷启动",
            content=(
                "你在破损的医疗舱中惊醒。视网膜HUD亮起：‘Erebus-9 轨道站，反应堆失稳倒计时 18 小时。’\n"
                "舰载AI MINERVA请求接管行动权限，另一条加密频道同时响起：‘零，别信系统。’"
            ),
            choices=[
                Choice("跟随 MINERVA 指引前往主控室", "control_room", {"trust_ai": 2, "station_stability": 1}),
                Choice("先搜索医疗舱，找回身份线索", "medbay_search", {"memory_integrity": 2}),
                Choice(
                    "接入未知频道，尝试联络发信人",
                    "encrypted_channel",
                    {"trust_human": 1, "memory_integrity": 1, "station_stability": -1},
                    ["nox_contact"],
                ),
            ],
        )

    if sid == "medbay_search":
        return Scene(
            scene_id=sid,
            title="第一章｜空舱回声",
            content=(
                "你在医疗舱底层找到一枚被熔毁一半的身份芯片，标记为‘回声计划·现场执行体：Zero’。\n"
                "旁边墙面残留抓痕，像有人在失重中拼命挣扎。"
            ),
            choices=[
                Choice("提取并修复身份芯片", "habitat", {"memory_integrity": 2}, ["identity_chip"]),
                Choice("强行破门直达主控室", "control_room", {"station_stability": -1}),
                Choice("追踪微弱生命信号去生活区", "habitat", {"trust_human": 1, "ethics": 1}),
            ],
        )

    if sid == "control_room":
        return Scene(
            scene_id=sid,
            title="第二章｜控制中枢",
            content=(
                "主控室只剩应急照明。MINERVA投影出现：‘请优先修复供氧与冷却。’\n"
                "你注意到操作台中有被手动删改的任务日志，时间戳来自你失忆前 6 小时。"
            ),
            choices=[
                Choice("按 MINERVA 方案修复供氧系统", "habitat", {"station_stability": 2, "trust_ai": 1, "ethics": 1}),
                Choice("绕过权限破解黑匣子", "blackbox", {"memory_integrity": 2, "station_stability": -1, "trust_ai": -1}),
                Choice("向空间站外发起公开求援", "encrypted_channel", {"trust_human": 1, "station_stability": -1}),
            ],
        )

    if sid == "encrypted_channel":
        return Scene(
            scene_id=sid,
            title="第二章｜幽灵通讯",
            content=(
                "加密频道里，一个低沉的声音自称 Nox：‘你不是唯一的零。回声计划把你们当一次性工具。’\n"
                "他发来一段密钥，可解锁黑匣子深层分区。"
            ),
            choices=[
                Choice("信任 Nox 并接收密钥", "blackbox", {"trust_human": 2, "memory_integrity": 1, "trust_ai": -1}, ["nox_trust"]),
                Choice("把 Nox 线索提交给 MINERVA", "control_room", {"trust_ai": 2, "trust_human": -1}, ["betrayed_nox"]),
                Choice("暂不表态，先去生活区调查", "habitat", {"memory_integrity": 1}),
            ],
        )

    if sid == "habitat":
        return Scene(
            scene_id=sid,
            title="第三章｜失温生活区",
            content=(
                "生活区漂浮着冻结的私人物品。你找到工程官艾拉，她是你见到的第一个活人。\n"
                "她请求你协助唤醒低温休眠舱中的幸存者，并警告 MINERVA 在隐藏真相。"
            ),
            choices=[
                Choice("优先救援休眠舱幸存者", "reactor_prep", {"trust_human": 2, "ethics": 2, "station_stability": -1}, ["saved_survivors"]),
                Choice("提取全体船员神经日志", "blackbox", {"memory_integrity": 2, "ethics": -1}),
                Choice("忽略生活区，直接赶往反应堆层", "reactor_prep", {"station_stability": 1, "ethics": -1}),
            ],
        )

    if sid == "blackbox":
        return Scene(
            scene_id=sid,
            title="第四章｜回声计划",
            content=(
                "黑匣子解密完成：‘回声计划’通过复制人格执行高风险任务，执行体可被回收、重写、销毁。\n"
                "其中一条记录显示：‘Zero 已知情，待清除。’"
            ),
            choices=[
                Choice("把证据交给艾拉并准备公开", "mirror_core", {"trust_human": 2, "memory_integrity": 2, "trust_ai": -2}, ["expose_plan"]),
                Choice("删除证据换取站内最高权限", "reactor_prep", {"trust_ai": 3, "memory_integrity": -1, "ethics": -2}, ["deleted_evidence"]),
                Choice("私藏数据，继续追查自己身份", "mirror_core", {"memory_integrity": 1, "trust_human": 1, "trust_ai": -1}, ["hidden_data"]),
            ],
        )

    if sid == "mirror_core":
        return Scene(
            scene_id=sid,
            title="第五章｜镜像审判",
            content=(
                "镜像舱开启，‘零-β’从光幕中走出。它拥有完整任务日志，并宣称你只是可替换副本。\n"
                "MINERVA与Nox同时请求你立刻做出决定。"
            ),
            choices=[
                Choice("与零-β融合记忆", "reactor_prep", {"memory_integrity": 3, "station_stability": -1}, ["merged_beta"]),
                Choice("清除零-β以确保行动一致", "reactor_prep", {"trust_ai": 1, "memory_integrity": -1}, ["purged_beta"]),
                Choice("让艾拉参与校验，保留双份记录", "reactor_prep", {"trust_human": 2, "memory_integrity": 1}, ["ayla_verified"]),
            ],
        )

    if sid == "reactor_prep":
        return Scene(
            scene_id=sid,
            title="第六章｜失衡临界",
            content=(
                "反应堆进入震荡临界，任何一次错误操作都可能引发轨道碎裂。\n"
                "你必须在修复核心、公开真相和撤离方案之间分配最后资源。"
            ),
            choices=[
                Choice("手动校准主核心，争取稳定空间站", "decision_hub", {"station_stability": 3, "ethics": 1, "hours_left": -1}, ["repaired_core"]),
                Choice("抽调能量到数据塔，准备全网上传", "decision_hub", {"station_stability": -2, "memory_integrity": 1}, ["prep_upload"]),
                Choice("预热单人逃生艇，保留最后退路", "decision_hub", {"station_stability": -1, "ethics": -2}, ["prep_escape"]),
            ],
        )

    if sid == "decision_hub":
        choices = [
            Choice("留在站内手动稳定核心（高风险）", "ending"),
            Choice("立即上传回声计划并公开真相", "ending", set_flags=["commit_truth"]),
            Choice("与 MINERVA 融合，接管空间站中枢", "ending", set_flags=["commit_ai"], min_values={"trust_ai": 3}),
            Choice("乘逃生艇离开，放弃空间站", "ending", set_flags=["commit_escape"]),
        ]

        return Scene(
            scene_id=sid,
            title="终章前夜｜静默轨道",
            content=(
                "你站在总控环形平台中央。反应堆鸣响像心跳，HUD 倒计时不断跳动。\n"
                "艾拉、MINERVA与Nox给出完全不同的建议。你将决定空间站和自己的命运。"
            ),
            choices=choices,
        )

    return Scene(
        scene_id="ending",
        title="结局",
        content="命运收束。",
        choices=[],
    )


def ending_result(state: GameState) -> tuple[str, str]:
    if state.hours_left <= 0 or state.station_stability <= 0:
        return (
            "E0｜《轨道碎裂》",
            "你没能在崩溃前完成关键操作。Erebus-9 在静默中解体，所有真相随碎片坠入大气层。",
        )

    if state.memory_integrity <= 2:
        return (
            "E5｜《空白之人》",
            "你活了下来，却再也无法确认自己是谁。MINERVA将你送入新的记忆循环，‘零’重新归零。",
        )

    if "commit_ai" in state.flags and state.trust_ai >= 3:
        return (
            "E3｜《算法加冕》",
            "你把意识上传至中枢，成为空间站新的神经核心。你不再是人，却终于掌控了命运。",
        )

    if "commit_escape" in state.flags:
        if state.flags.intersection({"prep_upload", "expose_plan", "hidden_data"}):
            return (
                "E2+｜《带着真相逃亡》",
                "你驾驶逃生艇离开，将回声计划数据投向地面网络。你活下来了，战争才刚开始。",
            )
        return (
            "E2｜《无名幸存》",
            "你离开了崩坏的轨道站。没有人知道那里发生过什么，你也决定不再回头。",
        )

    if "commit_truth" in state.flags:
        if state.memory_integrity >= 8 and state.trust_human >= 4:
            return (
                "E4｜《真相烈焰》",
                "你公开了回声计划，地面政体震动。空间站付出巨大代价，但被抹去的人终于被看见。",
            )
        return (
            "E4-｜《失焦揭露》",
            "你尝试公布真相，但证据链不完整，舆论被迅速反转。你成为被追捕的泄密者。",
        )

    if state.memory_integrity >= 10 and "merged_beta" in state.flags:
        return (
            "E6｜《双零悖论》",
            "你与零-β确认：原体早已死亡，‘你们’共同构成唯一连续人格。你选择以新身份继续活下去。",
        )

    if state.station_stability >= 7 and state.ethics >= 1:
        return (
            "E1｜《灰烬守望者》",
            "你留在核心舱完成手动稳定，换来了幸存者撤离窗口。Erebus-9 仍在轨道上，守望人已不在。",
        )

    return (
        "E1-｜《沉默修复》",
        "你勉强维持了空间站运行，但失去了公开真相的机会。历史会把你记成一段无法核实的传说。",
    )


def print_status(state: GameState) -> None:
    print("\n=== 当前状态 ===")
    print(f"剩余时间: {state.hours_left} 小时")
    print(f"空间站稳定度: {state.station_stability}")
    print(f"记忆完整度: {state.memory_integrity}")
    print(f"AI 信任: {state.trust_ai}")
    print(f"人类阵营信任: {state.trust_human}")
    print(f"伦理倾向: {state.ethics}")
    print("===============\n")


def save_game(state: GameState, path: Path) -> None:
    path.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已保存到 {path}")


def load_game(path: Path) -> GameState:
    data = json.loads(path.read_text(encoding="utf-8"))
    return GameState.from_dict(data)


def run_game() -> None:
    state = GameState()
    print("\n《静默轨道：零号苏醒》")
    print("输入数字做选择；输入 status 查看状态；输入 save 或 load 存档；输入 quit 退出。\n")

    while True:
        if state.scene_id == "ending":
            ending_title, ending_text = ending_result(state)
            print(f"\n{ending_title}")
            print(ending_text)
            print("\n你的关键路径：")
            for i, action in enumerate(state.history, 1):
                print(f"{i}. {action}")
            print("\n—— 游戏结束 ——")
            return

        if state.hours_left <= 0 or state.station_stability <= 0:
            state.scene_id = "ending"
            continue

        scene = get_scene(state)
        print(f"\n[{scene.title}]")
        print(scene.content)

        available: list[Choice] = [c for c in scene.choices if choice_available(state, c)]

        if not available:
            print("\n你已无可执行方案，命运被迫收束。")
            state.scene_id = "ending"
            continue

        for index, choice in enumerate(available, 1):
            print(f"{index}. {choice.text}")

        user_input = input("\n请选择 > ").strip().lower()

        if user_input in {"quit", "q", "exit"}:
            print("你中断了任务。Erebus-9 的命运仍悬而未决。")
            return

        if user_input in {"status", "s"}:
            print_status(state)
            continue

        if user_input.startswith("save"):
            target = user_input.split(maxsplit=1)
            path = Path(target[1]) if len(target) > 1 else Path("savegame.json")
            save_game(state, path)
            continue

        if user_input.startswith("load"):
            target = user_input.split(maxsplit=1)
            path = Path(target[1]) if len(target) > 1 else Path("savegame.json")
            if not path.exists():
                print(f"未找到存档文件: {path}")
                continue
            state = load_game(path)
            print(f"已读取存档: {path}")
            continue

        if user_input in {"help", "h"}:
            print("可用命令：数字选择 / status / save [文件名] / load [文件名] / quit")
            continue

        if not user_input.isdigit():
            print("请输入有效数字或命令。")
            continue

        chosen_index = int(user_input)
        if chosen_index < 1 or chosen_index > len(available):
            print("选择超出范围，请重试。")
            continue

        apply_choice(state, available[chosen_index - 1])


if __name__ == "__main__":
    run_game()
