import constants as co


def atom_mean_over_time(n):
    return co.TINF_SPAWN + (co.T0_SPAWN - co.TINF_SPAWN) / (1 + 0.08 * n)

def weights_over_time(n):
    if n < co.ONLY_HYDROGEN:
        return [1, 0, 0, 0]
    if n < co.ONLY_OXYGEN:
        return [0.4, 0.6, 0, 0]
    if n < co.ONLY_NITROGEN:
        return [0.33, 0.33, 0.34, 0]
    return [0.35, 0.25, 0.22, 0.18]
