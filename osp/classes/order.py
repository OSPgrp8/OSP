from mongoengine import Document,FloatField,BooleanField,ReferenceField,StringField,ImageField,CASCADE
from osp.classes.item import Item
from osp.classes.user import Seller,Buyer

REQUEST_STATUS = ("Pending","Rejected","Accepted")


class Order(Document):
    uid = StringField()
    offer_price = FloatField(required=True,min_value=0)
    item = ReferenceField(Item,reverse_delete_rule=CASCADE,required = True)
    buyer = ReferenceField(Buyer,reverse_delete_rule=CASCADE,required = True)
    seller = ReferenceField(Seller,reverse_delete_rule=CASCADE,required = True)
    request_status = StringField(default="Pending",choices = REQUEST_STATUS)
    delivery_status = BooleanField(default = False)
    payment_status = BooleanField(default = False)

    @staticmethod
    def create_order(**kwargs):
        try:
            order_item = Item.objects(uid=kwargs['item']).first()
            if not order_item:
                raise Exception("No such item exists!")

            order_buyer = Buyer.objects(uid=kwargs['buyer']).first()
            if not order_buyer:
                raise Exception("No such buyer exists!")

            order_seller = Seller.objects(uid=kwargs['seller']).first()
            if not order_seller:
                raise Exception("No such seller exists")

            new_order = Order(offer_price=kwargs['offer_price'],item=order_item,buyer=order_buyer,seller=order_seller)
            new_order.save()
            new_order.uid = str(new_order.id)
            new_order.save()
            return True, new_order.uid
        except Exception as ex:
            return False, str(ex)

    def negotiate(self, offer):
        try:
            if offer < 0:
                raise Exception("Please enter a valid offer price")
            self.offer_price = offer
            return True, "Offer placed"

        except Exception as e:
            return False, str(e)


class Transaction(Document):
    uid = StringField()
    offer_price = FloatField(required = True, min_value=0)
    item_name = StringField(required=True, min_length=1)
    item_id = StringField(required=True,min_length=1)
    buyer_name = StringField(required=True,min_length=1)
    buyer_id = StringField(required=True,min_length=1)
    seller_name = StringField(required=True,min_length=1)
    seller_id = StringField(required=True,min_length=1)
    photo = ImageField(size=(300,300,True),required=True)
    category_name = StringField(required=True,min_length=1)
    category_id = StringField(required=True,min_length=1)

    @staticmethod
    def create_transaction(order_id):
        try:
            purchase_order = Order.objects(uid=order_id).first()

            if not purchase_order:
                raise Exception("No such order exists!")

            transaction = Transaction(offer_price=purchase_order.offer_price,item_name=purchase_order.item.name,
                                      item_id=purchase_order.item.uid,buyer_name=purchase_order.buyer.name,
                                      buyer_id=purchase_order.buyer.uid,seller_name=purchase_order.seller.name,
                                      seller_id=purchase_order.seller.uid,photo=purchase_order.item.photo,
                                      category_name=purchase_order.item.category.name,category_id=purchase_order.item.category.uid)
            transaction.save()
            transaction.uid = str(transaction.id)
            transaction.save()
            return True, transaction.uid
        except Exception as ex:
            return False, str(ex)
