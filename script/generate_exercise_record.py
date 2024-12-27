import csv
from datetime import datetime, timedelta
import random

# 定义生成数据的数量
num_records = 20

# 定义可能的运动类型
exercise_types = ['跑步', '散步', '游泳', '自由活动']

# 打开一个文件用于写入CSV数据
with open('exercise_info.csv', 'w', newline='') as csvfile:
    fieldnames = ['exercise_id', 'user_id', 'type', 'start_time', 'end_time', 'calorie_cost']
    writer = csv.writer(csvfile)

    # 写入表头
    writer.writerow(fieldnames)

    # 生成数据并写入CSV文件
    for i in range(1, num_records + 1):
        # 随机生成用户ID
        user_id = 3

        # 随机选择运动类型
        exercise_type = random.choice(exercise_types)

        # 随机生成开始时间
        start_time = datetime.now() - timedelta(days=random.randint(1, 30))

        # 随机生成持续时间（分钟）
        duration_minutes = random.randint(30, 180)

        # 计算结束时间
        end_time = start_time + timedelta(minutes=duration_minutes)

        # 计算卡路里消耗（假设的计算方法）
        calorie_cost = random.randint(100, 800)  # 假设卡路里消耗范围是100到800

        # 创建记录
        record = [
            i,
            user_id,
            exercise_type,
            start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            end_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            calorie_cost
        ]

        # 写入记录
        writer.writerow(record)

print("CSV文件已生成。")