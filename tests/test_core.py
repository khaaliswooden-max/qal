import unittest
from datetime import datetime, timedelta
from qawm.core.models import Entity, Event, Relation, Layer, Confidence, RelationType
from qawm.inference.bayesian import ProbabilisticState, BeliefUpdater
from qawm.inference.causal import CausalGraph

class TestQAWMCore(unittest.TestCase):

    def test_entity_creation(self):
        e = Entity(
            id="e1",
            type="Artifact",
            layer=Layer.L0_PHYSICAL,
            attributes={"material": "ceramic"}
        )
        self.assertEqual(e.id, "e1")
        self.assertEqual(e.layer, Layer.L0_PHYSICAL)

    def test_bayesian_update(self):
        # Prior: Is the vase Greek or Roman?
        prior = ProbabilisticState(
            variable_id="vase_origin",
            distribution={"Greek": 0.5, "Roman": 0.5}
        )
        
        # Evidence: Found red-figure style (High likelihood for Greek)
        likelihoods = {"Greek": 0.9, "Roman": 0.1}
        
        posterior = BeliefUpdater.update(prior, likelihoods)
        
        greek_prob = posterior.distribution["Greek"]
        roman_prob = posterior.distribution["Roman"]
        
        self.assertGreater(greek_prob, roman_prob)
        self.assertAlmostEqual(greek_prob + roman_prob, 1.0)
        print(f"Posterior: {posterior.distribution}")

    def test_causal_graph(self):
        cg = CausalGraph()
        
        t0 = datetime.now()
        t1 = t0 + timedelta(hours=1)
        
        event_cause = Event(
            id="evt1", type="Fire", layer=Layer.L0_PHYSICAL, 
            timestamp=t0, confidence=Confidence.VERIFIED
        )
        event_effect = Event(
            id="evt2", type="AshLayer", layer=Layer.L0_PHYSICAL, 
            timestamp=t1, confidence=Confidence.VERIFIED
        )
        
        cg.add_event(event_cause)
        cg.add_event(event_effect)
        
        rel = Relation(
            source_id="evt1", target_id="evt2", 
            type=RelationType.TRANSFORMS, weight=1.0
        )
        
        cg.add_relation(rel)
        
        self.assertTrue(cg.check_consistency())
        self.assertIn(event_cause, cg.get_ancestors("evt2"))

    def test_temporal_paradox(self):
        cg = CausalGraph()
        t0 = datetime.now()
        t1 = t0 + timedelta(hours=1)
        
        # Cause is LATER than Effect
        event_cause = Event(id="c", type="C", layer=Layer.L0_PHYSICAL, timestamp=t1, confidence=Confidence.VERIFIED)
        event_effect = Event(id="e", type="E", layer=Layer.L0_PHYSICAL, timestamp=t0, confidence=Confidence.VERIFIED)
        
        cg.add_event(event_cause)
        cg.add_event(event_effect)
        
        rel = Relation(source_id="c", target_id="e", type=RelationType.INFLUENCES, weight=1.0)
        
        with self.assertRaises(ValueError):
            cg.add_relation(rel)

if __name__ == '__main__':
    unittest.main()
