__author__ = 'taen'

# We need to record the positions at the combined commodity level in order to properly
# compute the scanning risk and intra/inter-commodity spreads for the combined Commodity

# should we hold our own definition, or look it up?  I think look it up for a given set of risk parameters
# as they can be published multiple times in a day


class Position(object):

    underlying_type = None

    def __init__(self):
        self.code = None
        self.position = None
        self.position_valuation = None # do we need this?
        # we shouldnt need the multiplier from the position file as it will be included in the
        # product definition..
        # do we need the exchange this position is traded on?

        self.trade_date = None
        self.currency = None
        self.expiry_year = None
        self.expiry_month = None  # we wont use this as it may come in in french... urgh
        self.expiry = None

    def calculate_scanning_risk(self, risk_params):
        pos_def = risk_params.get_product_definition(self.code)


class FuturePosition(Position):

    def __init__(self):
        super().__init__()

    def calculate_scanning_risk(self, risk_params):
        pf_def = risk_params.get_pf_definition(self.code)

        # we want the future definition for our expiry date - the settlement date of this
        # future contract.

class OptionPosition(Position):

    def __init__(self):
        super().__init__()

        self.option_type = None # American or European
        self.strike = None
        self.call_put = None # Call or Put

    def calculate_position_array(self, risk_params):
        pf_def = risk_params.get_product_definition(self.code)



class CombinedCommodityPosition(object):

    def __init__(self):
        self.positions = list()
        self.cc_code = None # required to look up combined commodity definition

        # SEH:  should we keep a list of the short option positions in addition to the main
        #       list? worry about it later!

    def calculate_scanning_risk(self, risk_params):

        # get the combined commodity definition for this cc position from the risk param object
        cc_def = risk_params.get_combined_commodity_definition(self.cc_code)

        total_portfolio_risk = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for position in self.positions:
            position.calculate_position_arra

        #


