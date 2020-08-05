import frappe
import graphene
from graphene_frappe.graphql.schema import StockEntry, Todo, Person


class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)

    def mutate(root, info, name):
        person = Person(name=name)
        ok = True
        return CreatePerson(person=person, ok=ok)


class MyMutations(graphene.ObjectType):
    create_person = CreatePerson.Field()

class CreateTodo(graphene.Mutation):
    class Arguments:
        name = graphene.String()
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

class CreateStockEntry(graphene.Mutation):
    class Arguments:
        '''
        Arguments attributes are the arguments that the Mutation CreatePerson needs for resolving,
        in this case name will be the only argument for the mutation.
        '''
        name = graphene.String()
        # stock_entry_type = graphene.String()
        # company = graphene.String()

    ok = graphene.Boolean()
    stockentry = graphene.Field(lambda: StockEntry)

    def mutate(root, info, name):
        stockentry = StockEntry(name=name).as_dict()
        ok = True
        return CreateStockEntry(stockentry=stockentry, ok=ok)


class Mutation(graphene.ObjectType):
    create_stock_entry = CreateStockEntry.Field()
    create_todo = CreateTodo.Field()
    create_person = CreatePerson.Field()

