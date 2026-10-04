
class Product : 
    def __init__(self , ID , name , price , stock , category) :
        self.ID = ID
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category 

    def search_product(self , name) :
        return name.lower() in self.name.lower()  
        
    def add_stock(self , quantity) :
        self.stock += quantity

    def remove_stock(self , quantity) :
        if self.stock >= quantity :
            self.stock -= quantity
            return True
        else :
            return False 
               
    def get_stock_status(self) :
        if self.stock == 0 :
            return "Out of Stock"
        elif self.stock <= 5 :
            return "Low Stock"
        else :
            return ""    

class CartItem :
    def __init__(self , product , quantity) :
        self.product = product
        self.quantity = quantity

    def get_Subtotal(self) :
        return self.product.price * self.quantity
    
    def increase_quantity(self , quantity) :
        self.quantity += quantity

    def decrease_quantity(self , quantity) :
        if self.quantity >= quantity :
            self.quantity -= quantity
            return True
        else :
            return False

class Cart :
    def __init__(self) :
        self.items = []

    def add_item(self , product , quantity) :
        for item in self.items :
            if item.product.ID == product.ID :
                item.increase_quantity(quantity)
                product.remove_stock(quantity)
                return
        new_item = CartItem(product , quantity)
        self.items.append(new_item)
        product.remove_stock(quantity)    

    def remove_item(self , product_ID , quantity) :
        for item in self.items :
            if item.product.ID == product_ID :
                if item.decrease_quantity(quantity) :
                    item.product.add_stock(quantity)
                    if item.quantity == 0 :
                        self.items.remove(item)
                    return True
                else :
                    return False
        return False   
    
    def is_empty(self) :
        return len(self.items) == 0

    def calculate_subtotal(self) :
        subtotal = 0
        for item in self.items :
            subtotal += item.get_Subtotal()
        return subtotal

    def clear_cart(self) :
        self.items.clear()    

class Coupon :
    coupons = { 
        "CAFE10" : 0.1 ,
        "STUDENT5" : 0.05 ,
        "WELCOME3" : 0.03 } 

    @classmethod 
    def get_discount(cls , coupon_code) :
        if coupon_code in cls.coupons :
            return cls.coupons[coupon_code] 
        return 0 
    @classmethod
    def is_valid(cls , coupon_code) :
        return coupon_code in cls.coupons

class Order :
    def __init__(self , order_number , cart ) :
        self.order_number = order_number
        self.items = [] 
        for item in cart.items :
            self.items.append(
                {
                    "product" : item.product ,
                    "quantity" : item.quantity ,
                    "subtotal" : item.get_Subtotal()
                } )
        self.subtotal = cart.calculate_subtotal()
        self.auto_discount = 0 
        self.coupon_discount = 0
        self.discounted_amoount = 0 
        self.service_charge = 0
        self.final_total = 0

        self.payment_method = ""
        self.received_amount = 0
        self.change = 0

    def calculate_auto_discount(self) :
        if self.subtotal < 300 :
            self.auto_discount = 0
        elif 300 <= self.subtotal < 500 :
            self.auto_discount = 0.05 
        else :
            self.auto_discount = 0.1

    def apply_coupon_discount(self , coupon_code) :
        self.coupon_discount = Coupon.get_discount(coupon_code)

    def calculate_final_total(self) :
        total_discount = min(self.auto_discount + self.coupon_discount , 0.15) 
        self.discounted_amoount = self.subtotal * total_discount
        price_after_discount = self.subtotal - self.discounted_amoount
        self.service_charge = price_after_discount * 0.05
        self.final_total = price_after_discount + self.service_charge

    def set_payment_method(self , payment_method) :
        self.payment_method = payment_method 

    def process_cash (self , received_amount) :
        self.received_amount = received_amount
        if self.received_amount >= self.final_total :
            self.change = self.received_amount - self.final_total
            return True
        else :
            return False

class CafeManagementSystem :
    def __init__(self) :
        self.products = []
        self.cart = Cart()
        self.completed_orders = []
        self.order_number = 1001 
        self.username = "admin"
        self.password = "cafe123" 
        self.create_products()

    def create_products(self) :
        self.products.append(Product(1 , "Espresso" , 45 , 20 ,  "coffee"))
        self.products.append(Product(2 , "Cappuccino" , 65 , 15 , "coffee"))    
        self.products.append(Product(3 , "Latte" , 70 , 15 , "coffee"))
        self.products.append(Product(4 , "Tea" , 30 , 25 , "Hot Drinks"))
        self.products.append(Product(5 , "orange Juice" , 55 , 12 , "Cold Drinks"))
        self.products.append(Product(6 , "Water" , 15 , 30 , "Cold Drinks"))
        self.products.append(Product(7 , "Croissant" , 50 , 10 , "Bakery"))
        self.products.append(Product(8 , "cheesecake" , 85 , 8 , "Desserts"))

    def login(self , username , password ) : 
        return username == self.username and password == self.password

    def find_product_by_ID(self , product_ID) :
        for product in self.products :
            if product.ID == product_ID :
                return product
        return None

    def complete_order(self , order) :
        self.completed_orders.append(order)
        self.cart.clear_cart()
        self.order_number += 1
 
    def get_report_data(self) :
        total_orders = len(self.completed_orders)
        total_sales = sum(order.final_total for order in self.completed_orders)
        sold = {}
        for order in self.completed_orders :
            for item in order.items :
                product = item["product"]
                sold[product] = sold.get(product , 0) + item["quantity"]
        return {
            "total_orders" : total_orders ,
            "total_sales" : total_sales ,
            "average" : total_sales / total_orders if total_orders else 0 ,
            "sold" : sold ,
            "low_stock" : [p for p in self.products if 0 < p.stock <= 5] ,
            "out_of_stock" : [p for p in self.products if p.stock == 0] ,
        }
 

   