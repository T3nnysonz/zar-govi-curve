def getBounds(min_rate, max_rate, min_df, max_df): 
    bounds = {
        'min_rate': min_rate,     
        'max_rate': max_rate,    
        'min_df': min_df,      
        'max_df': max_df,       
    }
    return bounds;

def getConventions(day_count, coupon_frequency, interpolation_method, face_value, accrued_method):
    conventions = {
        'day_count': day_count,
        'coupon_frequency': coupon_frequency,
        'interpolation_method': interpolation_method,
        'face_value': face_value,
        'accrued_method': accrued_method
    }
    return conventions;

def getInstrument(mature_date, rate, clean_price, settlement_date,type):
    inst = {
        "mature_date":mature_date,
        "rate":rate,
        "clean_price":clean_price,
        "settlement_date":settlement_date,
        "type":type
    }
    return inst;