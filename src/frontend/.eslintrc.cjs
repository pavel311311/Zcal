/* eslint-env node */
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  parser: 'vue-eslint-parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    parser: '@typescript-eslint/parser',
  },
  plugins: ['@typescript-eslint'],
  rules: {
    // Vue specific
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'warn',
    'vue/require-default-prop': 'off',
    'vue/require-explicit-emits': 'off',
    'vue/v-on-event-hyphenation': 'off',
    // TypeScript
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    // General
    'no-console': 'warn',
    'no-debugger': 'warn',
  },
  overrides: [
    {
      files: ['*.vue'],
      rules: {
        // Allow TS in Vue SFC
        'no-undef': 'off',
      },
    },
  ],
}
