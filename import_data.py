import csv
import sqlite3
import os

def create_table():
    conn = sqlite3.connect('medicines.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        drug_code TEXT PRIMARY KEY,
        english_name TEXT,
        generic_name TEXT,
        main_ingredient_content REAL,
        secondary_ingredient_content REAL,
        max_daily_text REAL,
        max_daily_mg REAL,
        max_daily_ml REAL,
        max_mg_per_kg_day REAL,
        max_ml_per_kg_day REAL,
        dosing_range_text REAL,
        lowest_dose_kg REAL,
        lowest_ml_kg REAL,
        highest_dose_kg REAL,
        highest_ml_kg REAL,
        frequency TEXT
    )
    ''')

    conn.commit()
    conn.close()

def import_data():
    if not os.path.exists('medicines.csv'):
        print("Error: medicines.csv file not found!")
        return

    create_table()

    conn = sqlite3.connect('medicines.db')
    cur = conn.cursor()

    # 先清空表格
    cur.execute('DELETE FROM medicines')

    with open('medicines.csv', 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # 跳過標題行
        for row in csv_reader:
            try:
                cur.execute('''
                    INSERT INTO medicines (
                        drug_code, english_name, generic_name, main_ingredient_content,
                        secondary_ingredient_content, max_daily_text, max_daily_mg, max_daily_ml,
                        max_mg_per_kg_day, max_ml_per_kg_day, dosing_range_text, lowest_dose_kg,
                        lowest_ml_kg, highest_dose_kg, highest_ml_kg, frequency
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row[0],  # drug_code
                    row[1],  # english_name
                    row[2],  # generic_name
                    float(row[3]) if row[3] else None,  # main_ingredient_content
                    float(row[4]) if row[4] else None,  # secondary_ingredient_content
                    row[7],  # max_daily_text
                    float(row[8]) if row[8] else None,  # max_daily_mg
                    float(row[9]) if row[9] else None,  # max_daily_ml
                    float(row[10]) if row[10] else None,  # max_mg_per_kg_day
                    float(row[11]) if row[11] else None,  # max_ml_per_kg_day
                    row[12],  # dosing_range_text
                    float(row[13]) if row[13] else None,  # lowest_dose_kg
                    float(row[14]) if row[14] else None,  # lowest_ml_kg
                    float(row[15]) if row[15] else None,  # highest_dose_kg
                    float(row[16]) if row[16] else None,  # highest_ml_kg
                    row[17]  # frequency
                ))
            except Exception as e:
                print(f"Error importing row {row[0]}: {e}")

    conn.commit()
    conn.close()

    print("Data imported successfully!")

if __name__ == "__main__":
    import_data()
