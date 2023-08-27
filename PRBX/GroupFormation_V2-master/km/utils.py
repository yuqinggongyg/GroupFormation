from scipy import stats

def km_normed_characts(characts):
    return stats.zscore(characts)
