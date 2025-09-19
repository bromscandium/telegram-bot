import psycopg2
from config import DATABASE
from datetime import timedelta, datetime

conn = psycopg2.connect(DATABASE, sslmode="require")
cursor = conn.cursor()


# Database functions

def create_db():
    # warnings
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS warnings
                   (
                       user_id
                       BIGINT
                       PRIMARY
                       KEY,
                       warnings
                       INTEGER
                       DEFAULT
                       0,
                       reasons
                       TEXT
                   )
                   """)
    # predictions
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS predictions
                   (
                       id
                       BIGSERIAL
                       PRIMARY
                       KEY,
                       text
                       TEXT
                       NOT
                       NULL
                   )
                   """)
    conn.commit()


def add_warning(user_id, reason):
    cursor.execute("SELECT warnings, reasons FROM warnings WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    timestamp = datetime.now().strftime("%d.%m %H:%M")
    formatted_reason = f"{timestamp} {reason}"

    if result:
        warnings_count, reasons = result
        new_warning_count = warnings_count + 1
        updated_reasons = reasons + f"\n{formatted_reason}" if reasons else formatted_reason

        cursor.execute("UPDATE warnings SET warnings = %s, reasons = %s WHERE user_id = %s",
                       (new_warning_count, updated_reasons, user_id))
    else:
        cursor.execute("INSERT INTO warnings (user_id, warnings, reasons) VALUES (%s, %s, %s)",
                       (user_id, 1, formatted_reason))

    conn.commit()


def get_warning_count(user_id):
    cursor.execute("SELECT warnings FROM warnings WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    return result[0] if result else 0


def get_warning_reasons(user_id):
    cursor.execute("SELECT reasons FROM warnings WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result and result[0]:
        return result[0]
    return "—"


def reset_warnings(user_id):
    cursor.execute("UPDATE warnings SET warnings = 0 WHERE user_id = %s", (user_id,))
    conn.commit()


def get_random_prediction():
    cursor.execute("SELECT text FROM predictions ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row else "—"
