import graphene
from graphene import relay, ObjectType, String, Field, Schema ,Node,List 

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


class Todo(graphene.ObjectType):
    
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
