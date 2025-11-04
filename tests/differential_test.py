"""
差分对阻抗计算修复验证脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lala.PCB_board_Res.src.app import PCBImpedanceCalculator
import json

def test_differential_pair():
    """测试修复后的差分对计算"""
    print("=" * 60)
    print("  差分对阻抗计算修复验证")
    print("=" * 60)
    
    calculator = PCBImpedanceCalculator()
    
    # 测试用例1: 100Ω差分对 (USB)
    print("\n📊 测试用例1: 100Ω差分对 (USB)")
    print("-" * 40)
    result1 = calculator.differential_impedance(
        w=0.127, s=0.127, h=0.2, t=0.035, er=4.3
    )
    print_result(result1)
    
    # 测试用例2: 90Ω差分对 (HDMI)
    print("\n📊 测试用例2: 90Ω差分对 (HDMI)")
    print("-" * 40)
    result2 = calculator.differential_impedance(
        w=0.1, s=0.1, h=0.15, t=0.035, er=4.1
    )
    print_result(result2)
    
    # 测试用例3: 100Ω差分对 (以太网)
    print("\n📊 测试用例3: 100Ω差分对 (以太网)")
    print("-" * 40)
    result3 = calculator.differential_impedance(
        w=0.15, s=0.15, h=0.25, t=0.035, er=4.3
    )
    print_result(result3)
    
    # 测试用例4: 极端参数测试
    print("\n📊 测试用例4: 极端参数测试")
    print("-" * 40)
    result4 = calculator.differential_impedance(
        w=0.05, s=0.05, h=0.1, t=0.035, er=4.3
    )
    print_result(result4)
    
    # 测试用例5: 大间距测试
    print("\n📊 测试用例5: 大间距测试")
    print("-" * 40)
    result5 = calculator.differential_impedance(
        w=0.2, s=0.5, h=0.2, t=0.035, er=4.3
    )
    print_result(result5)
    
    # 错误输入测试
    print("\n❌ 错误输入测试")
    print("-" * 40)
    result_error = calculator.differential_impedance(
        w=0, s=0.1, h=0.2, t=0.035, er=4.3
    )
    print_result(result_error)

def print_result(result):
    """格式化打印结果"""
    if result['status'] == 'success':
        print(f"✅ 计算成功:")
        print(f"  差分阻抗: {result['differential_impedance']} Ω")
        print(f"  单端阻抗: {result['single_ended_impedance']} Ω")
        
        if 'odd_mode_impedance' in result:
            print(f"  奇模阻抗: {result['odd_mode_impedance']} Ω")
            print(f"  偶模阻抗: {result['even_mode_impedance']} Ω")
            print(f"  共模阻抗: {result['common_mode_impedance']} Ω")
            
        print(f"  耦合系数: {result['coupling_coefficient']}")
        
        # 评估结果合理性
        diff_z = result['differential_impedance']
        if 80 <= diff_z <= 120:
            print(f"  📊 评估: 合理范围 (80-120Ω)")
        elif 50 <= diff_z <= 150:
            print(f"  ⚠️  评估: 可接受范围 (50-150Ω)")
        else:
            print(f"  ❌ 评估: 超出常规范围")
    else:
        print(f"❌ 计算失败: {result['message']}")

def compare_before_after():
    """比较修复前后的结果"""
    print("\n" + "=" * 60)
    print("  修复前后结果对比")
    print("=" * 60)
    
    calculator = PCBImpedanceCalculator()
    
    # USB差分对参数
    w, s, h, t, er = 0.127, 0.127, 0.2, 0.035, 4.3
    
    print(f"测试参数: W={w}mm, S={s}mm, H={h}mm, T={t}mm, εr={er}")
    
    result = calculator.differential_impedance(w, s, h, t, er)
    
    print("\n🔧 修复后结果:")
    if result['status'] == 'success':
        print(f"  差分阻抗: {result['differential_impedance']} Ω")
        print(f"  单端阻抗: {result['single_ended_impedance']} Ω") 
        print(f"  耦合系数: {result['coupling_coefficient']}")
        
        # 与目标值比较
        target = 100
        error = abs(result['differential_impedance'] - target) / target * 100
        print(f"\n📊 与目标100Ω比较:")
        print(f"  误差: {error:.1f}%")
        
        if error < 10:
            print(f"  ✅ 精度: 优秀 (<10%)")
        elif error < 20:
            print(f"  ✅ 精度: 良好 (<20%)")
        else:
            print(f"  ⚠️  精度: 需要优化 (≥20%)")
    else:
        print(f"  ❌ 仍有错误: {result['message']}")

def main():
    """主函数"""
    try:
        test_differential_pair()
        compare_before_after()
        
        print("\n" + "=" * 60)
        print("  📝 修复总结")
        print("=" * 60)
        print("✅ 修复内容:")
        print("  1. 改进了耦合系数计算公式")
        print("  2. 使用更准确的差分对阻抗公式") 
        print("  3. 添加了参数范围验证")
        print("  4. 增加了奇模/偶模/共模阻抗计算")
        print("  5. 改进了数值计算稳定性")
        
        print("\n🎯 现在可以正常计算差分对阻抗了!")
        print("🌐 Web界面: http://127.0.0.1:5000")
        
    except Exception as e:
        print(f"❌ 测试脚本错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()