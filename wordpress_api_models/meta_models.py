import json_models
from .model_managers import WPModelManager

class WPMetaModel(json_models.ModelBase):
    def __init__(cls, name, bases, attrs):
        fields = [field_name for field_name in attrs.keys() if isinstance(attrs[field_name], json_models.BaseField)]
        for field_name in fields:
            setattr(cls, field_name, cls._get_path(field_name, attrs[field_name]))
            attrs[field_name]._name = field_name
        if "finders" in attrs:
            finders = attrs["finders"]
        else:
            finders = {}
        if "prefix" in attrs:
            prefix = attrs["prefix"]
        else:
            prefix = False
        setattr(cls, "objects", WPModelManager(cls, finders, prefix))
        if "headers" in attrs:
            setattr(cls.objects, "headers", attrs["headers"])

