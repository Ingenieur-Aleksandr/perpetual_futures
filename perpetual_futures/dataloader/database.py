from sqlalchemy import create_engine


def get_engine(user, passwd, host, port, db):
    """
    Функция для создания движка подключения к базе данных

    :param user: пользователь базы данных
    :param passwd: пароль
    :param host: хост
    :param port: порт
    :param db: наименование базы данных
    :return: sqlalchemy-движок для подключения к базе данных
    """
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    db_engine = create_engine(url, pool_size=50, echo=False)
    return db_engine

def get_engine_from_settings(db_settings: dict):
    """
    Функция для формирования движка подключения к базе на основе параметров подключения

    :param db_settings: параметры подключения
    :return: движок для работы с базой данных
    """
    keys = ['pguser', 'pgpasswd', 'pghost', 'pgport', 'pgdb']
    if not all(key in keys for key in db_settings.keys()):
        raise Exception('Проверьте корректность ключей в файле конфигурации')
    return get_engine(
        db_settings['pguser'],
        db_settings['pgpasswd'],
        db_settings['pghost'],
        db_settings['pgport'],
        db_settings['pgdb']
    )

def insert_with_progress(
        df_path: str,
        chunksize: int,
        number_of_rows: int,
        date_column_number: int,
        database_table_name: str,
        if_exists_pandas_sql_policy: str,
        db_engine
):
    """
    Функция для заполнения базы данных чанками данных из CSV файла

    :param df_path: путь к файлу с данными
    :param chunksize: размер чанка данных, который будет выгружаться
    :param number_of_rows: количество строк
    :param date_column_number: номер колонки дат
    :param database_table_name: наименование целевой таблицы в базе данных
    :param if_exists_pandas_sql_policy: инструкция по обработке заполнения существующей таблицы в базе данных
    :param db_engine: движок для подключения к базе данных
    :return:
    """
    for i, cdf in enumerate(
            pd.read_csv(
                df_path,
                chunksize=chunksize,
                parse_dates=[date_column_number]
            )
    ):
        replace = "replace" if i == 0 else if_exists_pandas_sql_policy
        cdf.to_sql(
            database_table_name,
            con=db_engine,
            if_exists=replace
        )
