__author__ = 'taen'
 
import sys
import lxml.etree as etree
import logging
 
from product_definitions import FuturePFDefinition, FutureDefinition
from product_definitions import OptionDefinition,OptionSeriesDefinition, OptionOnFuturePFDefinition
from combined_commodity_definition import CombinedCommodityDefinition
from cme_span_parameters import *
 
def parse_rate(rate_tag, container):
    rate = Rate()
    rate.id = int(rate_tag.find("r").text)
    rate.rate = float(rate_tag.find("val").text)
    pm_rate = rate_tag.find("pmRate")
    if len(pm_rate):
        rate.per_month_rate = float(pm_rate.text)
 
    ps_rate = rate_tag.find("psRate")
    if len(ps_rate):
        rate.per_spread_rate = float(ps_rate.text)
 
    container[rate.id] = rate
 
def parse_scan_rates(scan_rate, container):
    scn_rate = ScanRate()
    scn_rate.id = int(scan_rate.find("r").text)
    scn_rate.price_scan = float(scan_rate.find("priceScan").text)
    scn_rate.vol_scan = float(scan_rate.find("volScan").text)
    container[scn_rate.id] = scn_rate
 
def parse_tier(tier_tag, container):
 
    tier_num = int(tier_tag.find("tn").text)
    start_date = tier_tag.find("sPe")
    end_date = tier_tag.find("ePe")
    start_date = start_date.text if len(start_date) else None
    end_date = end_date.text if len(end_date) else None
        
    tier = SpreadTier(tier_num, start_date=start_date, end_date=end_date)
       
    scan_rates = tier_tag.findall("scanRate")
    if len(scan_rates):
        for scan_rate in scan_rates:
            parse_scan_rates(scan_rate, tier.scan_rates)
 
    rates = tier_tag.findall("rate")
    if len(rates):
        for rate in rates:
            parse_rate(rate, tier.rates)
 
    container[tier_num] = tier
 
def parse_delta_spread(delta_tag, container):
 
    delta_spread = DeltaSpreadDefinition()
    delta_spread.priority_number = int(delta_tag.find("spread").text)
    delta_spread.charge_method = delta_tag.find("charge_method").text
   
    # parse tier legs
    rates = delta_tag.findall("rate")
    if len(rates):
        for rate in rates:
            parse_rate(rate, delta_spread.rates)
 
    pmps_rates = delta_tag.findall("pmpsRate")    
    if len(pmps_rates):
        for rate in pmps_rates:
            parse_rate(rate, delta_spread.pmps_rates)
 
    tlegs = delta_tag.findall("tLeg")
    if len(tlegs):
        for tleg in tlegs:
            tier_leg = TierSpreadLeg()
            tier_leg.cc = tleg.find("cc").text
            tier_leg.tier_number = int(tleg.find("tn").text)
            tier_leg.relative_side = tleg.find("rs").text
            tier_leg.delta_spread_ratio = int(tleg.find("i").text)
            rates = tleg.findall("rate")
            if len(rates):
                for rate in rates:
                    parse_rate(rate, tier_leg.rates)
 
            delta_spread.tier_legs.append(tier_leg)  
             
    plegs = delta_tag.findall("pLeg")
    if len(plegs):
        for pleg in plegs:
            period_leg = PeriodSpreadLeg()
            period_leg.cc = pleg.find("cc").text
            period_leg.period_code = int(pleg.find("pe").text)
            period_leg.relative_side = pleg.find("rs").text
            period_leg.delta_spread_ratio = int(pleg.find("i").text)
            rates = pleg.findall("rate")
            if len(rates):
                for rate in rates:
                    parse_rate(rate, period_leg.rates)
 
            delta_spread.period_legs.append(period_leg)
 
    rplegs = delta_tag.findall("rpLeg") 
    if len(rplegs):
        for rpleg in rplegs:
            rperiod_leg = RelativePeriodSpreadLeg()
            rperiod_leg.cc = pleg.find("cc").text
            rperiod_leg.relative_period_number = int(pleg.find("rpNum").text)
            rperiod_leg.relative_side = pleg.find("rs").text
            rperiod_leg.delta_spread_ratio = int(pleg.find("i").text)
            rperiod_leg.begin_tier_number = int(pleg.find("btNum").text)
            rperiod_leg.end_tier_number = int(pleg.find("etNum").text)
 
            rates = pleg.findall("rate")
            if len(rates):
                for rate in rates:
                    parse_rate(rate, rperiod_leg.rates)
 
            delta_spread.relative_period_legs.append(rperiod_leg)
 
    # recursive delta spread definition
    delta_spreads = delta_tag.findall("dSpread")
    if len(delta_spreads):
        for d_spread in delta_spreads:
            parse_delta_spread(d_spread, delta_spread.delta_spreads)
 
