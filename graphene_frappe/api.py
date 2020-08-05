import frappe
import json
from frappe.api import get_request_form_data

import graphene
from graphene import  Schema
from graphene_frappe.graphql.query import Query
from graphene_frappe.graphql.mutations import Mutation, MyMutations


@frappe.whitelist(allow_guest=True)
def graphql():
    """ this will open end point in frappe framework to call graphql 
    http://0.0.0.0:8004/api/method/graphene_frappe.api.graphql
    """
    schema = Schema(query=Query, mutation=Mutation, auto_camelcase=False)
    data = get_request_form_data()
    query = data.get("query")
    result = schema.execute(query)
    d = json.dumps(result.data)
    return '{}'.format(d)
