<template>
  <div class="result-display card">
    <h2>计算结果</h2>

    <div v-if="loading" class="loading-container">
      <div class="loading"></div>
      <p>正在计算...</p>
    </div>

    <div v-else-if="!result" class="placeholder">
      <p>请配置参数并点击计算按钮</p>
    </div>

    <div v-else-if="result.status === 'error'" class="error-box">
      <h3>❌ 计算错误</h3>
      <p>{{ result.message }}</p>
    </div>

    <div v-else class="result-content">
      <h3>✓ 计算成功</h3>

      <!-- 阻抗结果 -->
      <div class="result-section">
        <h4>阻抗计算结果</h4>
        <div class="result-box">
          <!-- 主要阻抗值 -->
          <div v-if="result.impedance !== undefined" class="result-item">
            <span class="result-label">单端阻抗:</span>
            <span class="result-value">{{ result.impedance }} Ω</span>
          </div>

          <div v-if="result.differential_impedance !== undefined" class="result-item">
            <span class="result-label">差分阻抗:</span>
            <span class="result-value">{{ result.differential_impedance }} Ω</span>
          </div>

          <div v-if="result.single_ended_impedance !== undefined" class="result-item">
            <span class="result-label">单端阻抗:</span>
            <span class="result-value">{{ result.single_ended_impedance }} Ω</span>
          </div>

          <div v-if="result.odd_mode_impedance !== undefined" class="result-item">
            <span class="result-label">奇模阻抗:</span>
            <span class="result-value">{{ result.odd_mode_impedance }} Ω</span>
          </div>

          <div v-if="result.even_mode_impedance !== undefined" class="result-item">
            <span class="result-label">偶模阻抗:</span>
            <span class="result-value">{{ result.even_mode_impedance }} Ω</span>
          </div>

          <div v-if="result.common_mode_impedance !== undefined" class="result-item">
            <span class="result-label">共模阻抗:</span>
            <span class="result-value">{{ result.common_mode_impedance }} Ω</span>
          </div>
        </div>
      </div>

      <!-- 介电特性 -->
      <div v-if="result.er_eff !== undefined" class="result-section">
        <h4>介电特性</h4>
        <div class="result-box">
          <div class="result-item">
            <span class="result-label">有效介电常数:</span>
            <span class="result-value">{{ result.er_eff }}</span>
          </div>

          <div v-if="result.er_eff_odd !== undefined" class="result-item">
            <span class="result-label">奇模有效介电常数:</span>
            <span class="result-value">{{ result.er_eff_odd }}</span>
          </div>

          <div v-if="result.er_eff_even !== undefined" class="result-item">
            <span class="result-label">偶模有效介电常数:</span>
            <span class="result-value">{{ result.er_eff_even }}</span>
          </div>
        </div>
      </div>

      <!-- 耦合和填充因子 -->
      <div class="result-section">
        <h4>耦合特性</h4>
        <div class="result-box">
          <div v-if="result.coupling_coefficient !== undefined" class="result-item">
            <span class="result-label">耦合系数:</span>
            <span class="result-value">{{ result.coupling_coefficient }}</span>
          </div>

          <div v-if="result.coupling_factor !== undefined" class="result-item">
            <span class="result-label">耦合因子:</span>
            <span class="result-value">{{ result.coupling_factor }}</span>
          </div>

          <div v-if="result.filling_factor !== undefined" class="result-item">
            <span class="result-label">填充因子:</span>
            <span class="result-value">{{ result.filling_factor }}</span>
          </div>

          <div v-if="result.ground_coupling !== undefined" class="result-item">
            <span class="result-label">地线耦合:</span>
            <span class="result-value">{{ result.ground_coupling }}</span>
          </div>
        </div>
      </div>

      <!-- 几何和损耗参数 -->
      <div class="result-section">
        <h4>参数详情</h4>
        <div class="result-box">
          <div v-if="result.k_parameter !== undefined" class="result-item">
            <span class="result-label">几何参数 k:</span>
            <span class="result-value">{{ result.k_parameter }}</span>
          </div>

          <div v-if="result.k_odd !== undefined" class="result-item">
            <span class="result-label">奇模参数 k:</span>
            <span class="result-value">{{ result.k_odd }}</span>
          </div>

          <div v-if="result.k_even !== undefined" class="result-item">
            <span class="result-label">偶模参数 k:</span>
            <span class="result-value">{{ result.k_even }}</span>
          </div>

          <div v-if="result.conductor_loss !== undefined && result.conductor_loss !== null" class="result-item">
            <span class="result-label">导体损耗:</span>
            <span class="result-value">{{ result.conductor_loss }} dB/m</span>
          </div>

          <div v-if="result.dielectric_loss !== undefined" class="result-item">
            <span class="result-label">介质损耗:</span>
            <span class="result-value">{{ result.dielectric_loss }} dB/m</span>
          </div>

          <div v-if="result.offset_factor !== undefined" class="result-item">
            <span class="result-label">偏移修正系数:</span>
            <span class="result-value">{{ result.offset_factor }}</span>
          </div>

          <div v-if="result.upper_distance !== undefined" class="result-item">
            <span class="result-label">上层距离:</span>
            <span class="result-value">{{ result.upper_distance }} mm</span>
          </div>

          <div v-if="result.lower_distance !== undefined" class="result-item">
            <span class="result-label">下层距离:</span>
            <span class="result-value">{{ result.lower_distance }} mm</span>
          </div>

          <div v-if="result.h_eff !== undefined" class="result-item">
            <span class="result-label">有效厚度:</span>
            <span class="result-value">{{ result.h_eff }} mm</span>
          </div>

          <div v-if="result.signal_to_ground_gap !== undefined" class="result-item">
            <span class="result-label">信号到地间距:</span>
            <span class="result-value">{{ result.signal_to_ground_gap }} mm</span>
          </div>

          <div v-if="result.ground_width !== undefined" class="result-item">
            <span class="result-label">地线宽度:</span>
            <span class="result-value">{{ result.ground_width }} mm</span>
          </div>

          <div v-if="result.K_odd !== undefined" class="result-item">
            <span class="result-label">椭圆积分 K(k)奇模:</span>
            <span class="result-value">{{ result.K_odd }}</span>
          </div>

          <div v-if="result.K_even !== undefined" class="result-item">
            <span class="result-label">椭圆积分 K(k)偶模:</span>
            <span class="result-value">{{ result.K_even }}</span>
          </div>
        </div>
      </div>

      <!-- 导出按钮 -->
      <div class="export-actions">
        <button class="btn btn-secondary" @click="exportAsJSON">导出为 JSON</button>
        <button class="btn btn-secondary" @click="copyToClipboard">复制结果</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  result: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const exportAsJSON = () => {
  const dataStr = JSON.stringify(props.result, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `impedance-calculation-${Date.now()}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const copyToClipboard = () => {
  const text = Object.entries(props.result)
    .map(([key, value]) => `${key}: ${value}`)
    .join('\n')
  
  navigator.clipboard.writeText(text).then(() => {
    alert('已复制到剪贴板')
  })
}
</script>

<style scoped>
.result-display {
  min-height: 400px;
}

.result-display h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 1.5em;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

.placeholder {
  text-align: center;
  color: #999;
  padding: 60px 20px;
  font-size: 1.1em;
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
}

.loading {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-box {
  background-color: #fee2e2;
  border: 2px solid #fecaca;
  color: #dc2626;
  padding: 20px;
  border-radius: 8px;
}

.error-box h3 {
  margin-bottom: 10px;
  font-size: 1.1em;
}

.result-content h3 {
  color: #10b981;
  margin-bottom: 20px;
  font-size: 1.2em;
}

.result-section {
  margin-bottom: 25px;
}

.result-section h4 {
  color: #333;
  margin-bottom: 12px;
  font-size: 1.05em;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.result-box {
  background: #f0f9ff;
  border-left: 4px solid #667eea;
  padding: 15px;
  border-radius: 8px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e5e7eb;
}

.result-item:last-child {
  border-bottom: none;
}

.result-label {
  font-weight: 600;
  color: #555;
}

.result-value {
  color: #667eea;
  font-weight: 700;
  font-size: 1.1em;
}

.export-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn {
  flex: 1;
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-secondary {
  background-color: #764ba2;
  color: white;
}

.btn-secondary:hover {
  background-color: #6a3d8a;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(118, 75, 162, 0.3);
}

@media (max-width: 768px) {
  .result-display {
    position: static;
  }

  .export-actions {
    flex-direction: column;
  }
}
</style>
