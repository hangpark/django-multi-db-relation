# django-multi-db-relation

> Queryset optimization supports for multi database spanning relations between Django models.

## Requirements

- Python (>= 3.5)
- Django (>= 1.10)

## Installation

```sh
pip install django-multi-db-relation
```

## Usage

For models

```python
class ModelA(models.Model):
    name = models.CharField(max_length=10)

class ModelB(models.Model):
    a = models.ForeignKey(ModelA, on_delete=models.DO_NOTHING)

class ModelC(models.Model):
    b = models.ForeignKey(ModelB, on_delete=models.DO_NOTHING, db_constraint=False)
```

suppose that `ModelA` and `ModelB` is routed to `db1` and `ModelC` to `db2`.

We **cannot** run a queryset with `select_related()`.

```python
>>> ModelC.objects.select_related('b') # Table not found
```

In this case, modify `ModelC` like:

```python
from multi_db_relation.mixins import ExternalDbQuerySetMixin


class ModelCQuerySet(ExternalDbQuerySetMixin, models.QuerySet):
    pass

class ModelC(models.Model):
    b = models.ForeignKey(ModelB, on_delete=models.DO_NOTHING, db_constraint=False)
    
    objects = models.Manager.from_queryset(queryset_class=ModelCQuerySet)()
    
    class Meta:
        external_db_fields = ['b']
```

then:

```python
>>> ModelC.objects.select_related('b') # Number of queries is optimized from O(n) to O(1)
>>> ModelC.objects.select_related('b__a') # Also works well
```

## License

- See [LICENSE](LICENSE)