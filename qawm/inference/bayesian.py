import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel

class ProbabilisticState(BaseModel):
    """
    Represents a probability distribution over possible states of a variable.
    """
    variable_id: str
    # Mapping from state_value to probability. Must sum to 1.0.
    distribution: Dict[str, float] 

    def normalize(self):
        vals = np.array(list(self.distribution.values()), dtype=float)
        total = vals.sum()
        if total == 0:
            raise ValueError("Distribution sum is 0")
        vals /= total
        for k, v in zip(self.distribution.keys(), vals.tolist()):
            self.distribution[k] = v

    def entropy(self) -> float:
        """
        Calculate Shannon entropy of the distribution.
        Vectorized via NumPy for O(n) with minimal Python overhead.
        """
        vals = np.array(list(self.distribution.values()), dtype=float)
        mask = vals > 0
        return float(-np.sum(vals[mask] * np.log2(vals[mask])))

    def get_most_likely(self) -> tuple[str, float]:
        """
        Returns the state with the highest probability.
        """
        return max(self.distribution.items(), key=lambda item: item[1])

class BeliefUpdater:
    """
    Handles Bayesian updating of beliefs based on new evidence.
    P(H|E) = P(E|H) * P(H) / P(E)
    """
    
    @staticmethod
    def update(prior: ProbabilisticState, likelihoods: Dict[str, float]) -> ProbabilisticState:
        """
        Updates the prior distribution given the likelihood of the evidence for each hypothesis.
        
        Args:
            prior: The current belief state.
            likelihoods: A dict mapping hypothesis (state keys) to P(Evidence|Hypothesis).
                         Missing keys assume a default small likelihood or 0 depending on model.
        """
        # Vectorized: compute all unnormalized posteriors in one multiply
        keys = list(prior.distribution.keys())
        prior_arr = np.array([prior.distribution[k] for k in keys], dtype=float)
        likelihood_arr = np.array([likelihoods.get(k, 0.001) for k in keys], dtype=float)

        unnormalized = prior_arr * likelihood_arr
        total = unnormalized.sum()
        if total == 0:
            raise ValueError("Posterior distribution sums to 0; check likelihood values")
        normalized = unnormalized / total

        return ProbabilisticState(
            variable_id=prior.variable_id,
            distribution=dict(zip(keys, normalized.tolist()))
        )
