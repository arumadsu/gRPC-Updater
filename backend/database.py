import sqlite3
import logging

# Имя файла нашей базы данных (он создастся автоматически в папке backend)
DB_FILE = 'versions_cache.db'

# def get_connection():
#     conn = sqlite3.connect


def init_db():
    """
    Создает таблицу для версий, если ее еще нет.
    Эту функцию мы будем вызывать при старте gRPC-сервера.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Создаем таблицу.
    # Обрати внимание: названия колонок совпадают с полями в твоем .proto!
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS versions (
                       dir_name TEXT PRIMARY KEY,
                       build_tag TEXT,
                       version_name TEXT
                   )
                   ''')

    conn.commit()
    conn.close()
    logging.info("База данных SQLite инициализирована.")


def save_versions_to_cache(versions_list):
    """
    Сохраняет свежий список версий с FTP в базу данных.
    versions_list - это список словарей, которые вернула твоя функция парсинга FTP.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Сначала очищаем старый кэш, чтобы удалить удаленные с FTP версии
        cursor.execute('DELETE FROM versions')

        # Теперь записываем новые данные
        for v in versions_list:
            cursor.execute('''
                           INSERT INTO versions (dir_name, build_tag, version_name)
                           VALUES (?, ?, ?)
                           ''', (
                               v.get('dir_name', ''),
                               v.get('BUILD_TAG', ''),
                               v.get('version_name', '')
                           ))

        conn.commit()
        logging.debug(f"В кэш БД сохранено {len(versions_list)} версий.")
    except Exception as e:
        logging.error(f"Ошибка при записи в БД: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_cached_versions():
    """
    Достает все версии из базы данных.
    Именно эту функцию будет мгновенно вызывать наш gRPC-сервер, вместо долгого похода на FTP!
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Достаем все записи и сортируем их по тегу сборки по убыванию (как было в твоем main.py)
    cursor.execute('SELECT dir_name, build_tag, version_name FROM versions ORDER BY build_tag DESC')
    rows = cursor.fetchall()
    conn.close()

    # Превращаем сырые строки из БД обратно в список словарей
    versions = []
    for row in rows:
        versions.append({
            'dir_name': row[0],
            'build_tag': row[1],
            'version_name': row[2]
        })

    return versions