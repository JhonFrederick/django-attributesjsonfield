from django.forms import MultiValueField, CharField


from attributesjsonfield.widgets import AttributesJSONWidget


class AttributesJSONField(MultiValueField):
    """ """

    widget = AttributesJSONWidget

    def __init__(self, *args, attributes=None, require_all_fields=False, **kwargs):
        self.attributes = attributes

        self.clean_attributes = []
        if self.attributes:
            for attr in self.attributes:
                field = attr["field"] if type(attr) == dict else attr
                if type(attr) == dict:
                    label = attr.get("verbose_name", field)
                else:
                    label = field.replace("!", "")
                required = field.startswith("!")
                self.clean_attributes.append(
                    {
                        "field": field,
                        "label": label,
                        "name": field.replace("!", ""),
                        "choices": attr.get("choices") if type(attr) == dict else None,
                        "required": required,
                        "default": attr.get("default") if type(attr) == dict else None,
                        "data_type": attr.get("data_type")
                        if type(attr) == dict
                        else None,
                    }
                )
        else:
            self.clean_attributes = None
        fields = [
            CharField(
                label=attr["label"],
                initial=attr.get("default"),
                required=attr["required"],
            )
            for attr in self.clean_attributes
        ]
        self.widget = AttributesJSONWidget(attributes_json=self.clean_attributes)
        super().__init__(
            *args, fields=fields, require_all_fields=require_all_fields, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            data = {}
            for i, attribute in enumerate(self.clean_attributes):
                data[attribute["name"]] = data_list[i]
            return data
        return None