import unittest
import json
from lala.PCB_board_Res.src.app import app, PCBImpedanceCalculator

class TestPCBImpedanceCalculator(unittest.TestCase):
    def setUp(self):
        """测试前设置"""
        self.app = app.test_client()
        self.app.testing = True
        self.calculator = PCBImpedanceCalculator()

    def test_microstrip_impedance(self):
        """测试微带线阻抗计算"""
        result = self.calculator.microstrip_impedance(
            w=0.2, h=0.2, t=0.035, er=4.3, loss_tangent=0.02
        )
        self.assertEqual(result['status'], 'success')
        self.assertIsInstance(result['impedance'], (int, float))
        self.assertGreater(result['impedance'], 0)
        self.assertIsInstance(result['er_eff'], (int, float))

    def test_stripline_impedance(self):
        """测试带状线阻抗计算"""
        result = self.calculator.stripline_impedance(
            w=0.15, h=0.4, t=0.035, er=4.3
        )
        self.assertEqual(result['status'], 'success')
        self.assertIsInstance(result['impedance'], (int, float))
        self.assertGreater(result['impedance'], 0)

    def test_differential_impedance(self):
        """测试差分对阻抗计算"""
        result = self.calculator.differential_impedance(
            w=0.1, s=0.1, h=0.2, t=0.035, er=4.3
        )
        self.assertEqual(result['status'], 'success')
        self.assertIsInstance(result['differential_impedance'], (int, float))
        self.assertIsInstance(result['single_ended_impedance'], (int, float))
        self.assertIsInstance(result['coupling_coefficient'], (int, float))

    def test_coaxial_impedance(self):
        """测试同轴线阻抗计算"""
        result = self.calculator.coaxial_impedance(
            inner_diameter=1.0, outer_diameter=3.0, er=2.1
        )
        self.assertEqual(result['status'], 'success')
        self.assertIsInstance(result['impedance'], (int, float))
        self.assertGreater(result['impedance'], 0)

    def test_api_microstrip_calculation(self):
        """测试微带线API接口"""
        data = {
            'type': 'microstrip',
            'params': {
                'width': 0.2,
                'height': 0.2,
                'thickness': 0.035,
                'dielectric': 4.3,
                'loss_tangent': 0.02
            }
        }
        
        response = self.app.post('/api/calculate',
                               data=json.dumps(data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 'success')
        self.assertIn('impedance', result)

    def test_api_differential_calculation(self):
        """测试差分对API接口"""
        data = {
            'type': 'differential',
            'params': {
                'width': 0.1,
                'spacing': 0.1,
                'height': 0.2,
                'thickness': 0.035,
                'dielectric': 4.3
            }
        }
        
        response = self.app.post('/api/calculate',
                               data=json.dumps(data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 'success')
        self.assertIn('differential_impedance', result)

    def test_materials_api(self):
        """测试材料API接口"""
        response = self.app.get('/api/materials')
        self.assertEqual(response.status_code, 200)
        
        materials = json.loads(response.data)
        self.assertIsInstance(materials, dict)
        self.assertIn('FR4', materials)
        self.assertIn('er', materials['FR4'])

    def test_invalid_calculation_type(self):
        """测试无效计算类型"""
        data = {
            'type': 'invalid_type',
            'params': {}
        }
        
        response = self.app.post('/api/calculate',
                               data=json.dumps(data),
                               content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['status'], 'error')

    def test_missing_parameters(self):
        """测试缺少参数"""
        data = {
            'type': 'microstrip',
            'params': {
                'width': 0.2
                # 缺少其他必需参数
            }
        }
        
        response = self.app.post('/api/calculate',
                               data=json.dumps(data),
                               content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['status'], 'error')

    def test_home_page(self):
        """测试主页"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'PCB', response.data)

class TestCalculationAccuracy(unittest.TestCase):
    """测试计算精度"""
    
    def setUp(self):
        self.calculator = PCBImpedanceCalculator()

    def test_microstrip_known_values(self):
        """测试微带线已知值"""
        # 使用已知的设计参数
        result = self.calculator.microstrip_impedance(
            w=0.254, h=0.2, t=0.035, er=4.3
        )
        
        # 期望阻抗约为50Ω (允许±5%误差)
        expected = 50
        tolerance = 0.05
        self.assertAlmostEqual(result['impedance'], expected, delta=expected*tolerance)

    def test_differential_100ohm_target(self):
        """测试100Ω差分对目标"""
        result = self.calculator.differential_impedance(
            w=0.127, s=0.127, h=0.2, t=0.035, er=4.3
        )
        
        # 期望差分阻抗约为100Ω
        expected = 100
        tolerance = 0.1
        self.assertAlmostEqual(result['differential_impedance'], expected, delta=expected*tolerance)

    def test_coaxial_75ohm_cable(self):
        """测试75Ω同轴线"""
        # RG-6同轴线参数
        result = self.calculator.coaxial_impedance(
            inner_diameter=1.024, outer_diameter=4.57, er=2.25
        )
        
        # 期望阻抗约为75Ω
        expected = 75
        tolerance = 0.05
        self.assertAlmostEqual(result['impedance'], expected, delta=expected*tolerance)

if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)