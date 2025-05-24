import math

from model_objects import ProductQuantity, SpecialOfferType, Discount


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    # incrementing cart product by 1
    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):        
         return self._product_quantities
    
    # incrementing cart product by x quantity
    def add_item_quantity(self, product, quantity):
        """
    update product quantites in the cart.

    Args:
        product (Product): The product obj to be added that has a name and a unit .
        quantity (float): The quantity of the product to be added.

    Returns:
        None: The function does not return anything.
        """
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity


    def handle_offers(self, receipt, offers, catalog):
        # this block need to be refactored using much neater match case block or more organised If-Elif-Else block
        # i think it is poorly written and needs to be refactored
        try:
            discount = None                
            for p in self._product_quantities.keys():
                quantity = self._product_quantities[p]
                #breakpoint()
                if p in offers.keys():
                    offer = offers[p]
                    unit_price = catalog.unit_price(p)
                    quantity_as_int = int(quantity)
                    
                    x = 1
                    if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                        x = 3

                    elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                        x = 2
                        if quantity_as_int >= 2:
                            total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
                            discount_n = unit_price * quantity - total
                            discount = Discount(p, "2 for " + str(offer.argument), -discount_n)

                    if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                        x = 5

                    number_of_x = math.floor(quantity_as_int / x)
                    if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                        discount_amount = quantity * unit_price - (
                                    (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                        discount = Discount(p, "3 for 2", -discount_amount)

                    if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                        discount = Discount(p, str(offer.argument) + "% off",
                                            -quantity * unit_price * offer.argument / 100.0)

                    if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                        discount_total = unit_price * quantity - (
                                    offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
                        discount = Discount(p, str(x) + " for " + str(offer.argument), -discount_total)
                    #breakpoint()                    
                    if discount:
                        receipt.add_discount(discount)
                    
        except Exception as e:
            print(f"Error handling offers: {e}")
