def calculate_price(base, competitor, occupancy, aggressiveness):
    delta = competitor - base
    faktor = 1 + (delta / base * aggressiveness)
    return round(base * faktor, 2)