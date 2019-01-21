import pytest

from shuup.core.models import ShopStatus, Shop, Product, ShopProduct
from shuup.core.utils.product import get_product_name
from shuup.testing.factories import get_default_supplier, create_product, get_default_sales_unit, get_default_tax_class, \
    get_default_product_type

"""
Refer to: https://github.com/shuup/shuup/issues/1275

There would be two kind of Products: shared products and shop specific products. This would be controlled by the flag that you proposed, e.g. named Product.is_shared.

Following limitations would apply for the SKUs:
[a] SKUs of shared products are unique within the Shuup installation.
[b] SKUs of shop specific products are unique within a shop and cannot conflict with the SKUs of the shared products.

A Shop Administrator (for a certain shop) could
[c] create and modify any shop specific products within the shop (including all Product and ShopProduct related details of them), and
[d] edit any shop specific details (stored in the ShopProduct part) of any shared product which already has a ShopProduct for the shop. Shared products which don't have ShopProduct for the shop would be invisible to the Shop Admininistrator except for the SKUs being unavailable.

A General Administrator (i.e. administrator of the whole Shuup installation and all of its shops) could
[e] do all the same things as Shop Administrators can and additionally
[f] create shared products from scratch or by converting existing shop specific products to shared products,
[g] unshare a shared product, i.e. convert it to a set of shop specific products, one for each previously existing ShopProduct, and
[h] manage sharing of the shared products to the shops by creating or deleting ShopProduct instances. See also [d].

"""
#
# CHOICES = [
#     # one shop stop
#     (None, "shop1", True, "shop1", False, 1, "product1"),
#     (None, "shop1", False, "shop1", False, 1, "product1"),
#     (True, "shop1", True, "shop1", False, 2, "product1"),
#     (True, "shop1", False, "shop1", True, 1, "product1"),
#     (False, "shop1", True, "shop1", False, 2, "product1"),
#     (False, "shop1", False, "shop1", True, 1, "product1"),
#
#     (None, "shop1", True, "shop2", False, 1, "product1"),
#     (None, "shop1", False, "shop2", False, 1, "product1"),
#     (True, "shop1", True, "shop2", False, 2, "product1"),
#     (True, "shop1", False, "shop2", True, 1, "product1"),
#     (False, "shop1", True, "shop2", False, 2, "product1"),
#     (False, "shop1", False, "shop2", True, 1, "product1"),
#
#     (None, "shop2", True, "shop1", False, 1, "product1"),
#     (None, "shop2", False, "shop1", False, 1, "product1"),
#     (True, "shop2", True, "shop1", False, 2, "product1"),
#     (True, "shop2", False, "shop1", True, 1, "product1"),
#     (False, "shop2", True, "shop1", False, 2, "product1"),
#     (False, "shop2", False, "shop1", True, 1, "product1"),
#
#     (None, "shop2", True, "shop2", False, 1, "product1"),
#     (None, "shop2", False, "shop2", False, 1, "product1"),
#     (True, "shop2", True, "shop2", False, 2, "product1"),
#     (True, "shop2", False, "shop2", True, 1, "product1"),
#     (False, "shop2", True, "shop2", False, 2, "product1"),
#     (False, "shop2", False, "shop2", True, 1, "product1"),
# ]
#
# @pytest.mark.parametrize("existing_product,existing_product_shop,new_product,new_product_shop,expected_error,sku_count,expected_name", CHOICES)
# @pytest.mark.django_db
# def test_product_sharing(rf, existing_product, existing_product_shop, new_product, new_product_shop, expected_error, sku_count, expected_name):
#     assert 1
#     # smoketest
#     Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
#     Shop.objects.create(identifier="shop2", status=ShopStatus.ENABLED, domain="shop2.shuup.com")
#
#     supplier = get_default_supplier()
#
#     existing_product_shop_object = Shop.objects.get(identifier=existing_product_shop)
#     new_product_shop_object = Shop.objects.get(identifier=new_product_shop)
#
#     sku = "test"
#     if existing_product is not None:
#         product = create_product(sku, existing_product_shop_object, supplier, is_shared=existing_product)
#         product.name = "product1"
#         product.save()
#         assert product.is_shared is existing_product
#
#     if expected_error:
#         with pytest.raises(ValueError):
#             # not allowed to create product with same sku.. yet
#             create_product(sku, new_product_shop_object, supplier, is_shared=new_product)
#     else:
#         product2 = create_product(sku, new_product_shop_object, supplier, is_shared=new_product)
#         product2.name = "product2"
#         product2.save()
#         assert get_product_name(product2, new_product_shop) == expected_name
#
#     assert Product.objects.filter(sku=sku).count() == sku_count



