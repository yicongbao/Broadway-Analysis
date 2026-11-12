import statsmodels.formula.api as smf

def formula(p):
    return 'log_gross ~ log_seats + Adapted + Revival + C(Year) + C(Music_Style) + '+' + '.join(c for c in p if c.startswith('Plot_'))
def fit(p):
    return smf.ols(formula(p),p).fit(cov_type='HC3')
def samples(p):
    return {'Full sample':p,'Without Hamilton':p[p.Show!='Hamilton'],'Without top 5%':p[p.Avg_Gross_USD<=p.Avg_Gross_USD.quantile(.95)],'At least 20 weeks':p[p.Observed_Weeks>=20]}
