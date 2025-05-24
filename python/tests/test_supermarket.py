import pytest

from model_objects import Product, SpecialOfferType, ProductUnit, Offer
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from catalog import SupermarketCatalog
from receipt import Receipt



@pytest.fixture
def setup_cart_TEN_PERCENT_DISCOUNT():
    cart = ShoppingCart()
    """Fixture to create a Cart instance with sample data"""
    # filling in catalog with dummy products
    catalog = FakeCatalog()
    # product object
    gum = Product("gum", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)

    catalog.add_product(gum, 2.0)
    catalog.add_product(apples, 2)  

    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(gum, 2)

    offers = {}
    offers[gum] = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, gum, 10.0)
    offers[apples] = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0) 
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, gum, 10.0)   
    receipt = teller.checks_out_articles_from(cart)
    
    receipt.add_discount(-1.00)  
    return receipt    

@pytest.fixture
def setup_cart_FIVE_FOR_AMOUNT():
    cart = ShoppingCart()
    """Fixture to create a Cart instance with sample data"""
    # filling in catalog with dummy products
    catalog = FakeCatalog()
    # product object
    gum = Product("gum", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)

    catalog.add_product(gum, 2.0)
    catalog.add_product(apples, 2)  

    cart.add_item_quantity(apples, 5)
    cart.add_item_quantity(gum, 5)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, apples, 10.0) 
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, gum, 10.0)   
    
    receipt = teller.checks_out_articles_from(cart)
    offers = {}
    # filling in offers with dummy products
    offers[gum] = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, gum, 10.0)
    offers[apples] = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)
    receipt.add_discount(-1.00)  
    return receipt    

@pytest.fixture
def setup_cart_THREE_FOR_TWO():
    cart = ShoppingCart()
    """Fixture to create a Cart instance with sample data"""
    # filling in catalog with dummy products
    catalog = FakeCatalog()
    # product object
    gum = Product("gum", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)

    catalog.add_product(gum, 2.0)
    catalog.add_product(apples, 2)  

    cart.add_item_quantity(apples, 3)
    cart.add_item_quantity(gum, 3)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, apples, 10.0) 
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, gum, 10.0)   
    
    receipt = teller.checks_out_articles_from(cart)
    offers = {}
    # filling in offers with dummy products
    offers[gum] = Offer(SpecialOfferType.THREE_FOR_TWO, gum, 10.0)
    offers[apples] = Offer(SpecialOfferType.THREE_FOR_TWO, apples, 10.0)
    receipt.add_discount(-1.00)  
    return receipt    

@pytest.fixture
def setup_cart_TWO_FOR_AMOUNT():
    cart = ShoppingCart()
    """Fixture to create a Cart instance with sample data"""
    # filling in catalog with dummy products
    catalog = FakeCatalog()
    # product object
    gum = Product("gum", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)

    catalog.add_product(gum, 2.0)
    catalog.add_product(apples, 2)  

    cart.add_item_quantity(apples, 2.5)
    cart.add_item_quantity(gum, 2)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, apples, 10.0) 
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, gum, 10.0)   
    
    receipt = teller.checks_out_articles_from(cart)
    offers = {}
    # filling in offers with dummy products
    offers[gum] = Offer(SpecialOfferType.TWO_FOR_AMOUNT, gum, 10.0)
    offers[apples] = Offer(SpecialOfferType.TWO_FOR_AMOUNT, apples, 10.0)
    receipt.add_discount(-1.00)  
    return receipt
    
    """
    Test discount application
    it needs to cover all offer cases which are 
    FIVE_FOR_AMOUNT
    TEN_PERCENT_DISCOUNT
    THREE_FOR_TWO
    TWO_FOR_AMOUNT
    """

def test_handle_offers_TEN_PERCENT_DISCOUNT(setup_cart_TEN_PERCENT_DISCOUNT):        
    receipt = setup_cart_TEN_PERCENT_DISCOUNT
    assert receipt.discounts[0] == -1.00
    assert receipt.discounts[0].description == "10% off"
    assert receipt.discounts[0].amount == -0.20  # 10% off on total
    

def test_handle_offers_THREE_FOR_TWO(setup_cart_THREE_FOR_TWO):
    receipt = setup_cart_THREE_FOR_TWO
    assert receipt.discounts[0] == -1.00
    assert receipt.discounts[0].description == "3 for 2" 
    assert receipt.discounts[0].amount == -2.00  # Discount applied


def test_handle_offers_TWO_FOR_AMOUNT(setup_cart_TWO_FOR_AMOUNT):
    receipt = setup_cart_TWO_FOR_AMOUNT
    assert receipt.discounts[0] == -1.00
    assert receipt.discounts[0].description == "2 for 1.50"
    assert receipt.discounts[0].amount == -0.50  # Discount applied

def test_handle_offers_FIVE_FOR_AMOUNT(setup_cart_FIVE_FOR_AMOUNT):
    receipt = setup_cart_FIVE_FOR_AMOUNT
    assert receipt.discounts[0] == -1.00
    assert receipt.discounts[0].description == "5 for 4.00"
    assert receipt.discounts[0].amount == -1.00  # Discount applied


# def test_add_item(setup_cart):
#     cart, catalog, product, receipt, offers = setup_cart
#     cart.add_item(Product("apples", ProductUnit.EACH))
#     assert cart.items[0].product.name == "apples"
#     assert cart.product_quantities['apples'] == 1.0    


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity


