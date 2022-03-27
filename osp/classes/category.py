from mongoengine import Document,StringField

class Category(Document):
    name = StringField(required = True , min_length=1)
    uid = StringField()       # default empty, then assigned

    @staticmethod
    def add_category(name):
        try:
            new_category = Category(name = name)
            new_category.save()
            new_category.update(uid = str(id))
            return(True,"Category successfully created")

        except Exception as e:
            return(False,str(e))

    @staticmethod
    def delete_category(someid):
        try:
            Category.objects(uid = str(someid)).delete()   # delete the category with that id
            return (True,"Category and corresponding items successfully deleted")

        except Exception as e:
            return (False, str(e))

