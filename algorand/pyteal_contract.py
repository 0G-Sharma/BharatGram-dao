from pyteal import *

# Simple stateful contract that stores a counter in global state

def approval_program():
    handle_creation = Seq([
        App.globalPut(Bytes("count"), Int(0)),
        Return(Int(1)),
    ])

    increment = Seq([
        App.globalPut(Bytes("count"), App.globalGet(Bytes("count")) + Int(1)),
        Return(Int(1)),
    ])

    reset = Seq([
        Assert(Txn.sender() == Global.creator_address()),
        App.globalPut(Bytes("count"), Int(0)),
        Return(Int(1)),
    ])

    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.NoOp, Cond([
            [Txn.application_args[0] == Bytes("inc"), increment],
            [Txn.application_args[0] == Bytes("reset"), reset],
        ])],
    )

    return program


def clear_state_program():
    return Return(Int(1))


if __name__ == "__main__":
    print(compileTeal(approval_program(), mode=Mode.Application, version=5))
