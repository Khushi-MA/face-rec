import random
from datetime import datetime, timedelta

# Configuration
start_time = datetime(2025, 3, 1, 0, 0, 0)
total_days = 30
samples_per_day = 48
id_counter = 9000  # Change if needed

# SQL start
sql_lines = ["INSERT INTO sensors1.demo_sensordata (id, sensor_id, device_name, timestamp, temperature, moisture, conductivity, pH, led_status, overall_moisture, status, last_seen) VALUES"]

# Generate 1440 entries
rows = []
for day in range(total_days):
    for sample in range(samples_per_day):
        timestamp = start_time + timedelta(days=day, minutes=sample * 30)
        last_seen = timestamp - timedelta(seconds=1)

        temperature = round(random.uniform(25.0, 35.0), 2)
        moisture = random.choice([0, 30, 60, 90])
        conductivity = round(random.uniform(2.0, 3.5), 2)
        pH = round(random.uniform(6.5, 7.5), 1)
        led_status = 'ON' if moisture < 40 else 'OFF'
        overall_moisture = moisture
        status = 'online' if moisture > 0 else 'offline'

        row = f"({id_counter}, 1, 'ASD2025', '{timestamp}', {temperature}, {moisture}, {conductivity}, {pH}, '{led_status}', {overall_moisture}, '{status}', '{last_seen}')"
        rows.append(row)
        id_counter += 1

# Finish SQL
sql_lines.append(",\n".join(rows) + ";")

# Write to file
with open("insert_dummy_data.sql", "w") as f:
    f.write("\n".join(sql_lines))

print("✅ SQL file 'insert_dummy_data.sql' generated with 1440 rows.")
