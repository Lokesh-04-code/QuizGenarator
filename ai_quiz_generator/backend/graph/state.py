from typing import TypedDict, List


class QuizState(TypedDict):
    context: str
    single_n: int
    multi_n: int
    tf_n: int
    yn_n: int
    model: str
    single_output: List
    multi_output: List
    tf_output: List
    yn_output: List