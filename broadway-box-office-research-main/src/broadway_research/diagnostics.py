import numpy as np

def inspect(f):
    x=f.model.exog
    return dict(rank=int(np.linalg.matrix_rank(x)),columns=x.shape[1],condition_number=float(np.linalg.cond(x)),max_leverage=float(f.get_influence().hat_matrix_diag.max()))
