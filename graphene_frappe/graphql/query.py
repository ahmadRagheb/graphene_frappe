import frappe
import json

import graphene
from graphene import relay, ObjectType, String, Field, Schema ,Node,List
from graphene_frappe.graphql.schema import StockEntry, Todo, get_graphene_class


class Query(ObjectType):
    get_all = String(doctype=graphene.String(required=True))
    get_doc = Field(StockEntry, doctype=graphene.String(required=True), name=graphene.String(required=True))

    def resolve_get_doc(parent, info, doctype, name, **kwargs):
        doc = frappe.get_doc(doctype, name)
        docdict = doc.as_dict()
        return docdict

    def resolve_get_all(root, info, doctype):
        ll =  frappe.get_all(doctype)
        return ll



# {
#   get_all(doctype: "Stock Entry") 
# }

# {
#   get_doc(doctype: "Stock Entry", name: "MAT-STE-2020-00001") {
#     name
#     stock_entry_type
#     items{
#       item_code
#       qty
#       t_warehouse
#       item_group
#       idx
#     }
    
#   }
# }