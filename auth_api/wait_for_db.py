import time
import subprocess
import logging
from logging import config as logging_config
from src.core.logger import LOGGING
from contextlib import closing
import psycopg2
from psycopg2.extras import DictCursor
from src.core.config import DbSettings

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
logger = logging.getLogger('loader')


def connect_and_start(ps_connect: dict):
    db_conn = None
    logger.info('Waiting for database...')
    while not db_conn:
        try:
            with closing(
                psycopg2.connect(**ps_connect, cursor_factory=DictCursor)
            ) as pg_conn, pg_conn.cursor() as curs:
                db_conn = True

        except Exception as exc:
            logger.info('Database unavailable, waititng 1 second...')
            time.sleep(1)

    logger.info('Database available!')

    # p = subprocess.Popen(['alembic', 'revision', '-m', 'initial'])
    # p.wait()

    # p = subprocess.Popen(['alembic', 'upgrade', 'head'])
    # p.wait()

    # p = subprocess.Popen(['alembic', 'revision', '--autogenerate'])
    # p.wait()

    p = subprocess.Popen(['alembic', 'upgrade', 'head'])
    p.wait()

    p = subprocess.Popen(['python3', '-m', 'flask', 'create_admin_role', 'admin', '1234'])
    p.wait()

    subprocess.run(['python3', '/opt/auth_api/pywsgi.py'])


if __name__ == '__main__':
    ps_connect = DbSettings().dict()
    connect_and_start(ps_connect)
