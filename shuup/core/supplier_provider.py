# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from shuup.core.models import Shop, Supplier
from shuup.core.utils.shops import get_shop_from_host
from shuup.utils.importing import cached_load


class DefaultSupplierProvider(object):
    @classmethod
    def get_supplier(cls, request, **kwargs):
        shop = None

        host = request.META.get("HTTP_HOST")
        if host:
            shop = get_shop_from_host(host)

        if not shop:
            shop = Shop.objects.first()

        return Supplier.objects.filter(shops=shop).first()


def get_supplier(shop, **kwargs):
    return cached_load("SHUUP_REQUEST_SUPPLIER_PROVIDER_SPEC").get_supplier(shop, **kwargs)
