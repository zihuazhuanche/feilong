#!/usr/bin/env python3
"""
每日定时提醒脚本
- 早上8:30（00:30 UTC）：今日任务 + push附自拍照
- 晚上17:30（09:30 UTC）：今日总结 + 明日计划附自拍照
"""

import time
from datetime import datetime, timedelta
import subprocess
import sys

def send_discord_message(message):
    """发送Discord消息"""
    try:
        subprocess.run([
            'message', 'send',
            '--target', '1468630738135158886',
            '--message', message
        ], check=True, capture_output=True)
        print(f"✅ 消息已发送: {message[:50]}...")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

def take_selfie():
    """拍摄自拍照"""
    try:
        # 使用 nodes camera_snap
        subprocess.run([
            'nodes', 'camera_snap',
            '--facing', 'front',
            '--delayMs', '2000',
            '--quality', '80'
        ], check=True, capture_output=True)
        print("✅ 自拍照已拍摄")
        return True
    except Exception as e:
        print(f"❌ 拍照失败: {e}")
        return False

def time_until_next_target():
    """计算到下一个目标时间的秒数"""
    now = datetime.now()
    # 设置目标时间（UTC）
    morning = now.replace(hour=0, minute=30, second=0, microsecond=0)
    evening = now.replace(hour=9, minute=30, second=0, microsecond=0)

    # 如果今天的时间已过，设置为明天
    if morning < now:
        morning += timedelta(days=1)
    if evening < now:
        evening += timedelta(days=1)

    # 找到下一个更近的目标
    morning_seconds = (morning - now).total_seconds()
    evening_seconds = (evening - now).total_seconds()

    if morning_seconds < evening_seconds:
        return morning_seconds, "morning"
    else:
        return evening_seconds, "evening"

def morning_routine():
    """早上8:30例程"""
    print(f"\n{'='*50}")
    print(f"🌅 早上8:30例程 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    # 发送今日任务提醒
    message = "⏰ **早安提醒**（8:30）\n\n📋 **今日任务清单**\n- [ ] 任务1：\n- [ ] 任务2：\n- [ ] 任务3：\n\n📸 准备拍摄工作照..."
    send_discord_message(message)

    # 拍摄自拍照
    take_selfie()

    # 提醒push到平台
    message = "💪 **任务推送提醒**\n\n✨ 当前准备推送到学习/工作平台\n📸 已附带工作照\n\n🔍 确认：1.今日任务 2.工作照"
    send_discord_message(message)

def evening_routine():
    """晚上17:30例程"""
    print(f"\n{'='*50}")
    print(f"🌆 晚上17:30例程 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    # 发送今日总结提醒
    message = "⏰ **晚间总结提醒**（17:30）\n\n📊 **今日完成情况**\n- ✅ 完成任务：\n- 🚧 进行中：\n- ⏰ 待完成：\n\n📝 **今日总结**：______________________\n\n📅 **明日计划**\n- [ ] 计划1：\n- [ ] 计划2：\n- [ ] 计划3：\n\n📸 准备拍摄结束照..."
    send_discord_message(message)

    # 拍摄自拍照
    take_selfie()

    # 确认总结和计划
    message = "✅ **晚间确认**\n\n📊 今日总结已完成\n📅 明日计划已制定\n📸 已附带结束照\n\n💤 祝愿好梦！"
    send_discord_message(message)

def main():
    """主循环"""
    print("🚀 每日定时提醒服务启动")
    print(f"📍 时区: UTC (北京时间 UTC+8)")
    print(f"🌅 早上: 00:30 UTC (8:30 北京)")
    print(f"🌆 晚上: 09:30 UTC (17:30 北京)")
    print(f"🕐 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    try:
        while True:
            seconds, period = time_until_next_target()

            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)

            if period == "morning":
                print(f"\n⏰ 下次提醒: 早上8:30（{hours}小时{minutes}分钟后）")
            else:
                print(f"\n⏰ 下次提醒: 晚上17:30（{hours}小时{minutes}分钟后）")

            print(f"💤 等待中... (Ctrl+C 退出)")

            # 等待
            time.sleep(seconds)

            # 执行相应的例程
            now = datetime.now()
            if now.hour == 0 and now.minute >= 30:
                morning_routine()
            elif now.hour == 9 and now.minute >= 30:
                evening_routine()

    except KeyboardInterrupt:
        print("\n\n👋 定时提醒服务已停止")
        return 0
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
