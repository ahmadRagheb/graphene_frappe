import frappe
import json

import graphene
from graphene import relay, ObjectType, String, Field, Schema ,Node,List
from graphene_frappe.graphql.schema import StockEntry, Todo, get_graphene_class

class Query(ObjectType):
    """ defined query to be executed
        we have two querys getall which returns the name(PK) of all Stock entry in the system
        also getdoc that reterns all the data based on the schema we defined  
     """
    getall = String(doctype=graphene.String(required=True))
    # getdoc = Field(StockEntry, doctype=graphene.String(required=True), name=graphene.String(required=True))
    get_doc = Field(Todo ,doctype=graphene.String(required=True), name=graphene.String(required=True))

    def resolve_get_doc(parent, info, doctype, name, **kwargs):
        doc = frappe.get_doc(doctype, name)
        docdict = doc.as_dict()
        return docdict

        # ToDoGraphene = get_graphene_class(doctype)

        # clean = {}
        # for x in docdict:
        #     if x in ToDoGraphene._meta.fields:
        #         clean[x] = docdict.get(x)

        # suffix = 'Graphene'
        # modelName = doctype.replace(' ','').strip() + suffix
        # user = ToDoGraphene(**clean) if clean else None
        # return user

    def resolve_getall(root, info, doctype):
        ll =  frappe.get_all(doctype)
        return ll