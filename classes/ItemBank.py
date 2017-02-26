class ItemBank(object):
    def __init__(self, properties):
        self.prior_alpha = properties['MinNumItems']
        self.prior_beta = 1
        self.min_items = 1
        self.max_items = 1
        self.min_error = 1
        self.item = ItemBank.Item(1)

    class Item(object):
        def __init__(self, properties):
            self.code = 1
            self.context = 1
            self.prompt = 1
            self.brief = 1
            self.alpha = 1
            self.betas = 1
            self.strata = 1
            self.category = 1
            self.response = ItemBank.Item.Responses(1)

        class Responses(object):
            def __init__(self, properties):
                self.text = 1
                self.difficulty = 1


