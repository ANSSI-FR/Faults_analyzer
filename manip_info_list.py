base_dir = "/media/nas/projects/fault_attacks_test"

manip_info_list = [
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "mov_rbxrbx_fix",
        "result_name": "intel_core_i3_fix_20190701_1640",
        "params_file": "analyzer_params/test_params.py",
        "id_name": "Intel Core i3 Linux [mov rbx,rbx] EM"
    },
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "mov_rbxrbx_fix",
        "result_name": "intel_core_i3_fix",
        "params_file": "analyzer_params/test_params.py",
        "id_name": "Intel Core i3 Linux [mov rbx,rbx] EM 2"
    },
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "or_rbxrbx_fix",
        "result_name": "intel_core_i3_or_rbxrbx_fix_20190801_1112",
        "params_file": "analyzer_params/test_intel_core_i3_or_params.py",
        "id_name": "Intel Core i3 Linux [orr rbx,rbx] EM"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_cmp",
        "result_name": "EM_fix",
        "params_file": "analyzer_params/raspi3_regtest_cmp_params.py",
        "id_name": "BCM2837 Linux [cmp] EM"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movallreg",
        "result_name": "EM_fix",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_params.py",
        "id_name": "BCM2837 Linux [mov allreg] EM"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "regtest_movallreg",
        "result_name": "EM_fix_2",
        "params_file": "analyzer_params/raspi3_regtest_movallreg_params.py",
        "id_name": "BCM2837 Linux [mov allreg] EM 2"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3_INRIA",
        "manip_name": "orx3x3",
        "result_name": "EM_carto_fix_20190812_1204",
        "params_file": "analyzer_params/raspi3_INRIA_orx3x3_EM.py",
        "id_name": "BCM2837 bare-metal [orr x3,x3] iv1 EM"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3_INRIA",
        "manip_name": "orx3x3",
        "result_name": "EM_carto_fix_IV2_20190814_1734",
        "params_file": "analyzer_params/raspi3_INRIA_orx3x3_IV2_EM.py",
        "id_name": "BCM2837 bare-metal [orr x3,x3] iv2 EM"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3_INRIA",
        "manip_name": "orx3x3",
        "result_name": "EM_carto_fix_IV2_20190819_1110",
        "params_file": "analyzer_params/raspi3_INRIA_orx3x3_IV2_EM.py",
        "id_name": "BCM2837 bare-metal [orr x3,x3] iv2 EM 2"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3_INRIA",
        "manip_name": "orx3x3",
        "result_name": "EM_carto_fix_IV1_20190820_1742",
        "params_file": "analyzer_params/raspi3_INRIA_orx3x3_EM.py",
        "id_name": "BCM2837 bare-metal [orr x3,x3] iv1 EM"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3",
        "manip_name": "orr3r3",
        "result_name": "EM_carto_fix_IV1_20190904_1506",
        "params_file": "analyzer_params/raspi3_orr3r3_EM.py",
        "id_name": "BCM2837 Linux [orr r3,r3] iv1 EM"
    }
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
        "params_file": "analyzer_params/raspi3_regtest_orallreg_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "raspi3_INRIA",
        "manip_name": "orx3x3",
        "result_name": "EM_carto_50x50_20190807_1159",
        "params_file": "analyzer_params/raspi3_INRIA_orx3x3_EM_carto.py"
    },
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "mov_rbxrbx_carto_full_40x40",
        "result_name": "intel_core_i3_map_40x40",
        "params_file": "analyzer_params/test_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "mov_rbxrbx_carto_die_40x40",
        "result_name": "intel_core_i3_mov_rbxrbx_carto_die_40x40_20190624_1229",
        "params_file": "analyzer_params/test_carto_params.py"
    },
    {
        "base_dir": base_dir,
        "device": "intel_core_i3",
        "manip_name": "mov_rbxrbx_carto_cores_20x20",
        "result_name": "intel_core_i3_map_cores_20x20",
        "params_file": "analyzer_params/test_carto_params.py"
    }
]
