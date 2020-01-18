import inspect
from itertools import islice
from abc import ABCMeta, abstractmethod
from graphql import GraphQLError


class FormValidator:
    __metaclass__ = ABCMeta

    def __init__(self, data):
        self.data = data
        self.cleaned_data = {}
        self.errors = {}

    def is_valid(self):
        for name, validator in inspect.getmembers(self, predicate=inspect.ismethod):
            if "validate_" in name:
                validator()
        return not self.errors

    @abstractmethod
    def save(self):
        pass


class BulkManager(object):
    def __init__(self, model, items=[], update_dict={}, removed_items=[], batch_size=100):

        self.model = model
        self.update_dict = update_dict
        self.batch_size = batch_size
        self.removed_items = removed_items

        self.new_items = list(filter(lambda item: not item.get("id"), items))
        self.existing_items = list(
            filter(lambda item: item.get("id") is not None, items)
        )

        if self.new_items:
            self.bulk_create()
        if self.existing_items:
            self.bulk_update()
        if self.removed_items:
            self.bulk_delete()

    def _prepare_bulk_create_data(self):
        for item in self.new_items:
            item.update(self.update_dict)
            yield self.model(**item)

    def _prepare_bulk_update_data(self):
        for item in self.existing_items:
            item.update(self.update_dict)
            yield self.model(**item)

    def bulk_create(self):
        data = self._prepare_bulk_create_data()
        while True:
            items = list(islice(data, self.batch_size))
            if not items:
                break
            self.model.objects.bulk_create(items, self.batch_size)

    def bulk_update(self):
        field_item = self.existing_items[0]
        fields = list(filter(lambda key: key is not "id", field_item.keys()))
        data = self._prepare_bulk_update_data()

        while True:
            items = list(islice(data, self.batch_size))
            if not items:
                break
            self.model.objects.bulk_update(items, fields)

    def bulk_delete(self):
        ids = [item.get("id") for item in self.removed_items if item.get("id")]
        del_objs = self.model.objects.filter(pk__in=ids)
        if del_objs.exists():
            del_objs._raw_delete("default")


def can(*permissions):
    def wrapped_decorator(func):
        def inner(cls, info, *args, **kwargs):
            
            if not info.context:
                raise GraphQLError("Permission Denied.")

            user = info.context.user
            if not user.is_authenticated or not user.role:
                raise GraphQLError("Permission Denied.")

            # An admin (Django superusers) can do everything.
            if user.is_superuser:
                return func(cls, info, **kwargs)

            # A user CAN perform an action, if he has ANY of the requested permissions.
            user_permissions = list(
                user.role.rights.all().values_list("codename", flat=True)
            )

            if any(permission in user_permissions for permission in permissions):
                return func(cls, info, **kwargs)
            raise GraphQLError("Permission Denied.")

        return inner

    return wrapped_decorator
