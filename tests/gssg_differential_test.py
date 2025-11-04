"""
修正后的GSSG CPWG测试 - G-S-S-G差分对结构
测试正确的GSSG结构：Ground-Signal-Signal-Ground (两个信号线)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import PCBImpedanceCalculator
import json

def print_separator(title):
    """打印分隔符"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_result(description, result):
    """格式化打印结果"""
    print(f"\n📊 {description}")
    print("-" * 50)
    
    if result['status'] == 'success':
        if 'differential_impedance' in result:
            print(f"差分阻抗: {result['differential_impedance']} Ω")
        if 'single_ended_impedance' in result:
            print(f"单端阻抗: {result['single_ended_impedance']} Ω")
        if 'common_mode_impedance' in result:
            print(f"共模阻抗: {result['common_mode_impedance']} Ω")
        if 'odd_mode_impedance' in result:
            print(f"奇模阻抗: {result['odd_mode_impedance']} Ω")
        if 'even_mode_impedance' in result:
            print(f"偶模阻抗: {result['even_mode_impedance']} Ω")
        if 'er_eff' in result:
            print(f"有效介电常数: {result['er_eff']}")
        if 'coupling_coefficient' in result:
            print(f"耦合系数: {result['coupling_coefficient']}")
        if 'filling_factor' in result:
            print(f"填充因子: {result['filling_factor']}")
        if 'conductor_loss' in result and result['conductor_loss']:
            print(f"导体损耗: {result['conductor_loss']} dB/cm")
        if 'dielectric_loss' in result:
            print(f"介质损耗: {result['dielectric_loss']} dB/cm")
    else:
        print(f"❌ 错误: {result['message']}")

def test_gssg_cpwg_differential():
    """测试GSSG CPWG差分对计算功能"""
    
    print_separator("GSSG CPWG差分对测试 (G-S-S-G结构)")
    
    calculator = PCBImpedanceCalculator()
    
    print("🔍 GSSG结构说明:")
    print("   G-S-S-G = Ground-Signal-Signal-Ground")
    print("   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐")
    print("   │  G  │ │ S1  │ │ S2  │ │  G  │")
    print("   └─────┘ └─────┘ └─────┘ └─────┘")
    print("   两个信号线S1和S2组成差分对")
    
    # 1. 100Ω差分对 GSSG CPWG设计
    result1 = calculator.cpwg_impedance(
        w=0.1, s=0.1, h=0.2, t=0.035, er=4.3
    )
    print_result("100Ω差分对 GSSG CPWG (FR4)", result1)
    
    # 2. 90Ω差分对 (HDMI标准)
    result2 = calculator.cpwg_impedance(
        w=0.12, s=0.08, h=0.15, t=0.035, er=4.1
    )
    print_result("90Ω差分对 GSSG CPWG (HDMI)", result2)
    
    # 3. 85Ω差分对 (PCIe标准)  
    result3 = calculator.cpwg_impedance(
        w=0.15, s=0.1, h=0.2, t=0.035, er=4.3
    )
    print_result("85Ω差分对 GSSG CPWG (PCIe)", result3)
    
    # 4. 高频Rogers材料
    result4 = calculator.cpwg_impedance(
        w=0.2, s=0.15, h=0.254, t=0.017, er=3.38
    )
    print_result("100Ω差分对 GSSG (Rogers 4003C)", result4)

def test_gssg_vs_normal_differential():
    """比较GSSG CPWG与普通差分对的差异"""
    
    print_separator("GSSG CPWG vs 普通差分对对比")
    
    calculator = PCBImpedanceCalculator()
    
    # 相同参数
    params = {'w': 0.1, 's': 0.1, 'h': 0.2, 't': 0.035, 'er': 4.3}
    
    # GSSG CPWG差分对
    gssg_result = calculator.cpwg_impedance(**params)
    print_result("GSSG CPWG差分对", gssg_result)
    
    # 普通差分对 (微带线)
    normal_result = calculator.differential_impedance(**params)
    print_result("普通差分对 (微带线)", normal_result)
    
    if gssg_result['status'] == 'success' and normal_result['status'] == 'success':
        gssg_diff = gssg_result['differential_impedance']
        normal_diff = normal_result['differential_impedance']
        diff = abs(gssg_diff - normal_diff)
        print(f"\n📈 差分阻抗差异: {diff:.2f}Ω")
        print(f"GSSG相比普通差分对的变化: {(gssg_diff - normal_diff)/normal_diff*100:+.1f}%")

