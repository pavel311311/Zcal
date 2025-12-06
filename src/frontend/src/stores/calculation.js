import { defineStore } from 'pinia'

export const useCalculationStore = defineStore('calculation', {
  state: () => ({
    result: null,
    isLoading: false,
  }),
  actions: {
    setLoading(flag) {
      this.isLoading = flag
    },
    setResult(res) {
      this.result = res
    },
    clear() {
      this.result = null
      this.isLoading = false
    },
  },
})