def parse_scan_definition(spread, param_set):
    spd = ScanningSpreadDefinition()
 
def parse_combined_commodity_tag(cc_tag, param_set):
 
    ccdef = CombinedCommodityDefinition()
    ccdef.code = cc_tag.find("cc").text
    ccdef.name = cc_tag.find("Name").text
    ccdef.currency = cc_tag.find("currency").text
  
    ccdef.wfpr_method = cc_tag.find("wfprMeth").text
    ccdef.spot_method = cc_tag.find("spotMeth").text
    ccdef.proc_method = cc_tag.find("procMeth").text
    ccdef.som_method = cc_tag.find("somMeth").text
 
    # parse pf links to add associated product family information
    pf_links = cc_tag.findall("pfLink")
    if len(pf_links):
        for pf_link in pf_links:
            pf = ProductFamilyLink()
            pf.exchange = pf_link.find("exch").text
            pf.pfid = int(pf_link.find("pfID").text)
            pf.scalar = float(pf_link.find("sc").text)
 
            # look up the definition by id and exchange
            pf.definition = param_set.exchange_product_families[pf.exchange][pf.pfid]
 
            ccdef.product_links.append(pf)
 
    def parse_tiers(tag, container):
        tier = cc_tag.find(tag)
        tiers = tier.findall("tier")
        if len(tiers):
            for tier_tag in tiers:
                parse_tier(tier_tag, container)
 
    parse_tiers("interTiers", ccdef.inter_tiers)
    parse_tiers("intraTiers", ccdef.intra_tiers)
    parse_tiers("rateTiers", ccdef.rate_tiers)
    parse_tiers("scanTiers", ccdef.scan_tiers)
    parse_tiers("somTiers", ccdef.som_tiers)
 
    # parse delta spreads
    delta_spreads = cc_tag.findall("dSpread")
    if len(delta_spreads):
        for d_spread in delta_spreads:
            parse_delta_spread(d_spread, ccdef.intra_delta_spreads)
 
    param_set.combined_commodities[ccdef.code] = ccdef
 
def parse_risk_array_tag(contract, tag):
    """ add risk arrays and tiers """
    risk_arrays = tag.findall("ra")
    for risk_array in risk_arrays:
        risk = RiskArray()
        risk.id = int(risk_array.find("r").text)
        sens = risk_array.findall("a")
 
        for val in sens:
            risk.risks.append(float(val.text))
        risk.delta = float(risk_array.find("d").text)
 
        contract.risk_arrays[risk.id] = risk
 

def parse_future_pf_tag(futpf):
    """
       Parses one Future Product Family tag for a specific exchange.
    """
    future_def = FuturePFDefinition()
    future_def.id = int(futpf.find("pfId").text)
    future_def.code = futpf.find("pfCode").text
    future_def.currency = futpf.find("currency").text
    future_def.name = futpf.find("name").text
 
    # handle contracts
    for fut in futpf.findall("fut"):
        # lookup is by settlement date...
        contract = FutureDefinition()
        contract.period_expiry = fut.find("pe").text
        fut_settdate = fut.find("setlDate")
           
        if len(fut_settdate):
            contract.expiry = fut_settdate.text # parse this
 
        """ add risk arrays and tiers """
        parse_risk_array_tag(contract, fut)
        if contract.expiry:
            future_def.contracts[contract.expiry] = contract
 
    return future_def
 
