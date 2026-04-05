import numpy as np
from scipy.stats import norm
from typing import Dict, Tuple, Any

class BayesianChronology:
    """
    Handles temporal reasoning and uncertainty for QAWM traces.
    """

    @staticmethod
    def normalize_time(value: float, unit: str) -> float:
        """
        Converts time to a standardized 'Years Before Present' (YBP) scale.
        Positive values are years ago.
        """
        if unit == "BP":
            return value
        elif unit == "BC":
            return value + 1950  # 0 BP is defined as 1950 AD
        elif unit == "AD":
            return 1950 - value
        elif unit == "MYA":
            return value * 1_000_000
        else:
            raise ValueError(f"Unknown time unit: {unit}")

    @staticmethod
    def probability_precedes(t1: Dict[str, Any], t2: Dict[str, Any]) -> float:
        """
        Calculates the probability that event t1 precedes event t2 (t1 is older than t2 in YBP).
        Assumes Gaussian distributions for timestamps.
        """
        mu1 = BayesianChronology.normalize_time(t1["value"], t1["unit"])
        sigma1 = t1.get("uncertainty", 0.0)
        
        mu2 = BayesianChronology.normalize_time(t2["value"], t2["unit"])
        sigma2 = t2.get("uncertainty", 0.0)

        # Difference variable D = T1 - T2
        # We want P(T1 > T2) since larger YBP means older
        mu_diff = mu1 - mu2
        sigma_diff = np.sqrt(sigma1**2 + sigma2**2)

        if sigma_diff == 0:
            return 1.0 if mu1 > mu2 else 0.0

        # Z-score for D > 0
        z = mu_diff / sigma_diff
        return norm.cdf(z)
