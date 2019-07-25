base_dir = "/media/nas/projects/fault_attacks_test"

manip_info_list = [
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "mov_rbxrbx_fix",
        "result_name": "intel_core_i3_fix_20190701_1640",
        "params_file": "analyzer_params/test_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "mov_rbxrbx_fix",
        "result_name": "intel_core_i3_fix",
        "params_file": "analyzer_params/test_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "or_rbxrbx_fix",
        "result_name": "intel_core_i3_or_rbxrbx_fix_20190724_1000",
        "params_file": "analyzer_params/test_intel_core_i3_or_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_cmp",
        "result_name": "EM_fix",
        "params_file": "analyzer_params/raspi3_regtest_cmp_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movallreg",
        "result_name": "EM_fix",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movallreg",
        "result_name": "EM_fix_2",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_params.py"
    },
]

carto_info_list = [
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "or_rbxrbx_carto_die_20x40",
        "result_name": "intel_core_i3_or_rbxrbx_carto_die_20x40_20190719_1210",
        "params_file": "analyzer_params/test_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movallreg",
        "result_name": "EM_carto_40x40",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3_INRIA",
        "manip_name": "loop_linux",
        "result_name": "EM_carto_40x40",
        "params_file": "analyzer_params/raspi3_INRIA_loop_linux_EM_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3_INRIA",
        "manip_name": "loop_baremetal",
        "result_name": "EM_carto_40x40",
        "params_file": "analyzer_params/raspi3_INRIA_loop_linux_EM_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3_INRIA",
        "manip_name": "loop_baremetal",
        "result_name": "EM_carto_40x40_2",
        "params_file": "analyzer_params/raspi3_INRIA_loop_linux_EM_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_addr0r1_carto_20x20",
        "result_name": "EM_carto_20x20",
        "params_file": "analyzer_params/raspi3_regtest_addr0r1_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_andallreg_carto_20x20",
        "result_name": "rasp_regtest_andallreg",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_cmp",
        "result_name": "EM_carto_20x20",
        "params_file": "analyzer_params/raspi3_regtest_cmp_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movallreg",
        "result_name": "EM_carto_20x40",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movallreg",
        "result_name": "EM_carto_20x20",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movallreg",
        "result_name": "EM_carto_20x20_2",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movaltr0r3",
        "result_name": "EM_carto_20x20",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movaltr2r7",
        "result_name": "EM_carto_20x20",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movfolr5r8",
        "result_name": "EM_carto_20x20",
        "params_file": "analyzer_params/raspi3_regtest_movfolr5r8_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movr0r0",
        "result_name": "EM_carto_20x20",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movr3r3",
        "result_name": "EM_carto_20x20",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_orallreg",
        "result_name": "EM_carto_topleft_20x20",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_orallreg",
        "result_name": "EM_carto_topleft_20x20_2",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_carto_params.py"
    }
]
