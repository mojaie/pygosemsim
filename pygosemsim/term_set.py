
from pygosemsim import similarity


def max_sim(terms1, terms2, sem_sim=similarity.resnik):
    """Similarity score between two term sets based on maximum value
    """
    sims = []
    for t1 in terms1:
        for t2 in terms2:
            sim = sem_sim(t1, t2)
            sims.append(sim)
    return max(sims)


def avg_sim(terms1, terms2, sem_sim=similarity.resnik):
    """Similarity between two term sets based on average
    """
    sims = []
    for t1 in terms1:
        for t2 in terms2:
            sim = sem_sim(t1, t2)
            sims.append(sim)
    return sum(sims) / (len(terms1) * len(terms2))


def bma_sim(terms1, terms2, sem_sim=similarity.resnik):
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
    return sum(sims) / (len(terms1) + len(terms2))
