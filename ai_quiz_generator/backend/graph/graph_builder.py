from langgraph.graph import StateGraph, END
from graph.state import QuizState
from graph.nodes import single_node, multi_node, tf_node, yn_node


def build_graph():

    builder = StateGraph(QuizState)

    builder.add_node("single", single_node)
    builder.add_node("multi", multi_node)
    builder.add_node("tf", tf_node)
    builder.add_node("yn", yn_node)

    builder.set_entry_point("single")

    builder.add_edge("single", "multi")
    builder.add_edge("multi", "tf")
    builder.add_edge("tf", "yn")
    builder.add_edge("yn", END)

    return builder.compile()