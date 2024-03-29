import pytest
from .context import forage_outcomes
from .context import support_functions

def test_weight_outcomes():
    types_dict = {'text_event':0,'event_curr':0,'npc_event':0,'currency_event':0,'lure_event':0,'event_special':0}
    for i in range(1000):
        event_type = support_functions.roll_random_result(forage_outcomes.outcome_types)
        types_dict[event_type] += 1
    # assumes a 25% desired text rate and a 1% desired lure rate
    assertions = ((types_dict['text_event'] > 200 and types_dict['text_event'] < 300),
                  (types_dict['lure_event'] > 0 and types_dict['lure_event'] < 20))
    #assert assert_this
    assert assertions[0] and assertions[1]