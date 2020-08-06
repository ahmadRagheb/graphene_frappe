import frappe
import graphene
from graphene import relay, ObjectType, String, Field, Schema ,Node,List 
from datetime import datetime
from frappe.model import no_value_fields

# no_value_fields = ('Section Break', 'Column Break', 'HTML', 'Table',
#  'Table MultiSelect', 'Button', 'Image',
# 	'Fold', 'Heading')


frappe_to_graphene = {
    "Date": graphene.Date
}

def get_graphene_class(doctype, suffix='Graphene'):
	docfields = frappe.get_all('DocField', fields=['fieldname', 'fieldtype'], filters={'parent': doctype})
	docfields.extend(frappe.get_all('Custom Field', fields=['fieldname', 'fieldtype'], filters={'dt': doctype}))
	attrs={
		df.fieldname: frappe_to_graphene.get(df.get('fieldtype'), graphene.String)()
		for df in docfields
		if df.get('fieldtype') not in no_value_fields
	}
	attrs['name'] = graphene.String()
	def cls_resolve_get_doc(self, parent, info, name, **kwargs):
		return resolve_get_doc(parent, info, doctype, **kwargs)
		
	cls_resolve_get_doc.__name__ = "resolve_get_doc"

	attrs["resolve_get_doc"] = cls_resolve_get_doc

	return type(doctype.replace(' ','').strip() + suffix, (graphene.ObjectType,), attrs)

class Items (graphene.ObjectType):
	item_code = graphene.String()
	qty = graphene.Int()
	t_warehouse = graphene.String()
	item_group = graphene.String()
	idx = graphene.Int()

class StockEntry(graphene.ObjectType):
	name = graphene.String()
	stock_entry_type = graphene.String()
	title = graphene.String()
	naming_series = graphene.String()
	outgoing_stock_entry = graphene.String()
	purpose = graphene.String()
	company = graphene.String()
	posting_date = graphene.Date()
	items = graphene.List(Items)

	def resolve_items(self, args):
		items = self.get('items')
		return items

class Todo(graphene.ObjectType):
	name = graphene.String()
	color = graphene.String()
	status = graphene.String()
	date = graphene.Date()
	description = graphene.String()


class Person(graphene.ObjectType):
	""" we defined the schema for Stock Entry Doctype 
		by defind the type for each field in doctype and resolve them .
		to use it in query 
	"""
	name = graphene.String()
	age = graphene.Int()
