"""
扩展传输线结构测试脚本
测试GSSG和其他新增的传输线类型
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import PCBImpedanceCalculator

def print_separator(title):
    """打印分隔符"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_result(description, result):
    """格式化打印结果"""
    print(f"\n📊 {description}")
    print("-" * 40)
    
    if result['status'] == 'success':
        # 基本阻抗结果
        if 'impedance' in result:
            print(f"特征阻抗: {result['impedance']} Ω")
        
        # 差分对相关结果
        if 'differential_impedance' in result:
            print(f"差分阻抗: {result['differential_impedance']} Ω")
        if 'common_mode_impedance' in result:
            print(f"共模阻抗: {result['common_mode_impedance']} Ω")
        if 'single_ended_impedance' in result:
            print(f"单端阻抗: {result['single_ended_impedance']} Ω")
        
        # 耦合参数
        if 'coupling_coefficient' in result:
            print(f"耦合系数: {result['coupling_coefficient']}")
        if 'coupling_factor' in result:
            print(f"耦合因子: {result['coupling_factor']}")
        if 'ground_coupling' in result:
            print(f"地线耦合: {result['ground_coupling']}")
        
        # 介电参数
        if 'er_eff' in result:
            print(f"有效介电常数: {result['er_eff']}")
        if 'h_eff' in result:
            print(f"等效厚度: {result['h_eff']} mm")
        
        # 其他参数
        if 'offset_factor' in result:
            print(f"偏移修正系数: {result['offset_factor']}")
        if 'upper_distance' in result:
            print(f"上层距离: {result['upper_distance']} mm")
        if 'lower_distance' in result:
            print(f"下层距离: {result['lower_distance']} mm")
        if 'k_parameter' in result:
            print(f"K参数: {result['k_parameter']}")
            
    else:
        print(f"❌ 错误: {result['message']}")

