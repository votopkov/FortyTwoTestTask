from django.core.management.base import NoArgsCommand
from _fucntions import count_instances


class Command(NoArgsCommand):

    help = 'Print all project models and the count of objects in every model'

    def handle(self, *args, **kwargs):
        for k, v in count_instances().items():
            row = '%s\t%d' % (k, v)
            self.stdout.write("Error: %s\n" % row)