# @pytest.mark.django_db
# def test_product_sharing1(rf):
#     # https://github.com/shuup/shuup/issues/1275
#     # [a] SKUs of shared products are unique within the Shuup installation.
#
#     shop = Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
#     supplier = get_default_supplier()
#     sku = "test"
#
#     assert Product.objects.count() == 0
#     create_product(sku, shop, supplier, is_shared=True)
#
#     assert Product.objects.count() == 1
#     with pytest.raises(ValueError):
#         # not allowed to create product with same sku.. yet
#         create_product(sku, shop, supplier, is_shared=True)
#
#     assert Product.objects.count() == 1
#     assert Product.objects.filter(sku=sku).count() == 1
#
#
# @pytest.mark.django_db
# def test_product_sharing2(rf):
#     # https://github.com/shuup/shuup/issues/1275
#     # [b] SKUs of shop specific products are unique within a shop and cannot conflict with the SKUs of the shared products.
#     shop = Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
#     supplier = get_default_supplier()
#     sku = "test"
#
#     assert Product.objects.count() == 0
#     create_product(sku, shop, supplier, is_shared=False)
#
#     assert Product.objects.count() == 1
#     with pytest.raises(ValueError):
#         # not allowed to create product with same sku.. yet
#         create_product(sku, shop, supplier, is_shared=False)
#
#     assert Product.objects.count() == 2
#     assert Product.objects.filter(sku=sku).count() == 2
#     assert ShopProduct.objects.count() == 1
#
#
# @pytest.mark.django_db
# def test_product_sharing3(rf):
#     # https://github.com/shuup/shuup/issues/1275
#     # [b] SKUs of shop specific products are unique within a shop and cannot conflict with the SKUs of the shared products.
#     shop = Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
#     supplier = get_default_supplier()
#     sku = "test"
#
#     assert Product.objects.count() == 0
#     create_product(sku, shop, supplier, is_shared=True)
#
#     assert Product.objects.count() == 1
#     with pytest.raises(ValueError):
#         # not allowed to create product with same sku.. yet
#         create_product(sku, shop, supplier, is_shared=False)
#
#     assert Product.objects.count() == 2
#     assert Product.objects.filter(sku=sku).count() == 2
#     assert ShopProduct.objects.count() == 1


# @pytest.mark.django_db
# def test_product_sharing4(rf):
#     # https://github.com/shuup/shuup/issues/1275
#     # [b] SKUs of shop specific products are unique within a shop and cannot conflict with the SKUs of the shared products.
#     shop = Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
#     supplier = get_default_supplier()
#     sku = "test"
#
#     assert Product.objects.count() == 0
#     create_product(sku, shop, supplier, is_shared=False)
#
#     assert Product.objects.count() == 1
#     with pytest.raises(ValueError):
#         # not allowed to create product with same sku.. yet
#         create_product(sku, shop, supplier, is_shared=True)
#
#     assert Product.objects.count() == 2
#     assert Product.objects.filter(sku=sku).count() == 2
#     assert ShopProduct.objects.count() == 1


