__author__ = 'taen'
 
from collections import OrderedDict
 
class CMESPANParameterSet(object):
    """
    """
    date = None
    settlement = None
    scenario_count = 16
 
    # we will only represent one clearing house in this structure
    def __init__(self):
       self.spot_rates = dict()
       self.exchange_product_families = dict()  # dict of dicts
       self.combined_commodities = dict()
       self.super_spreads = dict()
       self.margin_currency = "USD" # default for testing
       self.inter_spreads = OrderedDict()
 
    def get_spot_rate(self, from_currency, to_currency):
        key = from_currency + "_" + to_currency
 
        if key not in self.spot_rates:
            raise Exception("Spot rate for currency pair {0}{1} does not exist!".format(from_currency, to_currency))
 
        return self.spot_rates[key].rate
 
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
 
class Rate(object):
 
    def __init__(self):
        self.id = None
        self.rate = None
        self.per_month_rate = None
        self.per_spread_rate = None
 
class SpreadTier(object):
 
    def __init__(self, tier_index, start_date=None, end_date=None):
        self.tier = tier_index
        self.end_date = end_date
        self.start_date = start_date
 
        self.rates = dict()
        self.scan_rates = dict()
 
class SpotRateDefinition(object):
 
    def __init__(self, to_currency=None, from_currency=None, rate = 0.0):
        """ Holds the spot rate for one currency pair"""
        self.to_ccy = to_currency
        self.from_ccy = from_currency
   
        self.rate = rate
 
class TierSpreadLeg(object):
 
    cc = None
    relative_side = None
    delta_spread_ratio = None
    tier_number = None
 
    def __init__(self):
        self.rates = dict()
 
class PeriodSpreadLeg(object):
 
    cc = None
    relative_period_number = None
 
    period_code = None
    relative_side = None
    delta_spread_ratio = None
 
    def __init__(self):
        self.rates = dict()
 
class RelativePeriodSpreadLeg(object):
 
    cc = None
    relative_side = None
    delta_spread_ratio = None
    begin_tier_number = None
    end_tier_number = None
 
    def __init__(self):
        self.rates = dict()
 
class DeltaSpreadDefinition(object):
    """ Represe"""
    priority_number = None
    charge_method = None
    tier_legs = None
 
    delta_spreads = None
 
    def __init__(self):
        self.tier_legs = list()
        self.period_legs = list()
        self.relative_period_legs = list()
 
        self.rates = dict()
        self.pmps_rates = dict()
        self.delta_spreads = dict()

class ScanSpreadLeg(object):
 
    cc = None
    delta_spread_ratio = None
    tier_number = None
 
    def __init__(self):
        self.is_target = False
        self.is_required = False
        self.rates = dict()
 
class ScanningSpreadDefinition(object):
    """ Represe"""
    priority_number = None
    apply_fx_risk = None
    apportion_risk = None
    def __init__(self):
        self.spread_legs = list()
        self.num_legs_required = 2
        self.is_target = False
       
        self.spread_rates = dict()
       