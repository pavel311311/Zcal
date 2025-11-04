"""
简化的PCB阻抗计算器测试脚本
"""
import math

def test_microstrip_simple():
    """简单测试微带线计算"""
    print("=== 微带线阻抗计算测试 ===")
    
    # 输入参数
    w = 0.254  # 线宽 mm
    h = 0.2    # 介质厚度 mm  
    t = 0.035  # 铜厚 mm
    er = 4.3   # 介电常数
    
    print(f"输入参数: W={w}mm, H={h}mm, T={t}mm, εr={er}")
    
    # 有效介电常数
    er_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * h / w) ** (-0.5)
    print(f"有效介电常数: {er_eff:.3f}")
    
    # 考虑铜厚的有效线宽
    w_eff = w + t * (1 + math.log(2 * h / t)) / math.pi
    print(f"有效线宽: {w_eff:.3f}mm")
    
    # 阻抗计算
    if w_eff / h < 1:
        z0 = 60 / math.sqrt(er_eff) * math.log(8 * h / w_eff + w_eff / (4 * h))
        print("使用窄线公式")
    else:
        z0 = 120 * math.pi / math.sqrt(er_eff) / (w_eff / h + 1.393 + 0.667 * math.log(w_eff / h + 1.444))
        print("使用宽线公式")
    
    print(f"计算阻抗: {z0:.2f}Ω")
    print(f"目标50Ω的误差: {abs(z0-50)/50*100:.1f}%")
    print()

def test_coaxial_simple():
    """简单测试同轴线计算"""
    print("=== 同轴线阻抗计算测试 ===")
    
    # RG-6参数
    d = 1.024  # 内导体直径
    D = 4.57   # 外导体内径  
    er = 2.25  # 介电常数
    
    print(f"输入参数: d={d}mm, D={D}mm, εr={er}")
    
    z0 = 60 / math.sqrt(er) * math.log(D / d)
    
    print(f"计算阻抗: {z0:.2f}Ω")
    print(f"目标75Ω的误差: {abs(z0-75)/75*100:.1f}%")
    print()

def test_flask_import():
    """测试Flask导入"""
    print("=== Flask导入测试 ===")
    try:
        from flask import Flask
        print("✅ Flask导入成功")
        
        # 创建简单应用
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return "测试成功"
            
        print("✅ Flask应用创建成功")
        
    except ImportError as e:
        print(f"❌ Flask导入失败: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

def main():
    """主测试函数"""
    print("PCB阻抗计算器 - 简化测试")
    print("=" * 50)
    
    test_microstrip_simple()
    test_coaxial_simple()  
    test_flask_import()
    
    print("测试完成！")

if __name__ == "__main__":
    main()