"""

Muutokset:
Product.sku => ei uniikki
Product.is_shared = boolean field (default False)

1) Luo tuote X, jolla on sku abc-123, tuote on shared
2) Luo tuote Y, jolla on sku abc-123, tuote on shared
    -> Product raise (koska shared ja sku on olemassa, tuomaksen A-kohta)

1) Luo tuote X, jolla on sku abc-123, tuote ei ole shared
2) Luo tuote Y, jolla on sku abc-123, tuote ei ole shared
    -> Product OK (ei shared, kauppa ei tiedossa, koska product)
    -> ShopProduct Raise (`if ShopProduct.objects.filter(product__sku=product.sku, shop=self.shop).exclude(pk=shop_product.pk).exists()`, tuomaksen B-kohta)
    -> kantaan tulee tuote ilman Shop Productia (Koska product on jo luotu)


```
@pytest.mark.django_db
def test_product_sharing2(rf):
    # https://github.com/shuup/shuup/issues/1275
    # [b] SKUs of shop specific products are unique within a shop and cannot conflict with the SKUs of the shared products.
    shop = Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
    supplier = get_default_supplier()
    sku = "test"

    assert Product.objects.count() == 0
    create_product(sku, shop, supplier, is_shared=False)

    assert Product.objects.count() == 1
    with pytest.raises(ValueError):
        # not allowed to create product with same sku.. yet
        create_product(sku, shop, supplier, is_shared=False)

    assert Product.objects.count() == 2
    assert Product.objects.filter(sku=sku).count() == 2
    assert ShopProduct.objects.count() == 1```

 
"""

# def test_product_name(rf):
#     assert 0


@pytest.mark.django_db
def test_product_creation1():
    shop = Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
    supplier = get_default_supplier()
    tax_class = get_default_tax_class()
    sales_unit = get_default_sales_unit()
    product_type = get_default_product_type()
    sku = "test"

    assert Product.objects.count() == 0

    product_name = "Testing Product"

    data = {
        "product_info": {
            "name": product_name
        },
        "shop_product": {
            "supplier": supplier
        },
        "shared": True
    }

    shop_product = ShopProduct.create_product(sku, shop, data)
    assert supplier in shop_product.suppliers.all()

    assert Product.objects.count() == 1

    product = shop_product.product

    assert product.tax_class == tax_class
    assert product.sales_unit == sales_unit
    assert product.type == product_type
    assert product.name == product_name

    with pytest.raises(ValueError) as exc_info:
        ShopProduct.create_product(sku, shop, data)
        assert exc_info != "Duplicate SKU", "#1275: [a] SKUs of shared products are unique within the Shuup installation."

    assert Product.objects.count() == 1
    assert Product.objects.filter(sku=sku).count() == 1
    assert ShopProduct.objects.count() == 1

    assert Product.objects.count() == 1
    data["shared"] = False
    with pytest.raises(ValueError) as exc_info:
        ShopProduct.create_product(sku, shop, data)
        assert exc_info == "Duplicate SKU's are not allowed inside one shop", "#1275: [b] SKUs of shop specific products are unique within a shop and cannot conflict with the SKUs of the shared products."

    assert Product.objects.count() == 1
    assert Product.objects.filter(sku=sku).count() == 1
    assert ShopProduct.objects.count() == 1


