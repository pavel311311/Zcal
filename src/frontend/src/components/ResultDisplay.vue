<template>
  <div class="result-display card">
    <h2>计算结果</h2>

    <div v-if="store.isLoading" class="loading-container">
      <div class="loading"></div>
      <p>正在计算...</p>
    </div>

    <div v-else-if="!store.result" class="placeholder">
      <p>请配置参数并点击计算按钮</p>
    </div>

    <div v-else-if="store.result && store.result.status === 'error'" class="error-box">
      <h3>❌ 计算错误</h3>
      <p>{{ store.result.message }}</p>
    </div>

    <div v-else class="result-content">
      <h3>✓ 计算成功</h3>

      <!-- 阻抗结果 -->
      <div class="result-section">
        <h4>阻抗计算结果</h4>
        <div class="result-box">
          <!-- 主要阻抗值 -->
          <div v-if="store.result.impedance !== undefined" class="result-item">
            <span class="result-label">单端阻抗:</span>
            <span class="result-value">{{ store.result.impedance }} Ω</span>
          </div>

          <div v-if="store.result.differential_impedance !== undefined" class="result-item">
            <span class="result-label">差分阻抗:</span>
            <span class="result-value">{{ store.result.differential_impedance }} Ω</span>
          </div>

          <div v-if="store.result.single_ended_impedance !== undefined" class="result-item">
            <span class="result-label">单端阻抗:</span>
            <span class="result-value">{{ store.result.single_ended_impedance }} Ω</span>
          </div>

          <div v-if="store.result.odd_mode_impedance !== undefined" class="result-item">
            <span class="result-label">奇模阻抗:</span>
            <span class="result-value">{{ store.result.odd_mode_impedance }} Ω</span>
          </div>

          <div v-if="store.result.even_mode_impedance !== undefined" class="result-item">
            <span class="result-label">偶模阻抗:</span>
            <span class="result-value">{{ store.result.even_mode_impedance }} Ω</span>
          </div>

          <div v-if="store.result.common_mode_impedance !== undefined" class="result-item">
            <span class="result-label">共模阻抗:</span>
            <span class="result-value">{{ store.result.common_mode_impedance }} Ω</span>
          </div>
        </div>
      </div>

      <!-- 介电特性 -->
      <div v-if="store.result.er_eff !== undefined" class="result-section">
        <h4>介电特性</h4>
        <div class="result-box">
          <div class="result-item">
            <span class="result-label">有效介电常数:</span>
            <span class="result-value">{{ store.result.er_eff }}</span>
          </div>

          <div v-if="store.result.er_eff_odd !== undefined" class="result-item">
            <span class="result-label">奇模有效介电常数:</span>
            <span class="result-value">{{ store.result.er_eff_odd }}</span>
          </div>

          <div v-if="store.result.er_eff_even !== undefined" class="result-item">
            <span class="result-label">偶模有效介电常数:</span>
            <span class="result-value">{{ store.result.er_eff_even }}</span>
          </div>
        </div>
      </div>

      <!-- 耦合和填充因子 -->
      <div class="result-section">
        <h4>耦合特性</h4>
        <div class="result-box">
          <div v-if="store.result.coupling_coefficient !== undefined" class="result-item">
            <span class="result-label">耦合系数:</span>
            <span class="result-value">{{ store.result.coupling_coefficient }}</span>
          </div>

          <div v-if="store.result.coupling_factor !== undefined" class="result-item">
            <span class="result-label">耦合因子:</span>
            <span class="result-value">{{ store.result.coupling_factor }}</span>
          </div>

          <div v-if="store.result.filling_factor !== undefined" class="result-item">
            <span class="result-label">填充因子:</span>
            <span class="result-value">{{ store.result.filling_factor }}</span>
          </div>

          <div v-if="store.result.ground_coupling !== undefined" class="result-item">
            <span class="result-label">地线耦合:</span>
            <span class="result-value">{{ store.result.ground_coupling }}</span>
          </div>
        </div>
      </div>

      <!-- 几何和损耗参数 -->
      <div class="result-section">
        <h4>参数详情</h4>
        <div class="result-box">
          <div v-if="store.result.k_parameter !== undefined" class="result-item">
            <span class="result-label">几何参数 k:</span>
            <span class="result-value">{{ store.result.k_parameter }}</span>
          </div>

          <div v-if="store.result.k_odd !== undefined" class="result-item">
            <span class="result-label">奇模参数 k:</span>
            <span class="result-value">{{ store.result.k_odd }}</span>
          </div>

          <div v-if="store.result.k_even !== undefined" class="result-item">
            <span class="result-label">偶模参数 k:</span>
            <span class="result-value">{{ store.result.k_even }}</span>
          </div>

          <div v-if="store.result.conductor_loss !== undefined && store.result.conductor_loss !== null" class="result-item">
            <span class="result-label">导体损耗:</span>
            <span class="result-value">{{ store.result.conductor_loss }} dB/m</span>
          </div>

          <div v-if="store.result.dielectric_loss !== undefined" class="result-item">
            <span class="result-label">介质损耗:</span>
            <span class="result-value">{{ store.result.dielectric_loss }} dB/m</span>
          </div>

          <div v-if="store.result.offset_factor !== undefined" class="result-item">
            <span class="result-label">偏移修正系数:</span>
            <span class="result-value">{{ store.result.offset_factor }}</span>
          </div>

          <div v-if="store.result.upper_distance !== undefined" class="result-item">
            <span class="result-label">上层距离:</span>
            <span class="result-value">{{ store.result.upper_distance }} mm</span>
          </div>

          <div v-if="store.result.lower_distance !== undefined" class="result-item">
            <span class="result-label">下层距离:</span>
            <span class="result-value">{{ store.result.lower_distance }} mm</span>
          </div>

          <div v-if="store.result.h_eff !== undefined" class="result-item">
            <span class="result-label">有效厚度:</span>
            <span class="result-value">{{ store.result.h_eff }} mm</span>
          </div>

          <div v-if="store.result.signal_to_ground_gap !== undefined" class="result-item">
            <span class="result-label">信号到地间距:</span>
            <span class="result-value">{{ store.result.signal_to_ground_gap }} mm</span>
          </div>

          <div v-if="store.result.ground_width !== undefined" class="result-item">
            <span class="result-label">地线宽度:</span>
            <span class="result-value">{{ store.result.ground_width }} mm</span>
          </div>

          <div v-if="store.result.K_odd !== undefined" class="result-item">
            <span class="result-label">椭圆积分 K(k)奇模:</span>
            <span class="result-value">{{ store.result.K_odd }}</span>
          </div>

          <div v-if="store.result.K_even !== undefined" class="result-item">
            <span class="result-label">椭圆积分 K(k)偶模:</span>
            <span class="result-value">{{ store.result.K_even }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCalculationStore } from '../stores/calculation'

const store = useCalculationStore()


</script>
