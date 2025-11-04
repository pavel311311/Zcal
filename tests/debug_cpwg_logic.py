#!/usr/bin/env python3
"""
CPWG间距S对阻抗影响的逻辑验证测试
验证间距S增大时，阻抗应该增大，而不是减小
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lala.PCB_board_Res.src.app import PCBImpedanceCalculator

def test_spacing_logic():
    """测试间距S对阻抗的逻辑影响"""
    print("🔍 测试CPWG间距S对阻抗的影响")
    print("理论预期：间距S增大 → 耦合减弱 → 差分阻抗增大")
    print("=" * 60)
    
    calculator = PCBImpedanceCalculator()
    
    # 固定其他参数，只改变间距S
    base_params = {
        'w': 0.1,      # 信号线宽
        'h': 0.2,      # 介质厚度  
        't': 0.035,    # 铜厚
        'er': 4.3,     # FR4
        'g': 0.1,      # 信号到地间距
        'gw': 0.3      # 地线宽度
    }
    
    # 测试不同的间距S值
    s_values = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    
    print("\n间距S变化对阻抗的影响:")
    print("S(mm)  | Z_diff(Ω) | Z_single(Ω) | 耦合系数 | 变化趋势")
    print("-" * 55)
    
    prev_z_diff = None
    
    for s in s_values:
        params = base_params.copy()
        params['s'] = s
        
        result = calculator.cpwg_impedance(**params)
        
        if result['status'] == 'success':
            z_diff = result['differential_impedance']
            z_single = result['single_ended_impedance'] 
            coupling = result['coupling_coefficient']
            
            # 判断变化趋势
            if prev_z_diff is not None:
                if z_diff > prev_z_diff:
                    trend = "↗️ 正确"
                elif z_diff < prev_z_diff:
                    trend = "⬇️ 错误!"
                else:
                    trend = "→ 不变"
            else:
                trend = "起始"
            
            print(f"{s:0.2f}  | {z_diff:7.1f}  | {z_single:8.1f}   | {coupling:8.3f} | {trend}")
            
            prev_z_diff = z_diff
        else:
            print(f"{s:0.2f}  | 计算失败: {result['message']}")
    
    print("\n🎯 物理意义分析:")
    print("✅ 正确逻辑: S↗ → 耦合↘ → Z_diff↗")  
    print("❌ 错误逻辑: S↗ → Z_diff↘ (违反物理定律)")

def analyze_coupling_formula():
    """分析耦合系数的计算公式"""
    print("\n🔬 分析当前耦合系数计算公式")
    print("=" * 60)
    
    calculator = PCBImpedanceCalculator()
    
    # 读取当前算法中的耦合计算
    import math
    
    # 模拟当前算法的参数
    w, s, h = 0.1, 0.15, 0.2
    w_eff = w + 0.035 * (1 + math.log(4 * h / 0.035)) / math.pi
    
    print(f"当前参数: W={w}mm, S={s}mm, H={h}mm")
    print(f"有效宽度: W_eff={w_eff:.4f}mm")
    
    # 检查椭圆积分k值的计算
    print("\n🔍 椭圆积分k值检查:")
    
    # 奇模k值
    k_odd = math.tanh(math.pi * w_eff / (4 * h)) / math.tanh(math.pi * (w_eff + s) / (4 * h))
    print(f"k_odd = tanh(π×W_eff/(4×H)) / tanh(π×(W_eff+S)/(4×H))")
    print(f"k_odd = tanh({math.pi * w_eff / (4 * h):.3f}) / tanh({math.pi * (w_eff + s) / (4 * h):.3f})")
    print(f"k_odd = {math.tanh(math.pi * w_eff / (4 * h)):.4f} / {math.tanh(math.pi * (w_eff + s) / (4 * h)):.4f} = {k_odd:.4f}")
    
    # 偶模k值  
    g = 0.1  # 信号到地间距
    k_even = math.tanh(math.pi * w_eff / (2 * h)) / math.tanh(math.pi * (w_eff + g) / (2 * h))
    print(f"\nk_even = tanh(π×W_eff/(2×H)) / tanh(π×(W_eff+G)/(2×H))")
    print(f"k_even = tanh({math.pi * w_eff / (2 * h):.3f}) / tanh({math.pi * (w_eff + g) / (2 * h):.3f})")
    print(f"k_even = {math.tanh(math.pi * w_eff / (2 * h)):.4f} / {math.tanh(math.pi * (w_eff + g) / (2 * h)):.4f} = {k_even:.4f}")
    
    print(f"\n⚠️  问题分析:")
    print(f"S增大时，k_odd应该如何变化？")
    print(f"分子: tanh(π×W_eff/(4×H)) 不变")
    print(f"分母: tanh(π×(W_eff+S)/(4×H)) 随S增大而增大")
    print(f"因此: k_odd 应该随S增大而减小 ✅")
    print(f"而阻抗与k值的关系需要进一步检查...")

def check_impedance_k_relationship():
    """检查阻抗与k值的关系"""
    print("\n📐 检查阻抗与椭圆积分k值的关系")
    print("=" * 60)
    
    import math
    
    # 椭圆积分K(k)的近似计算
    def elliptic_K_approx(k):
        if k < 0.7:
            return math.pi / math.log(2 * (1 + math.sqrt(k)) / (1 - math.sqrt(k)))
        else:
            return math.log(2 * (1 + math.sqrt(k)) / (1 - math.sqrt(k))) / math.pi
    
    # 测试不同k值对应的K(k)
    k_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    print("k值 | K(k) | Z∝1/K(k)")
    print("-" * 25)
    
    for k in k_values:
        K_k = elliptic_K_approx(k)
        z_prop = 1 / K_k  # 阻抗正比于1/K(k)
        print(f"{k:0.1f} | {K_k:0.3f} | {z_prop:0.3f}")
    
    print(f"\n🔍 关键发现:")
    print(f"阻抗 Z ∝ 1/K(k)")
    print(f"当k减小时，K(k)减小，所以Z增大 ✅")
    print(f"这符合S增大→k减小→Z增大的逻辑")

def verify_differential_formula():
    """验证差分阻抗的计算公式"""
    print("\n🧮 验证差分阻抗计算公式")
    print("=" * 60)
    
    print("标准差分阻抗公式:")
    print("Z_diff = 2 × Z_odd")
    print("其中 Z_odd = 30π/√εr_eff × 1/K(k_odd)")
    
    print("\n🤔 可能的问题:")
    print("1. 椭圆积分k值计算是否正确？")
    print("2. 有效介电常数计算是否正确？")
    print("3. 修正系数是否引入了错误？")
    print("4. 奇偶模阻抗的定义是否正确？")

if __name__ == "__main__":
    print("🚨 CPWG间距逻辑验证")
    print("检查间距S增大时阻抗是否正确增大")
    print()
    
    # 运行测试
    test_spacing_logic()
    analyze_coupling_formula()
    check_impedance_k_relationship() 
    verify_differential_formula()
    
    print("\n💡 下一步行动:")
    print("1. 检查椭圆积分k值的定义")
    print("2. 验证CPWG差分对的标准公式")
    print("3. 修正算法中的错误")