from django.core.management.base import BaseCommand, CommandError

from gedgo.gedcom_update import update
from os import path

class Command(BaseCommand):
    help = 'Adds a new gedcom with a given .ged file.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the .ged file')

    def handle(self, *args, **options):
        file_name = options['file_path']
        if not path.exists(file_name):
            raise CommandError('Gedcom file "%s" not found.' % file_name)
        if (not len(file_name) > 4) or (not file_name[-4:] == '.ged'):
            raise CommandError(
                'File "%s" does not appear to be a .ged file.' % file_name)

        update(None, file_name)