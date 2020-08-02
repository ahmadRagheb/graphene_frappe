import frappe
import json
from frappe.api import  get_request_form_data

import graphene
from graphene import ObjectType, String, Field, Schema
from graphene_frappe.graphql.query import Query

@frappe.whitelist(allow_guest=True)
def graphql():
    schema = Schema(query=Query, auto_camelcase=False)
    data = get_request_form_data()
    query = data.get("query")
    result = schema.execute(query)
    d = json.dumps(result.data)
    return '{}'.format(d)
