from decimal import Decimal

from pow2core.factors.implementations.slot import SlotFactorByFixed


class TestSlotFactorByFixed:
    def test_init_with_basic_params(self):
        weights = {True: 10, False: 5}
        rare_requirements = {1: 2, 2: 3}

        factor = SlotFactorByFixed(weights, rare_requirements)

        assert factor.name == "slot"
        assert factor.rare_requirements == rare_requirements
        assert factor.precision == 2
        assert factor.tokens_with_slot == []

    def test_init_with_custom_precision(self):
        weights = {True: Decimal('10.5'), False: Decimal('5.2')}
        rare_requirements = {1: 2, 2: 3}

        factor = SlotFactorByFixed(weights, rare_requirements, precision=3)

        assert factor.name == "slot"
        assert factor.precision == 3
        assert factor.rare_requirements == rare_requirements

    def test_init_with_decimal_weights(self):
        weights = {True: Decimal('15.75'), False: Decimal('7.25')}
        rare_requirements = {1: 1, 2: 2, 3: 1}

        factor = SlotFactorByFixed(weights, rare_requirements, precision=4)

        assert factor.name == "slot"
        assert factor.rare_requirements == rare_requirements
        assert factor.precision == 4

    def test_load_tokens_with_slot_simple_case(self):
        weights = {True: 10, False: 5}
        rare_requirements = {1: 2, 2: 1}
        factor = SlotFactorByFixed(weights, rare_requirements, max_weight=10, is_visible=True)

        rare_balances = {
            1: [(1, 101), (1, 102), (1, 103), (1, 104)],  # 4 tokens of rare 1
            2: [(1, 201), (1, 202), (1, 203)]        # 3 tokens of rare 2
        }

        factor.load_tokens_with_slot(rare_balances)

        # Should be able to make 2 sets (min(4//2, 3//1) = min(2, 3) = 2)
        # Set 1: 2 tokens from rare 1 + 1 token from rare 2
        # Set 2: 2 tokens from rare 1 + 1 token from rare 2
        # Total: 4 tokens from rare 1 + 2 tokens from rare 2 = 6 tokens
        expected_tokens = [(1, 101), (1, 102), (1, 103), (1, 104), (1, 201), (1, 202)]
        assert len(factor.tokens_with_slot) == 6
        assert set(factor.tokens_with_slot) == set(expected_tokens)

    def test_load_tokens_with_slot_limited_by_requirements(self):
        weights = {True: 10, False: 5}
        rare_requirements = {1: 3, 2: 2}
        factor = SlotFactorByFixed(weights, rare_requirements)

        rare_balances = {
            1: [(1, 101), (1, 102), (1, 103), (1, 104), (1, 105), (1, 106)],  # 6 tokens of rare 1
            2: [(1, 201), (1, 202), (1, 203)]                   # 3 tokens of rare 2
        }

        factor.load_tokens_with_slot(rare_balances)

        # Should be able to make 1 set (min(6//3, 3//2) = min(2, 1) = 1)
        # Set 1: 3 tokens from rare 1 + 2 tokens from rare 2 = 5 tokens
        assert len(factor.tokens_with_slot) == 5
        expected_tokens = [(1, 101), (1, 102), (1, 103), (1, 201), (1, 202)]
        assert set(factor.tokens_with_slot) == set(expected_tokens)

    def test_load_tokens_with_slot_no_sets_possible(self):
        weights = {True: 10, False: 5}
        rare_requirements = {1: 5, 2: 3}
        factor = SlotFactorByFixed(weights, rare_requirements)

        rare_balances = {
            1: [(1, 101), (1, 102)],    # Only 2 tokens of rare 1 (need 5)
            2: [(1, 201), (1, 202), (1, 203)] # 3 tokens of rare 2 (need 3)
        }

        factor.load_tokens_with_slot(rare_balances)

        # Should be able to make 0 sets (min(2//5, 3//3) = min(0, 1) = 0)
        assert len(factor.tokens_with_slot) == 0

    def test_load_tokens_with_slot_multiple_calls(self):
        weights = {True: 10, False: 5}
        rare_requirements = {1: 1, 2: 1}
        factor = SlotFactorByFixed(weights, rare_requirements)

        # First call
        rare_balances_1 = {
            1: [(1, 101), (1, 102)],
            2: [(1, 201), (1, 202)]
        }
        factor.load_tokens_with_slot(rare_balances_1)
        assert len(factor.tokens_with_slot) == 4

        # Second call - should extend the list
        rare_balances_2 = {
            1: [(1, 103)],
            2: [(1, 203)]
        }
        factor.load_tokens_with_slot(rare_balances_2)
        assert len(factor.tokens_with_slot) == 6
        expected_tokens = [(1, 101), (1, 102), (1, 201), (1, 202), (1, 103), (1, 203)]
        assert set(factor.tokens_with_slot) == set(expected_tokens)

    def test_get_weight_token_with_slot(self):
        weights = {True: 15, False: 3}
        rare_requirements = {1: 1}
        factor = SlotFactorByFixed(weights, rare_requirements, max_weight=15, is_visible=True)

        # Add some tokens to slot list
        factor.tokens_with_slot = [(1, 101), (1, 102), (1, 103)]

        # Token in slot should get True weight
        assert factor.get_weight(collection_id=1, token_id=101).weight == Decimal('15.00')
        assert factor.get_weight(collection_id=1, token_id=102).weight == Decimal('15.00')
        assert factor.get_weight(collection_id=1, token_id=103).weight == Decimal('15.00')

    def test_get_weight_token_without_slot(self):
        weights = {True: 15, False: 3}
        rare_requirements = {1: 1}
        factor = SlotFactorByFixed(weights, rare_requirements, max_weight=15, is_visible=True)

        # Add some tokens to slot list
        factor.tokens_with_slot = [(1, 101), (1, 102), (1, 103)]

        # Token not in slot should get False weight
        assert factor.get_weight(collection_id=1, token_id=201).weight == Decimal('3.00')
        assert factor.get_weight(collection_id=1, token_id=999).weight == Decimal('3.00')

    def test_get_weight_with_decimal_weights_and_precision(self):
        weights = {True: Decimal('12.555'), False: Decimal('2.777')}
        rare_requirements = {1: 1}
        factor = SlotFactorByFixed(weights, rare_requirements, precision=3, max_weight=15, is_visible=True)

        factor.tokens_with_slot = [(1, 101)]

        # Should respect precision
        assert factor.get_weight(collection_id=1, token_id=101).weight == Decimal('12.555')
        assert factor.get_weight(collection_id=1, token_id=999).weight == Decimal('2.777')

    def test_get_weight_empty_slot_list(self):
        weights = {True: 10, False: 1}
        rare_requirements = {1: 1}
        factor = SlotFactorByFixed(weights, rare_requirements, max_weight=10, is_visible=True)

        # No tokens in slot list, so all should get False weight
        assert factor.get_weight(collection_id=1, token_id=101).weight == Decimal('1.00')
        assert factor.get_weight(collection_id=1, token_id=999).weight == Decimal('1.00')

    def test_complex_scenario(self):
        """Test a complex scenario with multiple rares and requirements"""
        weights = {True: 20, False: 2}
        rare_requirements = {1: 2, 2: 1, 3: 3}
        factor = SlotFactorByFixed(weights, rare_requirements, precision=1, max_weight=20, is_visible=True)

        rare_balances = {
            1: [(1, 1001), (1, 1002), (1, 1003), (1, 1004), (1, 1005), (1, 1006)],  # 6 tokens
            2: [(1, 2001), (1, 2002), (1, 2003), (1, 2004)],               # 4 tokens
            3: [(1, 3001), (1, 3002), (1, 3003), (1, 3004), (1, 3005), (1, 3006)]   # 6 tokens
        }

        factor.load_tokens_with_slot(rare_balances)

        # Can make min(6//2, 4//1, 6//3) = min(3, 4, 2) = 2 sets
        # Each set needs: 2 from rare1 + 1 from rare2 + 3 from rare3 = 6 tokens
        # Total: 2 sets * 6 tokens = 12 tokens
        assert len(factor.tokens_with_slot) == 12

        # Test weights
        assert factor.get_weight(collection_id=1, token_id=1001).weight == Decimal('20.0')  # In slot
        assert factor.get_weight(collection_id=1, token_id=9999).weight == Decimal('2.0')   # Not in slot