@pytest.mark.django_db
def test_product_creation2():
    shop = Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
    shop2 = Shop.objects.create(identifier="shop2", status=ShopStatus.ENABLED, domain="shop2.shuup.com")
    shop3 = Shop.objects.create(identifier="shop3", status=ShopStatus.ENABLED, domain="shop3.shuup.com")
    shop4 = Shop.objects.create(identifier="shop4", status=ShopStatus.ENABLED, domain="shop4.shuup.com")
    supplier = get_default_supplier()
    tax_class = get_default_tax_class()
    sales_unit = get_default_sales_unit()
    product_type = get_default_product_type()
    sku = "test"

    assert Product.objects.count() == 0

    product_name = "Testing Product"

    data = {
        "product_info": {
            "name": product_name
        },
        "shop_product": {
            "supplier": supplier
        },
        "shared": False
    }

    shop_product = ShopProduct.create_product(sku, shop, data)
    assert supplier in shop_product.suppliers.all()

    assert Product.objects.count() == 1

    product = shop_product.product

    assert product.tax_class == tax_class
    assert product.sales_unit == sales_unit
    assert product.type == product_type
    assert product.name == product_name

    # try to create to same shop, fails because duplicate
    with pytest.raises(ValueError) as exc_info:
        ShopProduct.create_product(sku, shop, data)
        assert exc_info == "Duplicate SKU's are not allowed inside one shop", "#1275: [b] SKUs of shop specific products are unique within a shop and cannot conflict with the SKUs of the shared products."

    assert Product.objects.count() == 1
    assert Product.objects.filter(sku=sku).count() == 1
    assert ShopProduct.objects.count() == 1
    assert Product.objects.count() == 1

    # creation works ok as this is different shop
    ShopProduct.create_product(sku, shop2, data)
    assert Product.objects.count() == 2
    assert Product.objects.filter(sku=sku).count() == 2
    assert ShopProduct.objects.count() == 2

    data["shared"] = True
    # creation works ok as this is different shop

    with pytest.raises(ValueError) as exc_info:
        ShopProduct.create_product(sku, shop3, data)
        assert exc_info != "Duplicate SKU", "#1275: [a] SKUs of shared products are unique within the Shuup installation."
    assert Product.objects.count() == 2
    assert Product.objects.filter(sku=sku).count() == 2
    assert ShopProduct.objects.count() == 2

    with pytest.raises(ValueError) as exc_info:
        ShopProduct.create_product(sku, shop4, data)
        assert exc_info != "Duplicate SKU", "#1275: [a] SKUs of shared products are unique within the Shuup installation."

    assert Product.objects.count() == 2
    assert Product.objects.filter(sku=sku).count() == 2
    assert ShopProduct.objects.count() == 2


@pytest.mark.django_db
def test_product_creation3():
    shop = Shop.objects.create(identifier="shop1", status=ShopStatus.ENABLED, domain="shop1.shuup.com")
    shop2 = Shop.objects.create(identifier="shop2", status=ShopStatus.ENABLED, domain="shop2.shuup.com")
    shop3 = Shop.objects.create(identifier="shop3", status=ShopStatus.ENABLED, domain="shop3.shuup.com")
    shop4 = Shop.objects.create(identifier="shop4", status=ShopStatus.ENABLED, domain="shop4.shuup.com")
    supplier = get_default_supplier()
    tax_class = get_default_tax_class()
    sales_unit = get_default_sales_unit()
    product_type = get_default_product_type()
    sku = "test"

    assert Product.objects.count() == 0

    product_name = "Testing Product"

    data = {
        "product_info": {
            "name": product_name
        },
        "shop_product": {
            "supplier": supplier
        },
        "shared": True
    }

    shop_product = ShopProduct.create_product(sku, shop, data)
    assert supplier in shop_product.suppliers.all()

    assert Product.objects.count() == 1

    product = shop_product.product

    assert product.tax_class == tax_class
    assert product.sales_unit == sales_unit
    assert product.type == product_type
    assert product.name == product_name

    with pytest.raises(ValueError) as exc_info:
        ShopProduct.create_product(sku, shop, data)
        assert exc_info != "Duplicate SKU", "#1275: [a] SKUs of shared products are unique within the Shuup installation."

    assert Product.objects.count() == 1
    assert Product.objects.filter(sku=sku).count() == 1
    assert ShopProduct.objects.count() == 1

    assert Product.objects.count() == 1
    with pytest.raises(ValueError) as exc_info:
        ShopProduct.create_product(sku, shop, data)
        assert exc_info == "Duplicate SKU's are not allowed inside one shop", "#1275: [b] SKUs of shop specific products are unique within a shop and cannot conflict with the SKUs of the shared products."

    assert Product.objects.count() == 1
    assert Product.objects.filter(sku=sku).count() == 1
    assert ShopProduct.objects.count() == 1

    ShopProduct.create_product(sku, shop2, data)
    assert Product.objects.count() == 2
    assert Product.objects.filter(sku=sku).count() == 2
    assert ShopProduct.objects.count() == 2

    ShopProduct.create_product(sku, shop3, data)
    assert Product.objects.count() == 3
    assert Product.objects.filter(sku=sku).count() == 3
    assert ShopProduct.objects.count() == 3

    ShopProduct.create_product(sku, shop4, data)
    assert Product.objects.count() == 4
    assert Product.objects.filter(sku=sku).count() == 4
    assert ShopProduct.objects.count() == 4
