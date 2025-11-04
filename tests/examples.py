"""
PCB阻抗计算器 - 常用设计示例和验证脚本
"""

from lala.PCB_board_Res.src.app import PCBImpedanceCalculator
import json

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
        if 'impedance' in result:
            print(f"特征阻抗: {result['impedance']} Ω")
        if 'er_eff' in result:
            print(f"有效介电常数: {result['er_eff']}")
        if 'differential_impedance' in result:
            print(f"差分阻抗: {result['differential_impedance']} Ω")
            print(f"单端阻抗: {result['single_ended_impedance']} Ω") 
            print(f"耦合系数: {result['coupling_coefficient']}")
    else:
        print(f"❌ 错误: {result['message']}")

def main():
    """主函数 - 运行各种设计示例"""
    
    calculator = PCBImpedanceCalculator()
    
    print_separator("PCB阻抗计算器 - 设计示例验证")
    
    # 1. 微带线设计示例
    print_separator("微带线设计示例")
    
    # 50Ω微带线 (FR4, 0.2mm厚度)
    result1 = calculator.microstrip_impedance(
        w=0.254, h=0.2, t=0.035, er=4.3, loss_tangent=0.02
    )
    print_result("50Ω微带线 (FR4, H=0.2mm)", result1)
    
    # 50Ω微带线 (FR4, 0.1mm厚度)  
    result2 = calculator.microstrip_impedance(
        w=0.127, h=0.1, t=0.035, er=4.3
    )
    print_result("50Ω微带线 (FR4, H=0.1mm)", result2)
    
    # 75Ω微带线 (Rogers 4003C)
    result3 = calculator.microstrip_impedance(
        w=0.2, h=0.2, t=0.035, er=3.38
    )
    print_result("75Ω微带线 (Rogers 4003C)", result3)
    
    # 2. 带状线设计示例
    print_separator("带状线设计示例")
    
    # 50Ω带状线
    result4 = calculator.stripline_impedance(
        w=0.15, h=0.4, t=0.035, er=4.3
    )
    print_result("50Ω带状线 (FR4, H=0.4mm)", result4)
    
    # 100Ω带状线
    result5 = calculator.stripline_impedance(
        w=0.05, h=0.2, t=0.035, er=4.3
    )
    print_result("100Ω带状线 (FR4, H=0.2mm)", result5)
    
    # 3. 差分对设计示例
    print_separator("差分对设计示例")
    
    # 100Ω差分对 (USB)
    result6 = calculator.differential_impedance(
        w=0.127, s=0.127, h=0.2, t=0.035, er=4.3
    )
    print_result("100Ω差分对 - USB信号", result6)
    
    # 90Ω差分对 (HDMI)
    result7 = calculator.differential_impedance(
        w=0.1, s=0.1, h=0.15, t=0.035, er=4.1
    )
    print_result("90Ω差分对 - HDMI信号", result7)
    
    # 100Ω差分对 (以太网)
    result8 = calculator.differential_impedance(
        w=0.15, s=0.15, h=0.25, t=0.035, er=4.3
    )
    print_result("100Ω差分对 - 以太网信号", result8)
    
    # 4. 同轴线设计示例
    print_separator("同轴线设计示例")
    
    # 50Ω同轴线 (RG-58)
    result9 = calculator.coaxial_impedance(
        inner_diameter=0.9, outer_diameter=2.95, er=2.25
    )
    print_result("50Ω同轴线 (RG-58型)", result9)
    
    # 75Ω同轴线 (RG-6)
    result10 = calculator.coaxial_impedance(
        inner_diameter=1.024, outer_diameter=4.57, er=2.25
    )
    print_result("75Ω同轴线 (RG-6型)", result10)
    
    # 50Ω同轴线 (RG-174)
    result11 = calculator.coaxial_impedance(
        inner_diameter=0.48, outer_diameter=1.52, er=2.25
    )
    print_result("50Ω同轴线 (RG-174型)", result11)
    
    # 5. 高频设计示例
    print_separator("高频设计示例")
    
    # Rogers材料微带线
    result12 = calculator.microstrip_impedance(
        w=0.3, h=0.254, t=0.017, er=3.38, loss_tangent=0.0027
    )
    print_result("50Ω微带线 (Rogers 4003C, 10mil)", result12)
    
    # Teflon基材
    result13 = calculator.microstrip_impedance(
        w=0.5, h=0.5, t=0.035, er=2.1, loss_tangent=0.0002
    )
    print_result("50Ω微带线 (Teflon基材)", result13)
    
    # 6. 设计参数对比
    print_separator("设计参数影响分析")
    
    print("\n📈 线宽对阻抗的影响 (微带线, H=0.2mm, FR4):")
    widths = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    for w in widths:
        result = calculator.microstrip_impedance(w=w, h=0.2, t=0.035, er=4.3)
        if result['status'] == 'success':
            print(f"  W={w:0.2f}mm -> Z₀={result['impedance']:0.1f}Ω")
    
    print("\n📈 介质厚度对阻抗的影响 (微带线, W=0.2mm, FR4):")
    heights = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    for h in heights:
        result = calculator.microstrip_impedance(w=0.2, h=h, t=0.035, er=4.3)
        if result['status'] == 'success':
            print(f"  H={h:0.2f}mm -> Z₀={result['impedance']:0.1f}Ω")
    
    print("\n📈 介电常数对阻抗的影响 (微带线, W=0.2mm, H=0.2mm):")
    dielectrics = [2.1, 2.5, 3.0, 3.5, 4.0, 4.3, 4.5, 5.0]
    for er in dielectrics:
        result = calculator.microstrip_impedance(w=0.2, h=0.2, t=0.035, er=er)
        if result['status'] == 'success':
            print(f"  εᵣ={er:0.1f} -> Z₀={result['impedance']:0.1f}Ω")

