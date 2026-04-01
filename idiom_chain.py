import random

def load_idioms(file_path="idiom.txt"):
    """加载成语库到本地集合，用于快速校验（判负核心）"""
    idiom_set = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            idiom = line.strip()
            if idiom and len(idiom) == 4:  # 只保留四字成语
                idiom_set.add(idiom)
    return list(idiom_set), idiom_set

def idiom_game_offline():
    print("=" * 50)
    print("📜 成语接龙游戏（纯本地离线版 · 不在文档直接判负）")
    print("🎯 规则：接最后一个字，成语必须在文档中，禁止重复")
    print("=" * 50)

    # 加载本地成语库
    idiom_list, idiom_set = load_idioms()
    if not idiom_list:
        print("❌ 错误：idiom.txt 为空或不存在，请检查文件！")
        return

    # 随机开局
    current_idiom = random.choice(idiom_list)
    used_idioms = {current_idiom}  # 记录已使用成语，避免重复
    print(f"\n🤖 机器人先出：{current_idiom}")

    while True:
        last_char = current_idiom[-1]
        user_input = input(f"\n请用【{last_char}】开头接龙：").strip()

        # 1. 基础校验：非空
        if not user_input:
            print("❌ 请输入有效成语！")
            continue

        # 2. 核心判负：校验是否在成语库中
        if user_input not in idiom_set:
            print(f"💀 游戏结束！【{user_input}】不在成语库中，你输了！")
            break

        # 3. 重复校验：避免重复使用
        if user_input in used_idioms:
            print(f"❌ 成语【{user_input}】已经用过了，不能重复！")
            continue

        # 4. 首尾字校验：匹配最后一个字
        if user_input[0] != last_char:
            print(f"❌ 错啦！必须以【{last_char}】开头！")
            continue

        # 接龙成功
        print("✅ 接龙成功！")
        used_idioms.add(user_input)

        # 机器人接龙：找以用户输入最后一个字开头的未使用成语
        robot_next_char = user_input[-1]
        found = False

        # 打乱顺序，保证每次机器人接龙不同
        random.shuffle(idiom_list)
        for idiom in idiom_list:
            if idiom.startswith(robot_next_char) and idiom not in used_idioms:
                current_idiom = idiom
                used_idioms.add(idiom)
                print(f"🤖 机器人接：{current_idiom}")
                found = True
                break

        # 机器人接不住，玩家赢
        if not found:
            print("🎉 太厉害了！机器人接不住，你赢了！")
            break

if __name__ == "__main__":
    idiom_game_offline()