import json
from decimal import Decimal

class Customer_Encoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Decimal):
            return float(object)
    
        return json.JSONEncoder.default(self, object)