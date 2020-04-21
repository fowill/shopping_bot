# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class ProductDetails:
    def __init__(
        use,
        cost: str = None,
        brand: str = None,
        looking: str = None,
        unsupported_things=None,
    ):
        if unsupported_things is None:
            unsupported_things = []
        self.use = use
        self.cost = cost
        self.brand = brand
        self.looking = looking
