result_names = ["intel_core_i3_fix_20190701_1640", "intel_core_i3_fix"]

base_dir = "/media/nas/projects/fault_attacks_test"

manip_info_list = [{
    "base_dir": base_dir,
    "device": "intel_core_i3",
    "manip_name": "mov_rbxrbx_fix",
    "result_name": result_name,
    "params_file": "test_params.py"
} for result_name in result_names]
