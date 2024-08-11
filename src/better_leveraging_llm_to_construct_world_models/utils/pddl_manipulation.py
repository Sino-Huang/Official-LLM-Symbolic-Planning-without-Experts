# This file will manipulate pddl action schemas to get hard negatives examples.

from copy import deepcopy
import numpy as np
from pddl.logic import Predicate, Constant, Variable
from pddl.logic.base import And, Not, Or, BinaryOp, UnaryOp
from pddl.core import Domain, Problem, Action, Requirements, Formula
from pddl.logic.effects import AndEffect

from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import (
    get_action_schema_answer_str,
    get_domain_model_from_name,
)

MANIPULATION_TYPE_CONSTANT_LST = ["swap", "negate", "remove"]



def get_manipulated_action_lst(
    action_model: Action, manipulated_action_num, pollution_cap=2
):
    # this is also known as generating hard negatives by polluting with noise
    # type of manipulation: swap, negate, remove
    # * swap means we swap the predicate between preconditions and effects
    # * negate means we negate the predicate in the preconditions or effects
    # * remove means we remove the predicate from the preconditions or effects
    # * add (mutex exclusive) means we add a new predicate that is mutex exclusive with the existing predicates, is supported but not added here due to dependency on the fast-downward planner, check `mutex_exclusive_extractor.py` for more details`
    # pollution_cap will control the maximum number of manipulations for each action

    # randomly select number of manipulations for each action
    manipulated_action_lst = []
    manipulation_details_lst = [] 
    for _ in range(manipulated_action_num):
        # randomly select the number of manipulations
        num_manipulations = np.random.randint(1, pollution_cap + 1)

        # get precondition and effect
        precondition = action_model.precondition
        effect = action_model.effect

        if isinstance(precondition, BinaryOp):
            precon_operands = list(precondition.operands)
        else:
            precon_operands = [precondition]

        if isinstance(effect, AndEffect):
            effect_operands = list(effect.operands)
        else:
            effect_operands = [effect]

        updated_precon_operands = []
        updated_effect_operands = []

        available_manipulation_type_lst = deepcopy(MANIPULATION_TYPE_CONSTANT_LST)
        cur_manip_count = 0
        manipulation_detail_str = ""
        while (
            cur_manip_count < num_manipulations
            and len(available_manipulation_type_lst) > 0
            and (len(precon_operands) > 0 or len(effect_operands) > 0)
        ):
            manip_type = np.random.choice(available_manipulation_type_lst)
            # randomly select the predicate to manipulate
            if manip_type == "swap":
                if len(precon_operands) == 0 or len(effect_operands) == 0:
                    # cannot swap if one of them is empty
                    available_manipulation_type_lst.remove("swap")
                    continue
                # randomly select the predicate to swap
                swap_idx = np.random.randint(0, len(precon_operands))
                swap_predicate = precon_operands[swap_idx]
                # randomly select the predicate to swap with
                swap_with_idx = np.random.randint(0, len(effect_operands))
                swap_with_predicate = effect_operands[swap_with_idx]
                # swap the predicates
                updated_precon_operands.append(swap_with_predicate)
                updated_effect_operands.append(swap_predicate)
                # pop the old
                precon_operands.pop(swap_idx)
                effect_operands.pop(swap_with_idx)
                cur_manip_count += 1
                manipulation_detail_str += f"swap {swap_predicate} with {swap_with_predicate}\n"

            elif manip_type == "negate":
                # randomly select the predicate to negate
                # randomly pick precondition or effect
                negation_idx = np.random.randint(0, 2)
                if len(precon_operands) == 0:
                    negation_idx = 1
                elif len(effect_operands) == 0:
                    negation_idx = 0

                if negation_idx == 0 and len(precon_operands) > 0:
                    # randomly select the predicate to negate
                    negation_idx = np.random.randint(0, len(precon_operands))
                    negated_predicate = precon_operands[negation_idx]
                    if isinstance(negated_predicate, Not):
                        # remove the negation
                        updated_precon_operands.append(negated_predicate.argument)
                    else:
                        updated_precon_operands.append(Not(negated_predicate))
                    # remove the old
                    precon_operands.pop(negation_idx)
                    cur_manip_count += 1
                    manipulation_detail_str += f"negate {negated_predicate} in preconditions\n"
                elif negation_idx == 1 and len(effect_operands) > 0:
                    # randomly select the predicate to negate
                    negation_idx = np.random.randint(0, len(effect_operands))
                    negated_predicate = effect_operands[negation_idx]
                    if isinstance(negated_predicate, Not):
                        # remove the negation
                        updated_effect_operands.append(negated_predicate.argument)
                    else:
                        updated_effect_operands.append(Not(negated_predicate))
                    # remove the old
                    effect_operands.pop(negation_idx)
                    cur_manip_count += 1
                    manipulation_detail_str += f"negate {negated_predicate} in effects\n"
                else:
                    # either precon_operands or effect_operands is empty
                    available_manipulation_type_lst.remove("negate")
                    continue

            elif manip_type == "remove":
                # randomly select the predicate to remove
                # randomly pick precondition or effect
                removal_idx = np.random.randint(0, 2)
                if len(precon_operands) <= 1:
                    removal_idx = 1
                elif len(effect_operands) <= 1:
                    removal_idx = 0

                if removal_idx == 0 and len(precon_operands) > 1:
                    removal_idx = np.random.randint(0, len(precon_operands))
                    manipulation_detail_str += f"remove {precon_operands[removal_idx]} from preconditions\n"
                    precon_operands.pop(removal_idx)
                    cur_manip_count += 1
                elif removal_idx == 1 and len(effect_operands) > 1:
                    removal_idx = np.random.randint(0, len(effect_operands))
                    manipulation_detail_str += f"remove {effect_operands[removal_idx]} from effects\n"
                    effect_operands.pop(removal_idx)
                    cur_manip_count += 1
                else:
                    # either precon_operands or effect_operands is empty
                    available_manipulation_type_lst.remove("remove")
                    continue
        # we extend the remaining predicates
        updated_precon_operands.extend(precon_operands)
        updated_effect_operands.extend(effect_operands)
        # now we have the new preconditions and effects
        # we build a new action
        manipulated_action = Action(
            name=action_model.name,
            parameters=action_model.parameters,
            precondition=And(*updated_precon_operands),
            effect=AndEffect(*updated_effect_operands),
        )
        manipulated_action_lst.append(manipulated_action)
        manipulation_details_lst.append(manipulation_detail_str)

    return manipulated_action_lst, manipulation_details_lst


if __name__ == "__main__":
    # test
    test_domain = "doors"
    test_domain_model = get_domain_model_from_name(test_domain)
    action_model_lst = list(test_domain_model.actions)

    manipulated_action_lst, manipulation_details_lst = get_manipulated_action_lst(
        action_model_lst[0], 2, 2
    )

    for action, manipulate_detail in zip(manipulated_action_lst, manipulation_details_lst):
        print("Manipulation Detail")
        print(manipulate_detail)
        print("Polluted Action")
        print(get_action_schema_answer_str(action, add_hint=False))
        print("\n\n")

    print("Original Action")
    print(get_action_schema_answer_str(action_model_lst[0], add_hint=False))