def main():
    """主测试函数"""
    
    calculator = PCBImpedanceCalculator()
    
    print_separator("扩展传输线结构测试")
    
    # 1. GSSG结构测试
    print_separator("GSSG (Ground-Signal-Signal-Ground) 结构")
    
    # 100Ω GSSG差分对
    result1 = calculator.gssg_impedance(
        w=0.1, s=0.15, g=0.2, h=0.2, t=0.035, er=4.3
    )
    print_result("100Ω GSSG差分对 (典型高速设计)", result1)
    
    # 90Ω GSSG差分对 (HDMI)
    result2 = calculator.gssg_impedance(
        w=0.075, s=0.1, g=0.15, h=0.15, t=0.035, er=4.1
    )
    print_result("90Ω GSSG差分对 (HDMI应用)", result2)
    
    # 2. 嵌入式微带线测试
    print_separator("嵌入式微带线 (多层介质)")
    
    # 混合材料设计
    result3 = calculator.embedded_microstrip_impedance(
        w=0.2, h1=0.1, h2=0.15, t=0.035, er1=3.3, er2=4.3
    )
    print_result("混合材料微带线 (上层低εr)", result3)
    
    # 空气层设计
    result4 = calculator.embedded_microstrip_impedance(
        w=0.15, h1=0.05, h2=0.2, t=0.035, er1=1.0, er2=4.3
    )
    print_result("空气层微带线设计", result4)
    
    # 3. 偏移带状线测试
    print_separator("偏移带状线 (非对称结构)")
    
    # 偏向上层
    result5 = calculator.offset_stripline_impedance(
        w=0.12, h=0.4, b=0.3, t=0.035, er=4.3
    )
    print_result("偏向上层带状线", result5)
    
    # 偏向下层
    result6 = calculator.offset_stripline_impedance(
        w=0.12, h=0.4, b=0.1, t=0.035, er=4.3
    )
    print_result("偏向下层带状线", result6)
    
    # 4. 接地共面波导测试
    print_separator("接地共面波导 (GCPW)")
    
    # 50Ω GCPW
    result7 = calculator.grounded_coplanar_waveguide_impedance(
        w=0.2, s=0.1, h=0.2, t=0.035, er=4.3
    )
    print_result("50Ω GCPW (FR4基材)", result7)
    
    # 75Ω GCPW (RF应用)
    result8 = calculator.grounded_coplanar_waveguide_impedance(
        w=0.15, s=0.15, h=0.254, t=0.017, er=3.38
    )
    print_result("75Ω GCPW (Rogers材料)", result8)
    
    # 5. 宽边耦合带状线测试
    print_separator("宽边耦合带状线 (垂直耦合)")
    
    # 100Ω宽边耦合
    result9 = calculator.broadside_coupled_stripline_impedance(
        w=0.15, h=0.2, s=0.1, t=0.035, er=4.3
    )
    print_result("100Ω宽边耦合带状线", result9)
    
    # 紧耦合设计
    result10 = calculator.broadside_coupled_stripline_impedance(
        w=0.2, h=0.15, s=0.05, t=0.035, er=4.3
    )
    print_result("紧耦合宽边带状线", result10)
    
    # 6. 结构对比分析
    print_separator("不同结构阻抗对比")
    
    print("\n📈 相同参数下不同结构的阻抗对比:")
    print("基本参数: W=0.15mm, H=0.2mm, T=0.035mm, εr=4.3")
    print("-" * 50)
    
    # 微带线
    microstrip = calculator.microstrip_impedance(0.15, 0.2, 0.035, 4.3)
    if microstrip['status'] == 'success':
        print(f"微带线:     {microstrip['impedance']:6.1f} Ω")
    
    # 带状线
    stripline = calculator.stripline_impedance(0.15, 0.4, 0.035, 4.3)
    if stripline['status'] == 'success':
        print(f"带状线:     {stripline['impedance']:6.1f} Ω")
    
    # 差分对
    differential = calculator.differential_impedance(0.15, 0.15, 0.2, 0.035, 4.3)
    if differential['status'] == 'success':
        print(f"差分对:     {differential['differential_impedance']:6.1f} Ω (差分)")
        print(f"           {differential['single_ended_impedance']:6.1f} Ω (单端)")
    
    # GSSG
    gssg = calculator.gssg_impedance(0.15, 0.15, 0.2, 0.2, 0.035, 4.3)
    if gssg['status'] == 'success':
        print(f"GSSG:       {gssg['differential_impedance']:6.1f} Ω (差分)")
        print(f"           {gssg['common_mode_impedance']:6.1f} Ω (共模)")
    
    # GCPW
    gcpw = calculator.grounded_coplanar_waveguide_impedance(0.15, 0.1, 0.2, 0.035, 4.3)
    if gcpw['status'] == 'success':
        print(f"GCPW:       {gcpw['impedance']:6.1f} Ω")
    
    # 7. 应用场景推荐
    print_separator("应用场景推荐")
    
    scenarios = [
        {
            'name': '高速数字信号 (DDR4/5)',
            'structure': 'GSSG差分对',
            'impedance': '100Ω差分',
            'advantages': ['优秀信号隔离', '减少串扰', '良好SI性能']
        },
        {
            'name': 'RF/微波应用',
            'structure': 'GCPW',
            'impedance': '50Ω/75Ω',
            'advantages': ['宽带特性', '低损耗', '易于测试']
        },
        {
            'name': '高密度设计',
            'structure': '宽边耦合',
            'impedance': '100Ω差分',
            'advantages': ['节省面积', '紧密耦合', '垂直布线']
        },
        {
            'name': '多层混合设计',
            'structure': '嵌入式微带线',
            'impedance': '50Ω单端',
            'advantages': ['材料优化', '性能定制', '成本控制']
        },
        {
            'name': '层叠受限设计',
            'structure': '偏移带状线',
            'impedance': '50Ω单端',
            'advantages': ['灵活布局', '适应约束', '工艺优化']
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 {scenario['name']}:")
        print(f"   推荐结构: {scenario['structure']}")
        print(f"   目标阻抗: {scenario['impedance']}")
        print(f"   主要优势: {', '.join(scenario['advantages'])}")

def test_parameter_sensitivity():
    """测试参数敏感性"""
    
    print_separator("参数敏感性分析")
    
    calculator = PCBImpedanceCalculator()
    
    print("\n📊 GSSG结构参数敏感性 (基准: W=0.1, S=0.15, G=0.2, H=0.2, εr=4.3):")
    print("-" * 60)
    
    base_params = {'w': 0.1, 's': 0.15, 'g': 0.2, 'h': 0.2, 't': 0.035, 'er': 4.3}
    base_result = calculator.gssg_impedance(**base_params)
    
    if base_result['status'] == 'success':
        base_z_diff = base_result['differential_impedance']
        print(f"基准差分阻抗: {base_z_diff:.1f} Ω")
        print()
        
        # 测试线宽变化
        print("线宽变化影响:")
        for w_factor in [0.8, 0.9, 1.0, 1.1, 1.2]:
            params = base_params.copy()
            params['w'] = base_params['w'] * w_factor
            result = calculator.gssg_impedance(**params)
            if result['status'] == 'success':
                change = (result['differential_impedance'] - base_z_diff) / base_z_diff * 100
                print(f"  W×{w_factor}: {result['differential_impedance']:5.1f} Ω ({change:+5.1f}%)")
        
        # 测试信号间距变化
        print("\n信号间距变化影响:")
        for s_factor in [0.8, 0.9, 1.0, 1.1, 1.2]:
            params = base_params.copy()
            params['s'] = base_params['s'] * s_factor
            result = calculator.gssg_impedance(**params)
            if result['status'] == 'success':
                change = (result['differential_impedance'] - base_z_diff) / base_z_diff * 100
                print(f"  S×{s_factor}: {result['differential_impedance']:5.1f} Ω ({change:+5.1f}%)")
        
        # 测试地线间距变化
        print("\n地线间距变化影响:")
        for g_factor in [0.8, 0.9, 1.0, 1.1, 1.2]:
            params = base_params.copy()
            params['g'] = base_params['g'] * g_factor
            result = calculator.gssg_impedance(**params)
            if result['status'] == 'success':
                change = (result['differential_impedance'] - base_z_diff) / base_z_diff * 100
                print(f"  G×{g_factor}: {result['differential_impedance']:5.1f} Ω ({change:+5.1f}%)")

if __name__ == "__main__":
    main()
    test_parameter_sensitivity()
    
    print_separator("测试完成")
    print("\n🎯 新增传输线结构功能:")
    print("✅ GSSG (Ground-Signal-Signal-Ground)")
    print("✅ 嵌入式微带线 (多层介质)")
    print("✅ 偏移带状线 (非对称)")
    print("✅ 接地共面波导 (GCPW)")
    print("✅ 宽边耦合带状线 (垂直耦合)")
    
    print("\n🌐 启动Web应用测试这些新功能:")
    print("   python app.py")
    print("   浏览器访问: http://127.0.0.1:5000")