from app import app
import mongoengine as ming
from osp.classes.address import Address

if __name__ == "__main__":

    obj = Address(residence_number="a@b", street="str", locality="loc",
                 state="state", city="city")
    print(obj.pincode)

    app.run(debug = True,port = 8000)