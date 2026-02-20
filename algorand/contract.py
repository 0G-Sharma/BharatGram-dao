from pyteal import *

# BharatGram Transparency Smart Contract
# Stores project metadata and funding status on-chain.

def approval_program():
    # Global state keys
    total_projects = Bytes("total_projects")
    admin_address = Bytes("admin")

    # App Args
    # Method 0: register_project(project_id, budget, spent, status_hash)
    
    op_register = Bytes("register")
    op_update = Bytes("update")

    # 1. Initialization
    handle_creation = Seq([
        App.globalPut(total_projects, Int(0)),
        App.globalPut(admin_address, Txn.sender()),
        Return(Int(1))
    ])

    # 2. Register Project
    # Args: ["register", project_id (int), budget (int), spent (int), status_hash (string)]
    # Note: project_id is used as key for Box storage or global state.
    # We will use Box Storage for scalability (unlimited projects).
    
    project_id = Btoi(Txn.application_args[1])
    budget = Btoi(Txn.application_args[2])
    spent = Btoi(Txn.application_args[3])
    status_hash = Txn.application_args[4] # SHA256 of project details for verification

    # Box name is the project_id (8 bytes)
    box_name = Txn.application_args[1]

    register_project = Seq([
        Assert(Txn.sender() == App.globalGet(admin_address)),
        # Box Create: name, size (8 bytes budget + 8 bytes spent + 32 bytes hash = 48)
        App.box_create(box_name, Int(48)),
        App.box_replace(box_name, Int(0), Txn.application_args[2]), # budget
        App.box_replace(box_name, Int(8), Txn.application_args[3]), # spent
        App.box_replace(box_name, Int(16), status_hash),           # hash
        App.globalPut(total_projects, App.globalGet(total_projects) + Int(1)),
        Return(Int(1))
    ])

    # 3. Update Progress
    # Args: ["update", project_id, spent, status_hash]
    update_progress = Seq([
        Assert(Txn.sender() == App.globalGet(admin_address)),
        # Check if box exists
        Assert(App.box_length(box_name).hasValue()),
        App.box_replace(box_name, Int(8), Txn.application_args[2]), # new spent
        App.box_replace(box_name, Int(16), Txn.application_args[3]), # new hash
        Return(Int(1))
    ])

    # Router
    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Txn.sender() == App.globalGet(admin_address))],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(Txn.sender() == App.globalGet(admin_address))],
        [Txn.on_completion() == OnComplete.NoOp, Cond(
            [Txn.application_args[0] == op_register, register_project],
            [Txn.application_args[0] == op_update, update_progress]
        )]
    )

    return program

def clear_state_program():
    return Return(Int(1))

if __name__ == "__main__":
    with open("approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=8) # Version 8 for Box support
        f.write(compiled)
    with open("clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=8)
        f.write(compiled)
    print("TEAL files generated: approval.teal, clear.teal")
