from django.core.management.base import BaseCommand
from optparse import make_option
from django.contrib.contenttypes.models import ContentType
from testtask.settings import BASE_DIR
import time


filename = BASE_DIR + "/" + time.strftime("%d-%m-%Y") + ".dat"

def count_instances():
    result = {}
    for ct in ContentType.objects.all():
        m = ct.model_class()
        model_name = '%s.%s' % (m.__module__, m.__name__)
        instance_num = m._default_manager.count()
        result[model_name] = instance_num
    return result



class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--stderr-tee',
            action='store_true',
            dest='tee',
            default=False,
            help='duplicate output to stderr'),

        make_option('--stderr-prefix',
            action="store",
            type="string",
            dest='prefix',
            default='error:',
            help='prefix for stderr output'),
    )

    help = 'Print all project models and the count of objects in every model'

    def handle(self, *args, **kwargs):
        target = open(filename, 'w') #
        for k, v in count_instances().items():
            line = k + "  " + str(v) + "\n"
            target.write(line)
            row = '%s\t%d' % (k, v)
            self.stdout.write(row + "\n")
            if kwargs.get('tee'):
                prefix = kwargs.get('prefix')
                if prefix:
                    self.stderr.write('%s %s\n' % (prefix, row))
                else:
                    self.stderr.write('%s\n' % row)
        target.close()
