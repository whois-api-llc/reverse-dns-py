class Fields:
    domain = 'domain'
    value = 'value'

    @staticmethod
    def keys() -> list:
        return list(
            filter(lambda x: not x.startswith('_'), Fields.__dict__)
        )

    @staticmethod
    def values() -> list:
        return [Fields.__dict__[k] for k in Fields.keys()]