def test_gssg_parameter_analysis():
    """GSSG CPWG参数影响分析"""
    
    print_separator("GSSG CPWG参数影响分析")
    
    calculator = PCBImpedanceCalculator()
    
    print("\n📈 信号线宽对GSSG差分阻抗的影响 (S=0.1mm, H=0.2mm, FR4):")
    widths = [0.05, 0.08, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3]
    for w in widths:
        result = calculator.cpwg_impedance(w=w, s=0.1, h=0.2, t=0.035, er=4.3)
        if result['status'] == 'success':
            print(f"  W={w:0.2f}mm -> Z_diff={result['differential_impedance']:0.1f}Ω, Z_se={result['single_ended_impedance']:0.1f}Ω")
    
    print("\n📈 信号线间距对GSSG差分阻抗的影响 (W=0.1mm, H=0.2mm, FR4):")
    spacings = [0.05, 0.08, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3]
    for s in spacings:
        result = calculator.cpwg_impedance(w=0.1, s=s, h=0.2, t=0.035, er=4.3)
        if result['status'] == 'success':
            print(f"  S={s:0.2f}mm -> Z_diff={result['differential_impedance']:0.1f}Ω, 耦合={result['coupling_coefficient']:0.3f}")
    
    print("\n📈 介质厚度对GSSG差分阻抗的影响 (W=0.1mm, S=0.1mm, FR4):")
    heights = [0.1, 0.15, 0.2, 0.254, 0.3, 0.4, 0.5]
    for h in heights:
        result = calculator.cpwg_impedance(w=0.1, s=0.1, h=h, t=0.035, er=4.3)
        if result['status'] == 'success':
            print(f"  H={h:0.3f}mm -> Z_diff={result['differential_impedance']:0.1f}Ω, εr_eff={result['er_eff']:0.3f}")

def test_gssg_target_impedances():
    """测试目标差分阻抗的GSSG设计"""
    
    print_separator("常用差分阻抗的GSSG设计验证")
    
    calculator = PCBImpedanceCalculator()
    
    # 目标阻抗设计案例
    test_cases = [
        {
            'name': '100Ω USB差分对',
            'params': {'w': 0.1, 's': 0.1, 'h': 0.2, 't': 0.035, 'er': 4.3},
            'target': 100,
            'tolerance': 15
        },
        {
            'name': '90Ω HDMI差分对', 
            'params': {'w': 0.12, 's': 0.08, 'h': 0.15, 't': 0.035, 'er': 4.1},
            'target': 90,
            'tolerance': 15
        },
        {
            'name': '85Ω PCIe差分对',
            'params': {'w': 0.15, 's': 0.1, 'h': 0.2, 't': 0.035, 'er': 4.3},
            'target': 85,
            'tolerance': 15
        },
        {
            'name': '120Ω以太网差分对',
            'params': {'w': 0.08, 's': 0.15, 'h': 0.25, 't': 0.035, 'er': 4.3},
            'target': 120,
            'tolerance': 20
        }
    ]
    
    print("\n✅ 目标阻抗验证结果:")
    print("=" * 70)
    
    for case in test_cases:
        result = calculator.cpwg_impedance(**case['params'])
        if result['status'] == 'success':
            diff_impedance = result['differential_impedance']
            target = case['target']
            error = abs(diff_impedance - target) / target * 100
            status = "✅ PASS" if error <= case['tolerance'] else "❌ FAIL"
            print(f"{case['name']:20}: {diff_impedance:5.1f}Ω (目标:{target}Ω, 误差:{error:4.1f}%) {status}")
        else:
            print(f"{case['name']:20}: ❌ 计算失败")

def test_gssg_high_frequency():
    """高频材料GSSG性能测试"""
    
    print_separator("高频材料GSSG性能对比")
    
    calculator = PCBImpedanceCalculator()
    
    materials = {
        'FR4标准': {'er': 4.3, 'name': 'FR4 标准'},
        'FR4高频': {'er': 4.1, 'name': 'FR4 高频'},
        'Rogers4003C': {'er': 3.38, 'name': 'Rogers 4003C'},
        'Rogers4350B': {'er': 3.48, 'name': 'Rogers 4350B'}, 
        'Teflon': {'er': 2.1, 'name': 'Teflon/PTFE'},
        'Polyimide': {'er': 3.4, 'name': 'Polyimide'}
    }
    
    print("\n100Ω差分对GSSG设计 (W=0.1mm, S=0.1mm, H=0.2mm):")
    print("=" * 65)
    print(f"{'材料':15} {'εr':>6} {'Z_diff':>8} {'Z_se':>8} {'εr_eff':>8} {'耦合':>8}")
    print("=" * 65)
    
    for key, material in materials.items():
        result = calculator.cpwg_impedance(
            w=0.1, s=0.1, h=0.2, t=0.035, er=material['er']
        )
        if result['status'] == 'success':
            print(f"{material['name']:15} {material['er']:6.2f} {result['differential_impedance']:8.1f} {result['single_ended_impedance']:8.1f} {result['er_eff']:8.3f} {result['coupling_coefficient']:8.3f}")

def main():
    """主测试函数"""
    
    print("🔧 修正后的GSSG CPWG差分对测试")
    print("G-S-S-G = Ground-Signal-Signal-Ground (两个信号线)")
    print("=" * 70)
    
    try:
        test_gssg_cpwg_differential()
        test_gssg_vs_normal_differential()
        test_gssg_parameter_analysis()
        test_gssg_target_impedances()
        test_gssg_high_frequency()
        
        print_separator("测试完成")
        print("\n🎯 GSSG CPWG差分对功能测试成功！")
        print("📱 启动Web应用: python app.py")
        print("🌐 访问地址: http://localhost:5000") 
        print("🔍 选择: CPWG共面波导 (CPWG-GSSG)")
        print("📝 输入: W=信号线宽, S=信号线间距")
        print("📊 结果: 差分阻抗、单端阻抗、奇偶模阻抗等")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()