def parse_oof_pf_tag(oofpf):
 
    option_def = OptionOnFuturePFDefinition()
    option_def.id = int(oofpf.find("pfId").text)
    option_def.code = oofpf.find("pfCode").text
    option_def.currency = oofpf.find("currency").text
    option_def.exercise = oofpf.find("exercise").text
 
    # handle option series
    for series in oofpf.findall("series"):
        # lookup is by expiry...
        option_series = OptionSeriesDefinition()
        option_series.expiry = oofpf.find("setlDate").text # parse this
        option_series.scale_factor = float(oofpf.find("sc").text)
 
        # parse the scan rate
        for scan_rate in series.findall("scanRate"):
            scn_rate = ScanRate()
            scn_rate.id = int(scan_rate.find("r").text)
            scn_rate.price_scan = float(scan_rate.find("priceScan").text)
            scn_rate.vol_scan = float(scan_rate.find("volScan").text)
            option_series.scan_rates[scn_rate.id] = scn_rate
 
        for option in series.findall("opt"):
            # parse the individual option contracts
            opt = OptionDefinition()
            opt.strike = float(option.find("k").text)
 
            try:
                opt.price = float(option.find("p").text)
            except:
                pass
 
            opt.put_call = option.find("o").text
 
            #add risk arrays and tiers
            parse_risk_array_tag(opt, oofpf)
            option_series[(opt.strike, opt.put_call)] = opt
 
        option_def.series[option_series.expiry] = option_series
 
    return option_def
 
 
product_family_types = {"futPf":parse_future_pf_tag,
                        "oofPf":parse_oof_pf_tag
                       }
 
def parse_exchange_file(filename):
    root = etree.parse(filename)
 
    # do we need any of the exchange info?  maybe to make it easier position-wise?
    # for now lets keep a dict per exchange as this will be queried from the combined commodity
    exchange_code = root.find("exch").text
 
    exchange_dict = dict()
    for key, func in product_family_types.items():
        tags = root.findall(key)
        for tag in tags:
            definition = func(tag)
            exchange_dict[definition.id] = definition
 
    return exchange_code, exchange_dict
 
def parse_risk_files(mainfilename):
 
    # this file should have been preprocessed into a file containing everything
    # except the exchange data, which will be broken out by exchange
 
    # We will parse the exchange files first, as they would be defined
    # before the combined commodities
 
    stub = mainfilename[:-12]
    stripped_file = stub + "stripped.xml"
 
    try:
        logging.info("Using stripped filename: {}".format(stripped_file))
        root = etree.parse(stripped_file)
    except Exception as err:
        logging.exception(err)
        # log exception here
        raise
 
    # create a parameter set for each point in time (usually we expect only one...?)
    point_elem = root.find("pointInTime")
 
    param_set = CMESPANParameterSet()
    param_set.date = point_elem.find('date').text
 
    clearings = point_elem.findall("clearingOrg")
    for elem in clearings:
        if elem.find("ec").text != "CME":
            continue
 
        # parse the spot rates for currency conversion
        spot_rates = elem.findall("curConv")
        for spot_rate in spot_rates:
            ccy_def = SpotRateDefinition(to_currency=spot_rate.find("toCur").text,
                                         from_currency=spot_rate.find("fromCur").text,
                                         rate=float(spot_rate.find("factor").text))
 
            param_set.spot_rates[ccy_def.from_ccy + "_" + ccy_def.to_ccy] = ccy_def
 
 
        exchanges = ["CME","CBT","CMD","CMX","NYM"]
        for exch in exchanges:
           try:
                filename = "{}{}.xml".format(stub, exch)
                exchange, exch_dict = parse_exchange_file(filename)
                param_set.exchange_product_families[exchange] = exch_dict
           except Exception as err:
               logging.error("Failed to parse exchange file for {}!".format(exch))
               logging.exception(err)
 
        # parse the combined commodity definitions
        for cc_def in elem.findall("ccDef"):
            parse_combined_commodity_tag(cc_def, param_set)
 
        inter_spreads = elem.find("interSpreads")
        if len(inter_spreads):
            s_spreads = elem.findall("sSpread")
            for spread in s_spreads:
                parse_scan_definition(spread, param_set)
 
 
  
    # add additional parsing of super spreads etc
    return param_set
 
 
 
if __name__ == "__main__":
    try:
        positions = parse_risk_files(r'D:\Work\CME\cme.20150824.c.cust.c21.xml')
    except Exception as err:
        logging.exception(err)
    pass
 