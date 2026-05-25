import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Aguarda até que o banco de dados esteja disponível.'

    def handle(self, *args, **options):
        self.stdout.write('Aguardar conexão com o banco de dados...')
        db_conn = connections['default']

        while True:
            try:
                db_conn.ensure_connection()
                break
            except OperationalError:
                self.stdout.write('Banco de dados ainda não está pronto. Tentando de novo em 1 segundo...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Conexão com o banco de dados estabelecida.'))
