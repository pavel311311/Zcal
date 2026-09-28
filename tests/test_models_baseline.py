"""
Zcal 模型回归基线测试
运行：pytest tests -q
"""
import sys, os, math
import pytest

BACKEND = os.path.join(os.path.dirname(__file__), '..', 'src', 'backend')
sys.path.insert(0, os.path.abspath(BACKEND))

from app.services.models import MODEL_MAP

BASE = {
    'frequency': 1, 'width': 0.2, 'height': 1.6, 'thickness': 0.035,
    'dielectric': 4.3, 'loss_tangent': 0.01, 'spacing': 0.2, 'gap': 0.2,
    'dielectric_thickness': 0.254, 'height1': 0.8, 'height2': 0.8,
    'inner_diameter': 0.5, 'outer_diameter': 1.6,
}

def calc(model_type, **over):
    p = dict(BASE); p.update(over)
    return MODEL_MAP[model_type](p).get_result()

def test_all_models_run_without_error():
    """所有注册模型都必须能成功计算且返回有限值"""
    for name in MODEL_MAP:
        r = calc(name)
        assert r['status'] == 'success', f'{name} status != success'
        z = r['impedance']
        assert z is not None and math.isfinite(z) and z > 0, f'{name} impedance invalid: {z}'

def test_microstrip_baseline():
    assert abs(calc('microstrip')['impedance'] - 140.38) < 1.0

def test_stripline_impedance_is_correct():
    """带状线 W=0.2/H=1.6/er=4.3 应约 95.5Ω（修复前错误为 8Ω）"""
    z = calc('stripline')['impedance']
    assert 85 < z < 105, f'stripline Z0 wrong: {z}'

def test_coaxial_baseline():
    r = calc('coaxial', inner_diameter=0.5, outer_diameter=1.6, dielectric=2.1)
    assert abs(r['impedance'] - 48.0) < 4.0

def test_cpw_and_cpwg_reasonable():
    assert 70 < calc('cpw')['impedance'] < 90
    assert 75 < calc('cpwg')['impedance'] < 95

@pytest.mark.parametrize('name', [
    'differential_microstrip', 'differential_cpw', 'differential_cpwg',
    'differential_striplines', 'broadside_striplines', 'asymmetric_stripline',
])
def test_formerly_broken_models_run(name):
    """修复前会崩溃的模型现在必须能算"""
    assert calc(name)['status'] == 'success'

@pytest.mark.parametrize('name', [
    'differential_microstrip', 'differential_cpw', 'differential_cpwg',
    'differential_striplines', 'broadside_striplines',
])
def test_spacing_monotonic_increases_diff_impedance(name):
    """差分/耦合模型：spacing 增大，差分阻抗应单调不减"""
    zs = [calc(name, spacing=s)['impedance'] for s in (0.2, 0.5, 1.0, 2.0)]
    for a, b in zip(zs, zs[1:]):
        assert b >= a - 1e-6, f'{name} not monotonic: {zs}'

def test_asymmetric_stripline_asymmetry_effect():
    sym = calc('asymmetric_stripline', height1=0.8, height2=0.8)['impedance']
    asym = calc('asymmetric_stripline', height1=0.2, height2=1.4)['impedance']
    assert asym < sym, 'asymmetry should lower impedance'

def test_invalid_params_rejected():
    with pytest.raises(ValueError):
        calc('microstrip', frequency=-1)
    with pytest.raises(ValueError):
        calc('microstrip', thickness=5.0)  # thickness >= height
    with pytest.raises(ValueError):
        calc('coaxial', inner_diameter=2.0, outer_diameter=1.0)
