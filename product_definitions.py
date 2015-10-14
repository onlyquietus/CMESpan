

class RiskArray(object):
    # Represents one risk array instance
    def __init__(self):
        self.id = None  # rate id
        self.delta = None # tomorrows composite delta
        self.risks = list()

class ScanRate(object):

    def __init__(self):
        self.id = None
        self.price_scan = None
        self.vol_scan = None

class ProductFamilyDefinition(object):

    def __init__(self):
        self.id = None
        self.pf_type = None
        self.code = None
        self.currency = None

class FutureDefinition(object):

    def __init__(self):
        self.price = None
        self.risk_arrays = dict()

class FuturePFDefinition(ProductFamilyDefinition):

    def __init__(self):
        super().__init__()
        self.contracts = dict()  # lookup by settlement date

    def get_contract(self, expiry):
        if expiry not in self.contracts:
            raise KeyError("{} does not exist in Future Product Family: {}".format(expiry, self.code))


class OptionDefinition(object):

    def __init__(self):

        self.put_call = None
        self.strike = None
        self.price = None

        self.risk_arrays = dict() # lookup is by rate id


class OptionSeriesDefinition(object):
    # contains all the options where all params are the same except put/call code and strike
    def __init__(self):
        self.base_vol = None
        self.options = dict()   # lookup is by strike and put/call code
        self.scan_rates = dict()

    def get_option_def(self, put_call, strike):
        if (strike, put_call) not in self.options:
            raise KeyError("Option of {} and {} does not exist in series!".format(strike, put_call))

        return self.options[(strike, put_call)]

class OptionOnFuturePFDefinition(ProductFamilyDefinition):

    def __init__(self):
        super().__init__()
        self.cvf = None
        self.exercise = None # American or European

        self.series = dict()   #lookup is by expiry

    def get_series(self, expiry):
        if expiry not in self.series:
            raise KeyError("Option Series for {} does not exist in Option on Future Product Family: {}".format(expiry, self.code))

        return self.series[expiry]



