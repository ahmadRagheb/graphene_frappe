import frappe
import json

import graphene
from graphene import relay, ObjectType, String, Field, Schema ,Node,List 

# from graphene_frappe.graphql.serializers import Serializer
# from graphene_frappe.graphql.fields import CharField

class TodoGraphene(graphene.ObjectType):
    
    name = graphene.String()
    color = graphene.String()
    status = graphene.String()
    date = graphene.Date()

    def resolve_name(parent, info):
        return parent.get("name")

    def resolve_color(parent, info):
        return parent.get("color")

    def resolve_status(parent, info):
        return parent.get("status")

    def resolve_date(parent, info):
        return parent.get("date")

class StockEntry(graphene.ObjectType):
    
    name = graphene.String()
    stock_entry_type = graphene.String()
    title = graphene.String()
    naming_series = graphene.String()
    outgoing_stock_entry = graphene.String()
    purpose = graphene.String()
    company = graphene.String()
    posting_date = graphene.Date()
    items = graphene.String()

    def resolve_name(parent, info):
        return parent.get("name")

    def resolve_stock_entry_type(parent, info):
        return parent.get("name")

    def resolve_title(parent, info):
        return parent.get("title")
    def resolve_naming_series(parent, info):
        return parent.get("naming_series")
    def resolve_outgoing_stock_entry(parent, info):
        return parent.get("outgoing_stock_entry")
    def resolve_purpose(parent, info):
        return parent.get("purpose")
    def resolve_company(parent, info):
        return parent.get("company")
    def resolve_posting_date(parent, info):
        return parent.get("posting_date")
    def resolve_items(parent, info):
        items = parent.get("items")
        return items
        # itemss = parent.get("items")
        # re = []
        # for row in itemss :
        #     re.append(row.as_dict())
        # return re


class Query(ObjectType):

    getall = String(doctype=graphene.String(required=True))
    getdoc = Field(StockEntry, doctype=graphene.String(required=True), name=graphene.String(required=True))
    hello = String(name=graphene.String(required=True))
    goodbye = String()

    def resolve_getdoc(parent, info, doctype, name, **kwargs):
        doc = frappe.get_doc(doctype, name)
        return doc.as_dict()

        
    def resolve_getall(root, info, doctype):
        ll =  frappe.get_all(doctype)
        return ll

    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'







# class genericDoc(graphene.ObjectType):
#     doctype = parent.get('doctype')
#     metaData = frappe.model.meta.Meta(doctype)
#     result = convert_doc_to_dict(metaData)
    

# def convert_doc_to_dict(doc):
#     result = {}
#     for field in doc.as_dict().get('fields'):
#         name = field.get('fieldname')
#         fieldtype= field.get('fieldtype')
#         result[name]=fieldtype
#     return result