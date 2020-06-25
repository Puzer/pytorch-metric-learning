#! /usr/bin/env python3

import torch

from .generic_pair_loss import GenericPairLoss
from ..utils import common_functions as c_f, loss_and_miner_utils as lmu
from ..distances import CosineSimilarity

class MultiSimilarityLoss(GenericPairLoss):
    """
    modified from https://github.com/MalongTech/research-ms-loss/
    Args:
        alpha: The exponential weight for positive pairs
        beta: The exponential weight for negative pairs
        base: The shift in the exponent applied to both positive and negative pairs
    """
    def __init__(self, alpha, beta, base=0.5, **kwargs):
        super().__init__(mat_based_loss=True, **kwargs)
        self.alpha = alpha
        self.beta = beta
        self.base = base

    def _compute_loss(self, mat, pos_mask, neg_mask):
        pos_exp = self.distance.pos_neg_margin(self.base, mat)
        neg_exp = self.distance.pos_neg_margin(mat, self.base)
        pos_loss = (1.0/self.alpha) * lmu.logsumexp(self.alpha * pos_exp, keep_mask=pos_mask, add_one=True)
        neg_loss = (1.0/self.beta) * lmu.logsumexp(self.beta * neg_exp, keep_mask=neg_mask, add_one=True)
        return {"loss": {"losses": pos_loss + neg_loss, "indices": c_f.torch_arange_from_size(mat), "reduction_type": "element"}}

    def get_default_distance(self):
        return CosineSimilarity()