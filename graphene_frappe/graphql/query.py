import frappe
import json

import graphene
from graphene import relay, ObjectType, String, Field, Schema ,Node,List 
from graphene_frappe.graphql.schema import StockEntry,Todo
# from graphene_frappe.graphql.serializers import Serializer
# from graphene_frappe.graphql.fields import CharField


class Query(ObjectType):

    getall = String(doctype=graphene.String(required=True))
    getdoc = Field(StockEntry, doctype=graphene.String(required=True), name=graphene.String(required=True))

    def resolve_getdoc(parent, info, doctype, name, **kwargs):
        doc = frappe.get_doc(doctype, name)
        return doc.as_dict()

    def resolve_getall(root, info, doctype):
        ll =  frappe.get_all(doctype)
        return ll