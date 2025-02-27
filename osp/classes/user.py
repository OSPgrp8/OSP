from mongoengine import Document,StringField,EmailField,IntField,DateField,ReferenceField,NULLIFY,CASCADE
from osp.classes.address import Address
from osp.classes.category import Category

TYPE = ("Manager" , "Buyer" , "Seller")
GENDER = ("Male" , "Female" , "Others")

class User(Document):
    uid = StringField()
    password = StringField(minlength = 8,required = True)
    name = StringField(required = True,minlength = 1)
    email = EmailField(required = True)
    address = ReferenceField(Address,required=True,reverse_delete_rule=NULLIFY)
    telephone = IntField(required=True, min_value=1000000000, max_value=9999999999)

    meta = {'allow_inheritance' : True}

    def change_data(self,**kwargs):
        try:
            if "name" in kwargs :
                self.name = kwargs["name"]
            if "email" in kwargs:
                self.email = kwargs["email"]
            if "address" in kwargs:
                self.address = kwargs["address"]
            if "telephone" in kwargs:
                self.telephone = kwargs["telephone"]
            self.save()
            return (True, "Profile information updated successfully")

        except Exception as ex:
            return False, str(ex)

    def change_password(self,oldpass, newpass):
        try:
            if oldpass != self.password :
                raise Exception("Wrong password!")
            self.password = newpass
            self.save()
            return True, "Password changed"

        except Exception as ex:
            return False,str(ex)


class Manager(User):
    gender = StringField(required=True, choices=GENDER)
    dob = DateField(required=True)

    @staticmethod
    def create_manager(**kwargs):
        try:
            new_manager = Manager(
                password = kwargs["password"],
                name = kwargs["name"],
                email = kwargs["email"],
                address = kwargs["address"],
                telephone = kwargs["telephone"])
            new_manager.save()
            new_manager.uid = str(new_manager.id)
            new_manager.save()
            return True, new_manager.uid

        except Exception as ex:
            return False, str(ex)

    def type(self):
        return "Manager"

    @staticmethod
    def signup_key():                       # mimicking static variables
        return str("for_managers_only")


    def change_category(self, item_id, category_id):
        from osp.classes.item import Item
        try:
            item_ = Item.objects(uid=item_id).first()
            if not item_:
                raise Exception("No such item found!")

            category_ = Category.objects(uid=category_id).first()
            if not category_:
                raise Exception("No such category exists!")

            item_.category = category_
            item_.save()
        except Exception as ex:
            return False,str(ex)


    # for adding and removing categories, the static add and remove categories of the class Category can be used directly. No special methods are required in class Manager
    # similarly for deleting items, the static method delete item of class Item can be used directly


    def manage_seller(self,seller_id):
        try:
            seller = Seller.objects(uid=seller_id).first()
            if seller:
                seller.delete()
                return True, "Seller deleted"
            else :
                raise Exception("No such seller found!")

        except Exception as ex:
            return  False, str(ex)

    def manage_buyer(self, buyer_id):
        try:
            buyer = Buyer.objects(uid=buyer_id).first()
            if buyer:
                buyer.delete()
                return True, "Buyer deleted"
            else:
                raise Exception("No such buyer found!")

        except Exception as ex:
            return  False, str(ex)


    #def audit(self):    # implement after class Buy Requests

    #def negotiations(self,seller_id,buyer_id):   # implement after class Buy Requests


class Seller(User):
    # for adding and deleting products, static methods of Class Item can be used

    @staticmethod
    def create_seller(**kwargs):
        try:
            new_seller = Seller(
                password = kwargs["password"],
                name = kwargs["name"],
                email = kwargs["email"],
                address = kwargs["address"],
                telephone = kwargs["telephone"]
            )
            new_seller.save()
            new_seller.uid = str(new_seller.id)
            new_seller.save()
            return True, new_seller.uid

        except Exception as ex:
            return False, str(ex)

    def view_pending_orders(self):
         from osp.classes.order import Order
         return Order.objects(seller=self)

    def view_sales(self):
         from osp.classes.order import Transaction
         return Transaction.objects(seller = self)

    def negotiate(self,order_id,offer):
        from osp.classes.order import Order
        try:
            order = Order.objects(uid = order_id).first()
            order.negotiate(offer)
            return True,"Offer Placed"

        except Exception as ex:
            return False, str(ex)
                                                       # order is an object of class Order
    def update_order_status(self,order_id,status):     # status is an enumeration of REQUEST_STATUS
        from osp.classes.order import Order,Transaction
        try:
            order = Order.objects(uid = order_id).first()
            if not order:
                raise Exception("No such order found!")

            if status == "ACCEPTED":
                order.request_status = "ACCEPTED"
                return True, "Request accepted"

            elif status == "REJECTED":
                order.item.on_sale = True
                order.item.save()
                order.delete()
                # send mails
                return True, "Request rejected"

        except Exception as ex:
            return False, str(ex)


class Buyer(User):

    @staticmethod
    def create_buyer(**kwargs):
        try:
            new_buyer = Buyer(
                password = kwargs["password"],
                name = kwargs["name"],
                email = kwargs["email"],
                address = kwargs["address"],
                telephone = kwargs["telephone"]
            )
            new_buyer.save()
            new_buyer.uid = str(new_buyer.id)
            new_buyer.save()
            return True, new_buyer.uid

        except Exception as ex:
            return False, str(ex)

    def raise_purchase_request(self,item_id,offer):
        from osp.classes.order import Order,Transaction
        from osp.classes.item import Item
        try:
            item = Item.objects(uid = item_id).first()
            if not item :
                raise Exception("No such item found!")

            seller = Seller.objects(uid = item.seller.uid).first()
            if not seller :
                raise Exception("No such seller found!")

            order_id = Order.create_order(offer_price = offer , item = item.uid , seller = seller.uid , buyer = self.uid)[1]
            item.on_sale = False
            item.save()

            return True, order_id

        except Exception as ex:
            return False, str(ex)

    def negotiate(self,order_id,offer):
        from osp.classes.order import Order,Transaction
        try:
            order = Order.objects(uid = order_id).first()
            if not order :
                raise Exception("No such order exists!")

            order.negotiate(offer)
            return True, "Negotiation request Placed"

        except Exception as ex:
            return False, str(ex)

    def payment(self,order_id):
        from osp.classes.order import Order,Transaction
        try:
            order = Order.objects(uid = order_id).first()
            if not order :
                raise Exception("No such order exists!")

            if order.request_status == "ACCEPTED":
                transaction_id = Transaction.create_transaction(order_id)[1]
                order.item.delete()                 # check cascade deletion
                order.delete()
                return True, transaction_id

            else:
                raise Exception("Request has not yet been approved")

        except Exception as ex:
            return True, str(ex)


    def view_pending_orders(self):
         from osp.classes.order import Order
         return Order.objects(buyer=self)

    def view_purchases(self):
         from osp.classes.order import Transaction
         return Transaction.objects(buyer = self)

































