from datetime import datetime
from frappe import get_value

class Field(object):
    """
    Base Field Class that provides default validation,
    get and set values and set field parameters.
    :field_type: ==> type class (required)
        - determines the type of the field
    :required: ==> boolean (optional)
        - determines if the field is nullable/required.
        This field is optional with a default value of False.
    """
    field_type = None
    value = None

    def __init__(self, display_name=None, required=True, read_only=False):
        """Initialized required params and field_type."""
        self.required = required
        self.read_only = read_only
        self.display_name = display_name

    def set_value(self, value):
        """Set value for the field."""
        self.value = value
        return

    def get_value(self):
        """Retrieve value of the field."""
        return self.value

    def validate(self):
        """
        Validates the value of the field and if the field is
        required or nullable.
        """

        # Checks nullability of the field
        if self.required and not self.value:
            raise ValueError('This field is required.')

        # Return if the field is not required
        if not self.required and not self.value:
            return True

        # Validate if the given field have the correct field_type
        if self.value and not isinstance(self.value, self.field_type):
            raise ValueError('Invalid value.')

        return True


class IntegerField(Field):
    """Field for Integer values."""
    field_type = int


class CharField(Field):
    """Field for String values."""
    field_type = unicode


class BooleanField(Field):
    """Field for Boolean values."""
    field_type = bool


class DateTimeField(Field):
    """"Field for Datetime values."""
    field_type = unicode
    formatter = '%Y-%m-%d %H:%M'

    def get_value(self):
        """Returns a string representation for datetime field."""
        return self.value.strftime(self.formatter)

    def _set_object(self):
        """Private function to set object datetime field."""
        self.object = datetime.strptime(self.value, self.formatter)
        return

    def get_object(self):
        """Retrieve a datetime object representation for the field."""
        return self.object

    def validate(self):
        """Custom validation for datetime object."""
        super(DateTimeField, self).validate()
        try:
            self._set_object()
        except ValueError:
            raise ValueError(
                'Invalid format.Please use YYYY-MM-DD '
                'HH:MM with a 24 hour format.'
            )

        return True


class ChoiceField(Field):
    """Field with choices. Choices SHOULD be string."""
    field_type = unicode

    def __init__(
        self, choices,
        display_name=None,
        required=False,
        read_only=False
    ):
        """Initialize data."""
        super(ChoiceField, self).__init__(
            display_name=display_name,
            required=required,
            read_only=read_only
        )
        self.choices = choices

    def validate(self):
        """Custom validation for choicefield objects."""
        if self.value not in self.choices:
            raise ValueError(
                'Invalid value. The value given is not in the choices.'
            )

        return super(ChoiceField, self).validate()


class MoneyField(Field):
    """Field for monetary values."""
    field_type = float

    def validate(self):
        """Validation for monetary values."""
        try:
            if self.value:
                self.value = float(self.value)
        except ValueError:
            raise ValueError('Invalid value.')

        return super(MoneyField, self).validate()

class ForeignKeyField(Field):
    """
    Field for values that is a foreignkey to other doc types.
    :doc_type: ==> type str (required)
        - determines the doctype of the foreignkey field
    :field_name: ==> type str (required)
    - determines the column of the foreignkey field
    """
    field_type = unicode

    def __init__(self, doc_type, field_name, display_name=None, required=True, read_only=False):
        """ForeignKey Field with doc_type and field_name parameter."""
        self.doc_type = doc_type
        self.field_name = field_name

    def validate(self):
        """Validates if the given value is existing in the doctype's fieldname."""
        try:
            self.value = unicode(value)
            if not get_doc(self.doctype, self.value, self.field_name):
                raise ValueError('Invalid Address. Address is not existing.')
        except ValueError:
            raise ValueError('Invalid value.')

        return super(MoneyField, self).validate()