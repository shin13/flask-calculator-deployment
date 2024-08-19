DROP TABLE IF EXISTS medicines;
CREATE TABLE medicines (
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
);
