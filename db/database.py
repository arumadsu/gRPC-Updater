import sqlite3
import logging

DB_FILE = 'versions_cache.db'


def get_connection():
    """Вспомогательная функция для создания соединения с нужными настройками (PRAGMA и Row)"""
    conn = sqlite3.connect(DB_FILE)

    # Оптимизация #5: Возвращать строки как словари
    conn.row_factory = sqlite3.Row

    # # Оптимизация #4: Включаем WAL-режим для параллельного чтения и записи
    # conn.execute('PRAGMA journal_mode=WAL;')
    # conn.execute('PRAGMA synchronous=NORMAL;')
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS versions (
                       dir_name TEXT PRIMARY KEY,
                       build_tag TEXT,
                       version_name TEXT
                   )
                   ''')
    conn.commit()
    conn.close()
    logging.info("База данных SQLite инициализирована (WAL mode On).")


def save_versions_to_cache(versions_list):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM versions')  # Оптимизация #3: Оставляем, это быстро

        # Подготавливаем данные для executemany
        data_to_insert = [
            (v.get('dir_name', ''), v.get('BUILD_TAG', ''), v.get('version_name', ''))
            for v in versions_list
        ]

        # Оптимизация #1: Массовая вставка
        cursor.executemany('''
                           INSERT INTO versions (dir_name, build_tag, version_name)
                           VALUES (?, ?, ?)
                           ''', data_to_insert)

        conn.commit()
        logging.debug(f"В кэш БД сохранено {len(versions_list)} версий.")
    except Exception as e:
        logging.error(f"Ошибка при записи в БД: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_cached_versions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT dir_name, build_tag, version_name FROM versions ORDER BY build_tag DESC')
    rows = cursor.fetchall()
    conn.close()

    # Оптимизация #5: Моментальное превращение в список словарей
    return [dict(row) for row in rows]


#
# сделать структуру директорий