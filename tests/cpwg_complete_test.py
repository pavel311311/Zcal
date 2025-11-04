#!/usr/bin/env python3
"""
CPWG完整参数测试 - 包含G(信号到地间距)和GW(地线宽度)
测试GSSG差分对结构的完整几何参数对阻抗的影响
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lala.PCB_board_Res.src.app import PCBImpedanceCalculator

def test_cpwg_with_full_parameters():
    """测试包含完整参数的CPWG计算"""
    print("🧪 CPWG完整参数测试")
    print("=" * 60)
    
    calculator = PCBImpedanceCalculator()
    
    # 测试用例1: 标准参数 + 新参数
    print("\n📐 测试用例1: 标准100Ω差分对设计 + 完整几何参数")
    params = {
        'w': 0.1,      # 信号线宽 (mm)
        's': 0.15,     # 信号线间距 (mm) 
        'h': 0.2,      # 介质厚度 (mm)
        't': 0.035,    # 铜厚 (mm)
        'er': 4.3,     # FR4介电常数
        'g': 0.1,      # 信号到地间距 (mm) - 新参数
        'gw': 0.3      # 地线宽度 (mm) - 新参数
    }
    
    result = calculator.cpwg_impedance(**params)
    
    if result['status'] == 'success':
        print(f"✅ 计算成功!")
        print(f"   差分阻抗: {result['differential_impedance']}Ω")
        print(f"   单端阻抗: {result['single_ended_impedance']}Ω")
        print(f"   奇模阻抗: {result['odd_mode_impedance']}Ω")
        print(f"   偶模阻抗: {result['even_mode_impedance']}Ω")
        print(f"   共模阻抗: {result['common_mode_impedance']}Ω")
        print(f"   耦合系数: {result['coupling_coefficient']}")
        print(f"   有效介电常数: {result['er_eff']}")
        print(f"   k_odd参数: {result['k_odd']}")
        print(f"   k_even参数: {result['k_even']}")
        print(f"   K_odd椭圆积分: {result['K_odd']}")
        print(f"   K_even椭圆积分: {result['K_even']}")
        print(f"   奇模有效εr: {result['er_eff_odd']}")
        print(f"   偶模有效εr: {result['er_eff_even']}")
    else:
        print(f"❌ 计算失败: {result['message']}")
    
    return result

def test_parameter_effects():
    """测试各参数对阻抗的影响"""
    print("\n🔍 参数影响分析")
    print("=" * 60)
    
    calculator = PCBImpedanceCalculator()
    
    # 基础参数
    base_params = {
        'w': 0.1,      
        's': 0.15,     
        'h': 0.2,      
        't': 0.035,    
        'er': 4.3,     
        'g': 0.1,      
        'gw': 0.3      
    }
    
    # 1. 测试信号到地间距G的影响
    print("\n📏 信号到地间距(G)影响:")
    g_values = [0.05, 0.1, 0.15, 0.2, 0.25]
    
    for g in g_values:
        params = base_params.copy()
        params['g'] = g
        result = calculator.cpwg_impedance(**params)
        
        if result['status'] == 'success':
            print(f"   G={g:0.2f}mm: Z_diff={result['differential_impedance']:0.1f}Ω, "
                  f"耦合={result['coupling_coefficient']:0.3f}, "
                  f"k_odd={result['k_odd']:0.3f}")
    
    # 2. 测试地线宽度GW的影响
    print("\n📐 地线宽度(GW)影响:")
    gw_values = [0.2, 0.3, 0.5, 0.8, 1.0]
    
    for gw in gw_values:
        params = base_params.copy()
        params['gw'] = gw
        result = calculator.cpwg_impedance(**params)
        
        if result['status'] == 'success':
            print(f"   GW={gw:0.2f}mm: Z_diff={result['differential_impedance']:0.1f}Ω, "
                  f"k_even={result['k_even']:0.3f}")
    
    # 3. 测试G/W比值影响
    print("\n📊 G/W比值影响:")
    ratios = [0.5, 1.0, 1.5, 2.0, 2.5]
    
    for ratio in ratios:
        params = base_params.copy()
        params['g'] = ratio * params['w']  # G = ratio * W
        result = calculator.cpwg_impedance(**params)
        
        if result['status'] == 'success':
            print(f"   G/W={ratio:0.1f}: Z_diff={result['differential_impedance']:0.1f}Ω, "
                  f"Z_single={result['single_ended_impedance']:0.1f}Ω")

def test_design_optimization():
    """测试100Ω差分对设计优化"""
    print("\n🎯 100Ω差分对设计优化")
    print("=" * 60)
    
    calculator = PCBImpedanceCalculator()
    
    target_impedance = 100  # 目标差分阻抗
    tolerance = 5  # 容差 ±5Ω
    
    print(f"目标: {target_impedance}±{tolerance}Ω 差分阻抗")
    print("\n尝试不同的参数组合:")
    
    # 参数组合
    test_cases = [
        {'w': 0.08, 's': 0.12, 'g': 0.08, 'gw': 0.25, 'name': '紧凑设计'},
        {'w': 0.10, 's': 0.15, 'g': 0.10, 'gw': 0.30, 'name': '标准设计'},
        {'w': 0.12, 's': 0.18, 'g': 0.12, 'gw': 0.35, 'name': '宽松设计'},
        {'w': 0.10, 's': 0.10, 'g': 0.15, 'gw': 0.40, 'name': '强耦合设计'},
        {'w': 0.10, 's': 0.20, 'g': 0.05, 'gw': 0.20, 'name': '弱耦合设计'},
    ]
    
    common_params = {'h': 0.2, 't': 0.035, 'er': 4.3}
    
    for case in test_cases:
        params = {**common_params, **{k: v for k, v in case.items() if k != 'name'}}
        result = calculator.cpwg_impedance(**params)
        
        if result['status'] == 'success':
            diff_z = result['differential_impedance']
            error = abs(diff_z - target_impedance)
            match = "✅" if error <= tolerance else "❌"
            
            print(f"\n{match} {case['name']}:")
            print(f"   参数: W={params['w']}, S={params['s']}, G={params['g']}, GW={params['gw']}")
            print(f"   差分阻抗: {diff_z}Ω (误差: {error:0.1f}Ω)")
            print(f"   耦合系数: {result['coupling_coefficient']:0.3f}")
            
def test_extreme_cases():
    """测试极端情况"""
    print("\n⚠️  极端情况测试")
    print("=" * 60)
    
    calculator = PCBImpedanceCalculator()
    
    # 极端测试用例
    extreme_cases = [
        {'w': 0.05, 's': 0.05, 'g': 0.02, 'gw': 0.1, 'name': '极小几何'},
        {'w': 0.5, 's': 0.5, 'g': 0.5, 'gw': 1.0, 'name': '极大几何'},
        {'w': 0.1, 's': 0.01, 'g': 0.1, 'gw': 0.3, 'name': '极强耦合'},
        {'w': 0.1, 's': 1.0, 'g': 0.1, 'gw': 0.3, 'name': '极弱耦合'},
        {'w': 0.1, 's': 0.15, 'g': 0.01, 'gw': 0.3, 'name': '极小间距'},
        {'w': 0.1, 's': 0.15, 'g': 0.1, 'gw': 0.05, 'name': '极窄地线'},
    ]
    
    common_params = {'h': 0.2, 't': 0.035, 'er': 4.3}
    
    for case in extreme_cases:
        params = {**common_params, **{k: v for k, v in case.items() if k != 'name'}}
        result = calculator.cpwg_impedance(**params)
        
        print(f"\n📋 {case['name']}:")
        if result['status'] == 'success':
            print(f"   ✅ 差分阻抗: {result['differential_impedance']}Ω")
            print(f"      耦合系数: {result['coupling_coefficient']:0.3f}")
            print(f"      k_odd: {result['k_odd']:0.3f}")
            print(f"      k_even: {result['k_even']:0.3f}")
        else:
            print(f"   ❌ 计算失败: {result['message']}")

if __name__ == "__main__":
    print("🚀 CPWG完整参数测试套件")
    print("测试GSSG差分对结构，包含G(信号到地间距)和GW(地线宽度)参数")
    
    # 运行所有测试
    test_cpwg_with_full_parameters()
    test_parameter_effects()
    test_design_optimization()
    test_extreme_cases()
    
    print("\n🎯 测试完成!")
    print("现在CPWG模型包含了完整的几何参数，更准确地反映实际PCB结构!")