from django.db import models
from django.db.models import Prefetch
from django.db.models.constants import LOOKUP_SEP


def _add_meta_attr_to_model(attr):
    if attr not in models.options.DEFAULT_NAMES:
        models.options.DEFAULT_NAMES += (attr,)


_add_meta_attr_to_model('external_db_fields')


class ExternalDbQuerySetMixin:
    """
    Mixin to support :meth:`select_related()` with external database models.

    Specify names of relational fields with external database models as string list
    to an attribute named :attr:`external_db_fields` on the model's :class:`Meta` class.
    And then use a custom queryset inherits this mixin.
    """
    def select_related(self, *fields):
        if self._fields is not None:
            raise TypeError("Cannot call select_related() after .values() or .values_list()")

        target_fields = self.model._meta.external_db_fields
        select_fields = []
        prefetch_map = {}

        for field in fields:
            splitted_field = field.split(LOOKUP_SEP, 1)
            if splitted_field[0] in target_fields:
                prefetch_map.setdefault(splitted_field[0], [])
                prefetch_map[splitted_field[0]] += splitted_field[1:]
            else:
                select_fields.append(splitted_field[0])

        obj = super().select_related(*select_fields) if select_fields else self._chain()

        for field, select_fields in prefetch_map.items():
            TargetModel = self.model.__dict__[field].field.related_model
            queryset = TargetModel.objects.all()
            if select_fields:
                queryset = queryset.select_related(*select_fields)
            obj = obj.prefetch_related(Prefetch(field, queryset))

        return obj
