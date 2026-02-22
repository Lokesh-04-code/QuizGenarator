from agents.single_mcq_agent import generate_single_mcq
from agents.multi_mcq_agent import generate_multi_mcq
from agents.true_false_agent import generate_true_false
from agents.yes_no_agent import generate_yes_no


def single_node(state):
    state["single_output"] = generate_single_mcq(
        state["context"], state["single_n"], state["model"]
    )
    return state


def multi_node(state):
    state["multi_output"] = generate_multi_mcq(
        state["context"], state["multi_n"], state["model"]
    )
    return state


def tf_node(state):
    state["tf_output"] = generate_true_false(
        state["context"], state["tf_n"], state["model"]
    )
    return state


def yn_node(state):
    state["yn_output"] = generate_yes_no(
        state["context"], state["yn_n"], state["model"]
    )
    return state