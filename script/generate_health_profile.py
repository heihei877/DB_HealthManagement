import csv
from datetime import datetime, timedelta
import random

# 定义生成数据的数量
num_records = 100

# 定义时间范围的开始和结束日期
start_date = datetime(2024, 12, 1)
end_date = datetime(2024, 12, 31)

# 打开一个文件用于写入CSV数据
with open('health_profile.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'timestamp', 'height', 'weight', 'systolic_bp', 'diastolic_bp', 'blood_sugar', 'user_id']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

    # 生成数据并写入CSV文件
    for i in range(1, num_records + 1):
        # 随机生成数据
        random_height = round(random.uniform(150.00, 200.00), 2)
        random_weight = round(random.uniform(50.00, 100.00), 2)
        random_systolic_bp = round(random.uniform(90.00, 150.00), 2)
        random_diastolic_bp = round(random.uniform(60.00, 100.00), 2)
        random_blood_sugar = round(random.uniform(70.00, 120.00), 2)

        # 随机生成时间戳
        random_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )

        # 创建记录
        record = {
            'id': i,
            'timestamp': random_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'height': f"{random_height:.2f}",
            'weight': f"{random_weight:.2f}",
            'systolic_bp': f"{random_systolic_bp:.2f}",
            'diastolic_bp': f"{random_diastolic_bp:.2f}",
            'blood_sugar': f"{random_blood_sugar:.2f}",
            'user_id': 3  # 假设所有记录的用户ID都是1
        }

        # 写入记录
        writer.writerow(record)

print("CSV文件已生成。")