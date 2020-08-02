import frappe

class Serializer(object):

    serialized_data = None
    is_valid = False
    errors = None
    doctype = None
    doc = None

    class Meta:
        fields = []
        doctype = None
        errors = None

    def __init__(self, data, *args, **kwargs):
        self._set_serialized_data(data)

    def _set_serialized_data(self, data, *args, **kwargs):
        """
        Set the key of serialized data for fields with display name
        """
        serialized = {}
        fields_w_disp_name = [
            field for field in self.Meta.fields if (
                getattr(
                    self, field
                ).display_name is not None and getattr(
                    self, field
                ).read_only is False
            )
        ]
        fields_wo_disp_name = [
            field for field in self.Meta.fields if (
                getattr( self, field).display_name is None and getattr(
                    self, field
                ).read_only is False
            )
        ]

        for field in fields_w_disp_name:
            serialized[field] = data[getattr(self, field).display_name]
            getattr(self, field).set_value(serialized[field])

        for field in fields_wo_disp_name:
            serialized[field] = data[field]
            getattr(self, field).set_value(serialized[field])

        self.serialized_data = serialized

    def get_json(self):
        """
        returns a dictionary that has display name as key
        """
        serialized = {}
        fields_w_disp_name = [
            field for field in self.Meta.fields if getattr(
                self, field).display_name is not None
        ]
        fields_wo_disp_name = [
            field for field in self.Meta.fields if getattr(
                self, field).display_name is None
        ]

        for field in fields_w_disp_name:
            serialized[
                getattr(self, field).display_name
            ] = self.serialized_data[field]

        for field in fields_wo_disp_name:
            serialized[field] = self.serialized_data[field]

        return serialized

    def clean_fields(self):
        """
        Calls all validate method of the fields and returns error messages
        if there is a validation error.
        """
        self.is_valid = True
        err = {}
        write_fields = [
            field for field in self.Meta.fields if getattr(
                self, field).read_only==False
        ]
        for field in write_fields:
            try:
                getattr(self, field).validate()
            except ValueError as e:
                self.is_valid = False
                err[field] = [e.message]
        self.errors = err

    def _fill_read_only_fields(self, obj):
        """
        Fill the read only fields in the serialized_data
        """
        read_only_list = [
            field for field in self.Meta.fields if getattr(
                self, field).read_only==True]
        for field in read_only_list:
            self.serialized_data[field] = getattr(obj, field)

    def get_doc(self):
        """
        From serialized data, create the doc object
        """
        if not self.doc:
            data = self.serialized_data
            data['doctype'] = self.Meta.doctype
            self.doc = frappe.get_doc(data)
        return self.doc

    def save(self, *args, **kwargs):
        """
        Save the doctype
        """
        if self.errors:
            raise Exception('Errors in validation.')

        doc = self.get_doc()
        doc.validate()
        doc.insert(ignore_permissions=True)
        self._fill_read_only_fields(doc)
        return doc