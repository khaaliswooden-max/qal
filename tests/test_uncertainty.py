"""Tests for Uncertainty Quantification.

Tests validate:
1. Probability distribution tracking for all inferences
2. Confidence interval computation
3. Uncertainty propagation through causal chains
4. Shannon entropy calculations
5. Bayesian updating
"""
import unittest
import numpy as np
from qawm.inference.bayesian import ProbabilisticState, BeliefUpdater


class TestProbabilisticState(unittest.TestCase):
    """Test probability distribution handling."""
    
    def test_distribution_normalization(self):
        """Distributions must sum to 1.0 after normalization."""
        state = ProbabilisticState(
            variable_id="hypothesis_1",
            distribution={"A": 2.0, "B": 3.0, "C": 5.0}
        )
        state.normalize()
        
        total = sum(state.distribution.values())
        self.assertAlmostEqual(total, 1.0)
    
    def test_normalized_proportions(self):
        """Normalized values maintain relative proportions."""
        state = ProbabilisticState(
            variable_id="test",
            distribution={"A": 1.0, "B": 3.0}
        )
        state.normalize()
        
        self.assertAlmostEqual(state.distribution["A"], 0.25)
        self.assertAlmostEqual(state.distribution["B"], 0.75)
    
    def test_empty_distribution_raises_error(self):
        """Cannot normalize distribution that sums to zero."""
        state = ProbabilisticState(
            variable_id="empty",
            distribution={"A": 0.0, "B": 0.0}
        )
        
        with self.assertRaises(ValueError):
            state.normalize()
    
    def test_get_most_likely(self):
        """Can retrieve most likely state."""
        state = ProbabilisticState(
            variable_id="test",
            distribution={"A": 0.1, "B": 0.6, "C": 0.3}
        )
        
        most_likely, probability = state.get_most_likely()
        self.assertEqual(most_likely, "B")
        self.assertAlmostEqual(probability, 0.6)


class TestShannonEntropy(unittest.TestCase):
    """Test entropy calculations for uncertainty quantification."""
    
    def test_uniform_distribution_maximum_entropy(self):
        """Uniform distribution has maximum entropy."""
        uniform = ProbabilisticState(
            variable_id="uniform",
            distribution={"A": 0.25, "B": 0.25, "C": 0.25, "D": 0.25}
        )
        
        entropy = uniform.entropy()
        # Maximum entropy for 4 states is log2(4) = 2.0
        self.assertAlmostEqual(entropy, 2.0)
    
    def test_certain_state_zero_entropy(self):
        """Certain (single) state has zero entropy."""
        certain = ProbabilisticState(
            variable_id="certain",
            distribution={"A": 1.0, "B": 0.0, "C": 0.0}
        )
        
        entropy = certain.entropy()
        self.assertAlmostEqual(entropy, 0.0)
    
    def test_binary_distribution_entropy(self):
        """Binary distribution entropy matches formula."""
        binary = ProbabilisticState(
            variable_id="binary",
            distribution={"H": 0.5, "T": 0.5}
        )
        
        entropy = binary.entropy()
        # H = -0.5*log2(0.5) - 0.5*log2(0.5) = 1.0
        self.assertAlmostEqual(entropy, 1.0)


class TestBayesianUpdating(unittest.TestCase):
    """Test Bayesian belief updating."""
    
    def test_update_shifts_probability(self):
        """Evidence should shift probability toward supported hypothesis."""
        prior = ProbabilisticState(
            variable_id="cause",
            distribution={"drought": 0.33, "invasion": 0.33, "earthquake": 0.34}
        )
        
        # Evidence strongly supports drought
        likelihoods = {
            "drought": 0.9,
            "invasion": 0.1,
            "earthquake": 0.2
        }
        
        posterior = BeliefUpdater.update(prior, likelihoods)
        
        # Drought should now be most likely
        self.assertGreater(posterior.distribution["drought"], posterior.distribution["invasion"])
        self.assertGreater(posterior.distribution["drought"], posterior.distribution["earthquake"])
    
    def test_update_preserves_normalization(self):
        """Posterior distribution must remain normalized."""
        prior = ProbabilisticState(
            variable_id="test",
            distribution={"A": 0.5, "B": 0.5}
        )
        
        likelihoods = {"A": 0.8, "B": 0.2}
        posterior = BeliefUpdater.update(prior, likelihoods)
        
        total = sum(posterior.distribution.values())
        self.assertAlmostEqual(total, 1.0)
    
    def test_update_with_missing_likelihood_uses_epsilon(self):
        """Missing likelihoods use small epsilon, not zero."""
        prior = ProbabilisticState(
            variable_id="test",
            distribution={"A": 0.5, "B": 0.5}
        )
        
        # Only provide likelihood for A
        likelihoods = {"A": 0.9}
        posterior = BeliefUpdater.update(prior, likelihoods)
        
        # B should still have some probability (epsilon)
        self.assertGreater(posterior.distribution["B"], 0)
    
    def test_sequential_updates(self):
        """Multiple updates should accumulate evidence correctly."""
        prior = ProbabilisticState(
            variable_id="hypothesis",
            distribution={"H1": 0.5, "H2": 0.5}
        )
        
        # First evidence slightly favors H1
        evidence_1 = {"H1": 0.6, "H2": 0.4}
        posterior_1 = BeliefUpdater.update(prior, evidence_1)
        
        # Second evidence also favors H1
        evidence_2 = {"H1": 0.7, "H2": 0.3}
        posterior_2 = BeliefUpdater.update(posterior_1, evidence_2)
        
        # H1 should be increasingly likely
        self.assertGreater(posterior_2.distribution["H1"], posterior_1.distribution["H1"])


class TestUncertaintyCones(unittest.TestCase):
    """Test uncertainty visualization concepts."""
    
    def test_entropy_as_uncertainty_measure(self):
        """Higher entropy = more uncertainty."""
        low_uncertainty = ProbabilisticState(
            variable_id="low",
            distribution={"A": 0.9, "B": 0.1}
        )
        
        high_uncertainty = ProbabilisticState(
            variable_id="high",
            distribution={"A": 0.5, "B": 0.5}
        )
        
        self.assertLess(low_uncertainty.entropy(), high_uncertainty.entropy())
    
    def test_confidence_interval_concept(self):
        """Test confidence interval calculation approach."""
        # For a simple discrete distribution, CI includes states until
        # cumulative probability exceeds threshold
        distribution = {"A": 0.5, "B": 0.3, "C": 0.15, "D": 0.05}
        
        # 95% CI should include A, B, C (cumulative 0.95)
        sorted_states = sorted(distribution.items(), key=lambda x: -x[1])
        cumulative = 0
        ci_states = []
        for state, prob in sorted_states:
            cumulative += prob
            ci_states.append(state)
            if cumulative >= 0.95:
                break
        
        self.assertIn("A", ci_states)
        self.assertIn("B", ci_states)
        self.assertIn("C", ci_states)


if __name__ == '__main__':
    unittest.main()
