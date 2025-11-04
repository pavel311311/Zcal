"""
CPWG (Coplanar Waveguide with Ground) 阻抗计算测试
测试新增的GSSG结构CPWG阻抗计算功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lala.PCB_board_Res.src.app import PCBImpedanceCalculator
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
        print(f"特征阻抗: {result['impedance']} Ω")
        if 'er_eff' in result:
            print(f"有效介电常数: {result['er_eff']}")
        if 'filling_factor' in result:
            print(f"填充因子: {result['filling_factor']}")
        if 'k_parameter' in result:
            print(f"K参数: {result['k_parameter']}")
        if 'ground_correction' in result:
            print(f"接地修正系数: {result['ground_correction']}")
        if 'conductor_loss' in result and result['conductor_loss']:
            print(f"导体损耗: {result['conductor_loss']} dB/cm")
        if 'dielectric_loss' in result:
            print(f"介质损耗: {result['dielectric_loss']} dB/cm")
    else:
        print(f"❌ 错误: {result['message']}")

def test_cpwg_calculations():
    """测试CPWG计算功能"""
    
    print_separator("CPWG (Coplanar Waveguide with Ground) 测试")
    
    calculator = PCBImpedanceCalculator()
    
    # 1. 50Ω CPWG设计 (RF应用)
    result1 = calculator.cpwg_impedance(
        w=0.3, s=0.2, h=0.254, t=0.035, er=4.3
    )
    print_result("50Ω CPWG (FR4, H=0.254mm)", result1)
    
    # 2. 75Ω CPWG设计 (射频应用)
    result2 = calculator.cpwg_impedance(
        w=0.2, s=0.3, h=0.254, t=0.035, er=4.3
    )
    print_result("75Ω CPWG (FR4, H=0.254mm)", result2)
    
    # 3. 高频CPWG (Rogers材料)
    result3 = calculator.cpwg_impedance(
        w=0.4, s=0.25, h=0.508, t=0.017, er=3.38
    )
    print_result("50Ω CPWG (Rogers 4003C)", result3)
    
    # 4. 窄线宽CPWG (高阻抗)
    result4 = calculator.cpwg_impedance(
        w=0.1, s=0.15, h=0.2, t=0.035, er=4.3
    )
    print_result("高阻抗CPWG (窄线宽)", result4)
    
    # 5. 宽线宽CPWG (低阻抗)
    result5 = calculator.cpwg_impedance(
        w=1.0, s=0.1, h=0.5, t=0.035, er=4.3
    )
    print_result("低阻抗CPWG (宽线宽)", result5)

def test_cpwg_vs_gcpw():
    """比较CPWG和GCPW的差异"""
    
    print_separator("CPWG vs GCPW 对比测试")
    
    calculator = PCBImpedanceCalculator()
    
    # 相同参数下的对比
    params = {'w': 0.3, 's': 0.2, 'h': 0.254, 't': 0.035, 'er': 4.3}
    
    # CPWG计算
    cpwg_result = calculator.cpwg_impedance(**params)
    print_result("CPWG阻抗", cpwg_result)
    
    # GCPW计算 (简化版)
    gcpw_result = calculator.grounded_coplanar_waveguide_impedance(**params)
    print_result("GCPW阻抗", gcpw_result)
    
    if cpwg_result['status'] == 'success' and gcpw_result['status'] == 'success':
        diff = abs(cpwg_result['impedance'] - gcpw_result['impedance'])
        print(f"\n📈 阻抗差异: {diff:.2f}Ω")
        print(f"差异百分比: {diff/cpwg_result['impedance']*100:.1f}%")

def test_cpwg_parameter_effects():
    """测试CPWG参数影响"""
    
    print_separator("CPWG参数影响分析")
    
    calculator = PCBImpedanceCalculator()
    
    print("\n📈 线宽对CPWG阻抗的影响 (S=0.2mm, H=0.254mm, FR4):")
    widths = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
    for w in widths:
        result = calculator.cpwg_impedance(w=w, s=0.2, h=0.254, t=0.035, er=4.3)
        if result['status'] == 'success':
            print(f"  W={w:0.1f}mm -> Z₀={result['impedance']:0.1f}Ω")
    
    print("\n📈 间距对CPWG阻抗的影响 (W=0.3mm, H=0.254mm, FR4):")
    spacings = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    for s in spacings:
        result = calculator.cpwg_impedance(w=0.3, s=s, h=0.254, t=0.035, er=4.3)
        if result['status'] == 'success':
            print(f"  S={s:0.2f}mm -> Z₀={result['impedance']:0.1f}Ω")
    
    print("\n📈 介质厚度对CPWG阻抗的影响 (W=0.3mm, S=0.2mm, FR4):")
    heights = [0.1, 0.15, 0.2, 0.254, 0.3, 0.4, 0.5, 0.8, 1.0]
    for h in heights:
        result = calculator.cpwg_impedance(w=0.3, s=0.2, h=h, t=0.035, er=4.3)
        if result['status'] == 'success':
            print(f"  H={h:0.3f}mm -> Z₀={result['impedance']:0.1f}Ω")

def test_cpwg_materials():
    """测试不同材料的CPWG性能"""
    
    print_separator("不同材料的CPWG性能测试")
    
    calculator = PCBImpedanceCalculator()
    
    materials = {
        'FR4': {'er': 4.3, 'name': 'FR4 标准'},
        'FR4_HF': {'er': 4.1, 'name': 'FR4 高频'},
        'Rogers4003C': {'er': 3.38, 'name': 'Rogers 4003C'},
        'Rogers4350B': {'er': 3.48, 'name': 'Rogers 4350B'},
        'Teflon': {'er': 2.1, 'name': 'Teflon/PTFE'},
        'Polyimide': {'er': 3.4, 'name': 'Polyimide'}
    }
    
    # 固定几何参数，测试不同材料
    w, s, h, t = 0.3, 0.2, 0.254, 0.035
    
    for material_key, material in materials.items():
        result = calculator.cpwg_impedance(w=w, s=s, h=h, t=t, er=material['er'])
        if result['status'] == 'success':
            print(f"{material['name']:15} (εr={material['er']:4.2f}): Z₀={result['impedance']:5.1f}Ω, εr_eff={result['er_eff']:5.3f}")

def test_cpwg_accuracy():
    """验证CPWG计算精度"""
    
    print_separator("CPWG计算精度验证")
    
    calculator = PCBImpedanceCalculator()
    
    # 已知的CPWG设计案例（理论值）
    test_cases = [
        {
            'name': '50Ω标准CPWG',
            'params': {'w': 0.3, 's': 0.2, 'h': 0.254, 't': 0.035, 'er': 4.3},
            'expected': 50,
            'tolerance': 15  # ±15%
        },
        {
            'name': '75Ω射频CPWG',
            'params': {'w': 0.2, 's': 0.3, 'h': 0.254, 't': 0.035, 'er': 4.3},
            'expected': 75,
            'tolerance': 15
        },
        {
            'name': '100Ω高阻抗CPWG',
            'params': {'w': 0.1, 's': 0.4, 'h': 0.254, 't': 0.035, 'er': 4.3},
            'expected': 100,
            'tolerance': 20
        }
    ]
    
    print("\n✅ 精度验证结果:")
    print("=" * 60)
    
    for case in test_cases:
        result = calculator.cpwg_impedance(**case['params'])
        if result['status'] == 'success':
            impedance = result['impedance']
            expected = case['expected']
            error = abs(impedance - expected) / expected * 100
            status = "✅ PASS" if error <= case['tolerance'] else "❌ FAIL"
            print(f"{case['name']:20}: {impedance:5.1f}Ω (期望:{expected}Ω, 误差:{error:4.1f}%) {status}")
        else:
            print(f"{case['name']:20}: ❌ 计算失败 - {result['message']}")

def main():
    """主测试函数"""
    
    print("🔧 CPWG (Coplanar Waveguide with Ground) 完整测试")
    print("=" * 70)
    
    try:
        test_cpwg_calculations()
        test_cpwg_vs_gcpw()
        test_cpwg_parameter_effects()
        test_cpwg_materials()
        test_cpwg_accuracy()
        
        print_separator("测试完成")
        print("\n🎯 CPWG功能测试成功！")
        print("📱 启动Web应用: python app.py")
        print("🌐 访问地址: http://localhost:5000")
        print("🔍 选择计算类型: CPWG共面波导 (CPWG-GSSG)")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()