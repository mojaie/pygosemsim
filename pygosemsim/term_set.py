

def sim_func(G, sim_method, term1, term2):
    try:
        sim = sim_method(G, term1, term2)
    except ValueError:
        sim = 0
    if sim is None:
        sim = 0
    return sim


def sim_max(terms1, terms2, sem_sim):
    """Similarity score between two term sets based on maximum value
    """
    sims = []
    for t1 in terms1:
        for t2 in terms2:
            sim = sem_sim(t1, t2)
            sims.append(sim)
    return round(max(sims), 3)


def sim_avg(terms1, terms2, sem_sim):
    """Similarity between two term sets based on average
    """
    sims = []
    for t1 in terms1:
        for t2 in terms2:
            sim = sem_sim(t1, t2)
            sims.append(sim)
    return round(sum(sims) / (len(terms1) * len(terms2)), 3)


def sim_bma(terms1, terms2, sem_sim):
    """Similarity between two term sets based on Best-Match Average (BMA)
    """
    sims = []
    for t1 in terms1:
        row = []
        for t2 in terms2:
            sim = sem_sim(t1, t2)
            row.append(sim)
        sims.append(max(row))
    for t2 in terms2:
        row = []
        for t1 in terms1:
            sim = sem_sim(t1, t2)
            row.append(sim)
        sims.append(max(row))
    return round(sum(sims) / (len(terms1) + len(terms2)), 3)
