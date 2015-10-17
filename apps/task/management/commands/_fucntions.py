from django.contrib.contenttypes.models import ContentType


def count_instances():
    result = {}
    for ct in ContentType.objects.all():
        m = ct.model_class()
        model_name = '%s.%s' % (m.__module__, m.__name__)
        instance_num = m._default_manager.count()
        result[model_name] = instance_num
    return result
