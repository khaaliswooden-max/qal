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
        total = sum(self.distribution.values())
        if total == 0:
            raise ValueError("Distribution sum is 0")
        for k in self.distribution:
            self.distribution[k] /= total

    def entropy(self) -> float:
        """
        Calculate Shannon entropy of the distribution.
        """
        ent = 0.0
        for p in self.distribution.values():
            if p > 0:
                ent -= p * np.log2(p)
        return ent

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
        posterior_dist = {}
        
        # Calculate unnormalized posterior
        for hypothesis, prior_prob in prior.distribution.items():
            likelihood = likelihoods.get(hypothesis, 0.001) # Default to small epsilon if unknown
            posterior_dist[hypothesis] = prior_prob * likelihood
            
        # Create new state and normalize
        new_state = ProbabilisticState(
            variable_id=prior.variable_id,
            distribution=posterior_dist
        )
        new_state.normalize()
        return new_state