def validate_common_impedances():
    """验证常用阻抗值的设计"""
    
    print_separator("常用阻抗验证")
    
    calculator = PCBImpedanceCalculator()
    
    # 目标阻抗值和容差
    targets = [
        {"name": "50Ω单端", "target": 50, "tolerance": 5},
        {"name": "75Ω视频", "target": 75, "tolerance": 5},
        {"name": "100Ω差分", "target": 100, "tolerance": 10},
        {"name": "90Ω差分", "target": 90, "tolerance": 10}
    ]
    
    print("\n✅ 阻抗验证结果:")
    print("=" * 50)
    
    # 50Ω微带线验证
    result_50 = calculator.microstrip_impedance(w=0.254, h=0.2, t=0.035, er=4.3)
    if result_50['status'] == 'success':
        impedance = result_50['impedance']
        error = abs(impedance - 50) / 50 * 100
        status = "✅ PASS" if error <= 10 else "❌ FAIL"
        print(f"50Ω微带线: {impedance:0.1f}Ω (误差: {error:0.1f}%) {status}")
    
    # 100Ω差分对验证  
    result_100 = calculator.differential_impedance(w=0.127, s=0.127, h=0.2, t=0.035, er=4.3)
    if result_100['status'] == 'success':
        impedance = result_100['differential_impedance']
        error = abs(impedance - 100) / 100 * 100
        status = "✅ PASS" if error <= 15 else "❌ FAIL"
        print(f"100Ω差分对: {impedance:0.1f}Ω (误差: {error:0.1f}%) {status}")
    
    # 75Ω同轴线验证
    result_75 = calculator.coaxial_impedance(inner_diameter=1.024, outer_diameter=4.57, er=2.25)
    if result_75['status'] == 'success':
        impedance = result_75['impedance']
        error = abs(impedance - 75) / 75 * 100  
        status = "✅ PASS" if error <= 5 else "❌ FAIL"
        print(f"75Ω同轴线: {impedance:0.1f}Ω (误差: {error:0.1f}%) {status}")

if __name__ == "__main__":
    main()
    validate_common_impedances()
    
    print_separator("验证完成")
    print("\n🎯 如需运行Web应用，请执行: python app.py")
    print("🌐 然后访问: http://localhost:5000")
    print("\n📚 更多信息请查看 README.md 文件")