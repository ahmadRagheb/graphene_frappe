import frappe
import graphene
from graphene_frappe.graphql.schema import StockEntry, Todo, Person, Items


# mutation  {
#     create_stock_entry(stock_entry_type:"Material Receipt",company:"ax",items:[
#       {
#         item_code: "ddc",
#   	  	qty: 2,
#       	t_warehouse: "Finished Goods - A",
#       	item_group: "All Item Groups"
#       }
#     ]) {
#         stockentry {
#             name
#             stock_entry_type
#           	items{
#               item_code
#             }
#         }
#         ok
#     }
# }

class ItemsInput(graphene.InputObjectType):
	item_code = graphene.String()
	qty = graphene.Int()
	idx = graphene.Int()
	t_warehouse = graphene.String()
	item_group = graphene.String()

class CreateStockEntry(graphene.Mutation):
    class Arguments:
        stock_entry_type = graphene.String()
        company = graphene.String()
        items = graphene.List(ItemsInput)

    ok = graphene.Boolean()
    stockentry = graphene.Field(lambda: StockEntry)

    def mutate(root, info, stock_entry_type, items , company):
        doc = frappe.new_doc("Stock Entry")
        doc.company = company
        doc.stock_entry_type = stock_entry_type
        for row in items:
            doc.append("items",  row)
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        docdict = doc.as_dict()
        ok = True
        return CreateStockEntry(stockentry=docdict, ok=ok)

# mutation  {
#     update_stock_entry(name: "MAT-STE-2020-00003", stock_entry_type:"Material Receipt",company:"ax",items:[
#       {
#         item_code: "ddc",
#   	  	qty: 7,
#       	t_warehouse: "Finished Goods - A",
#       	item_group: "All Item Groups"
#       }
#     ]) {
#         stockentry {
#             name
#             stock_entry_type
#           	items{
#               item_code
#             }
#         }
#         ok
#     }
# }

class UpdateStockEntry(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        stock_entry_type = graphene.String()
        company = graphene.String()
        items = graphene.List(ItemsInput)

    ok = graphene.Boolean()
    stockentry = graphene.Field(lambda: StockEntry)

    def mutate(root, info, name, stock_entry_type, items , company):
        doc = frappe.get_doc("Stock Entry", name)
        doc.company = company
        doc.stock_entry_type = stock_entry_type
        for row in items:
            if row.idx:
                index = row.idx-1
                if row.qty == 0:
                    [doc.items.remove(d) for d in doc.get('items') if d.idx == row.idx ]
                else:
                    for key, value in row.items():
                        if not key == 'idx':
                            dumy_dict = {key:value}
                            doc.get('items')[index].update(dumy_dict) 
            else:
                doc.append("items",  row)
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        docdict = doc.as_dict()
        ok = True
        return UpdateStockEntry(stockentry=docdict, ok=ok)

# mutation  {
#     delete_stock_entry(name: "MAT-STE-2020-00003") {
#         name
#         ok
#     }
# }

class DeleteStockEntry(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    name = graphene.String()

    def mutate(root, info, name):
        frappe.delete_doc("Stock Entry", name, ignore_permissions=True)
        frappe.db.commit()
        ok = True
        return DeleteStockEntry(name=name, ok=ok)

class CreateTodo(graphene.Mutation):
    class Arguments:
        # name = graphene.String()
        description = graphene.String()
        color = graphene.String()

    ok = graphene.Boolean()
    todo = graphene.Field(lambda: Todo)

    def mutate(root, info, name, description, color):
        doc = frappe.new_doc("ToDo")
        doc.description = description
        doc.color = color
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        docdict = doc.as_dict()
        ok = True
        return CreateTodo( todo= docdict, ok=ok)

class UpdateTodo(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        color = graphene.String()

    ok = graphene.Boolean()
    todo = graphene.Field(lambda: Todo)

    def mutate(root, info, name, description, color):
        doc = frappe.get_doc("ToDo", name)
        doc.description = description
        doc.color = color
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        docdict = doc.as_dict()
        ok = True
        return UpdateTodo( todo= docdict, ok=ok)

class DeleteTodo(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    name = graphene.String()

    def mutate(root, info, name):
        frappe.delete_doc("ToDo", name, ignore_permissions=True)
        frappe.db.commit()
        ok = True
        return DeleteTodo( name=name , ok=ok)



class Mutation(graphene.ObjectType):
    create_stock_entry = CreateStockEntry.Field()
    update_stock_entry = UpdateStockEntry.Field()
    delete_stock_entry = DeleteStockEntry.Field()

    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo =  DeleteTodo.Field()
    # create_person = CreatePerson.Field()




# class CreatePerson(graphene.Mutation):
#     class Arguments:
#         name = graphene.String()

#     ok = graphene.Boolean()
#     person = graphene.Field(lambda: Person)

#     def mutate(root, info, name):
#         person = Person(name=name)
#         ok = True
#         return CreatePerson(person=person, ok=ok)


# class MyMutations(graphene.ObjectType):
#     create_person = CreatePerson.Field()
