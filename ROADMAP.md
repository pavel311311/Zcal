# Zcal 开发路线图

> 版本: 1.0.0
> 创建时间: 2026-04-10
> 最后更新: 2026-04-10
> 状态: 规划中

---

## 概述

**Zcal** 是一款 PCB 阻抗计算工具，用于计算射频传输线的阻抗特性。项目采用 Vue 3 + Pinia + Axios 技术栈。

**愿景**: 成为工程师首选的轻量级 Web 阻抗计算工具

---

## 技术栈现状

| 模块 | 技术 | 状态 |
|------|------|------|
| 前端框架 | Vue 3 + Composition API | ✅ 良好 |
| 状态管理 | Pinia | ✅ 良好 |
| HTTP 客户端 | Axios | ✅ 良好 |
| 构建工具 | Vite | ✅ 良好 |
| 语言 | JavaScript + TypeScript | 🟡 部分迁移 |
| 代码规范 | ESLint | ⬜ 待添加 |
| 测试 | - | ⬜ 待添加 |
| PWA 支持 | - | ⬜ 待添加 |
| Service Worker | - | ⬜ 待添加 |

---

## 版本规划

### v1.1.x - 稳定性提升期

**目标**: 提升代码质量和稳定性

| 功能 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| TypeScript 完整迁移 | 全部 JS 文件迁移为 TS | 🔴 高 | ✅ 已完成 |
| ESLint + Prettier | 统一代码风格 | 🟡 中 | ⬜ 待开发 |
| 单元测试 | Vitest + Testing Library | 🟡 中 | ⬜ 待开发 |
| 错误边界 | 全局错误处理 | 🟡 中 | ⬜ 待开发 |

---

### v1.2.x - 性能优化期

**目标**: 提升性能和加载速度

| 功能 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| Vite 构建优化 | 分包策略、压缩优化 | 🔴 高 | ✅ 已完成 |
| 组件懒加载 | 更多组件动态导入 | 🟡 中 | ⬜ 待开发 |
| 图片优化 | WebP 格式、CDN | 🟡 中 | ⬜ 待开发 |
| Lighthouse 优化 | 达到 90+ 分数 | 🔴 高 | ⬜ 待开发 |

---

### v1.3.x - 可访问性增强期

**目标**: 符合 WCAG 2.1 AA 标准

| 功能 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| ARIA 标签 | 所有表单元素添加标签 | 🔴 高 | ⬜ 待开发 |
| 键盘导航 | Tab 顺序优化 | 🔴 高 | ⬜ 待开发 |
| 屏幕阅读器 | 状态播报 | 🟡 中 | ⬜ 待开发 |
| 颜色对比度 | 符合 AA 标准 | 🟡 中 | ⬜ 待开发 |

---

### v1.4.x - PWA 与离线支持

**目标**: 支持离线使用和安装

| 功能 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| Service Worker | 离线缓存 | 🔴 高 | ⬜ 待开发 |
| PWA 清单 | 可安装应用 | 🔴 高 | ⬜ 待开发 |
| 离线计算 | 无网络时本地计算 | 🟡 中 | ⬜ 待开发 |
| 后台同步 | 网络恢复后同步 | 🟡 中 | ⬜ 待开发 |

---

### v1.5.x - 用户体验增强

**目标**: 提升用户操作体验

| 功能 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| 计算历史 | 记录计算结果 | 🟡 中 | ⬜ 待开发 |
| 参数预设 | 保存常用参数组合 | 🟡 中 | ⬜ 待开发 |
| 结果导出 | PDF/CSV 导出 | 🟡 中 | ⬜ 待开发 |
| 深色/浅色主题 | 主题切换 | 🟡 中 | ⬜ 待开发 |

---

## 每日开发任务清单

### Task 1: TypeScript 完整迁移 ⬜

**预估工时**: 2-3 天

**任务分解**:

```
Day 1:
  □ 迁移 config/*.js → config/*.ts
  □ 迁移 utils/*.js → utils/*.ts
  □ 添加类型定义

Day 2:
  □ 迁移所有 .js 组件为 .ts/.vue
  □ 运行 vue-tsc 检查
  □ 修复类型错误
```

**验收标准**:
- 全部文件使用 TypeScript
- vue-tsc --noEmit 通过
- 无 any 类型滥用

---

### Task 2: ESLint + Prettier 配置 ⬜

**预估工时**: 1 天

**任务分解**:

```
□ 安装 eslint-config-standard-with-typescript
□ 配置 .eslintrc.cjs
□ 配置 .prettierrc
□ 配置 git hooks (husky + lint-staged)
□ 添加 npm script: lint, lint:fix
```

**验收标准**:
- git commit 时自动 lint
- CI 中运行 lint 检查
- 代码风格统一

---

### Task 3: 单元测试 ⬜

**预估工时**: 2-3 天

**任务分解**:

```
Day 1:
  □ 安装 Vitest + @vue/test-utils
  □ 配置 vite.config.ts 测试入口
  □ 编写 Calculator Service 测试

Day 2:
  □ 编写 Store (Pinia) 测试
  □ 编写核心组件测试

Day 3:
  □ 添加 CI 测试流程
  □ 补充边界用例测试
```

**验收标准**:
- 测试覆盖率 > 70%
- 核心逻辑 100% 覆盖
- CI 测试通过

---

### Task 4: Service Worker + PWA ⬜

**预估工时**: 2-3 天

**任务分解**:

```
Day 1:
  □ 配置 vite-plugin-pwa
  □ 配置 manifest.json
  □ 添加离线缓存策略

Day 2:
  □ 实现计算结果缓存
  □ 实现离线计算逻辑

Day 3:
  □ 测试 PWA 安装
  □ Lighthouse PWA 分数 > 90
```

**验收标准**:
- 可离线使用
- Lighthouse PWA 分数 > 90
- 可安装到桌面

---

### Task 5: 可访问性增强 ⬜

**预估工时**: 2-3 天

**任务分解**:

```
Day 1:
  □ 添加表单 ARIA 标签
  □ 添加错误状态 aria-describedby
  □ 添加焦点管理

Day 2:
  □ 优化颜色对比度
  □ 添加屏幕阅读器状态播报
  □ 测试键盘导航

Day 3:
  □ axe-core 集成
  □ Lighthouse Accessibility 分数 > 90
```

**验收标准**:
- Lighthouse Accessibility > 90
- axe-core 无错误
- 完整键盘导航

---

### Task 6: Lighthouse 性能优化 ⬜

**预估工时**: 2 天

**任务分解**:

```
Day 1:
  □ 分析 Lighthouse 报告
  □ 优化图片资源
  □ 优化字体加载

Day 2:
  □ 优化关键渲染路径
  □ 减少 CLS
  □ 验证分数 > 90
```

**验收标准**:
- Lighthouse Performance > 90
- LCP < 2.5s
- CLS < 0.1

---

## 开发规范

### Git 分支策略

```
main           - 主分支，稳定版本
├── dev        - 开发分支（受保护）
│   ├── perf/  - 性能优化分支
│   ├── feat/  - 功能分支
│   └── fix/   - 修复分支
└── releases   - 发布分支
```

### Commit 规范

```
feat: 新功能
fix: 修复 Bug
perf: 性能优化
refactor: 重构
docs: 文档
test: 测试
chore: 构建/工具
```

示例:
```
feat: 添加计算历史记录功能

- 实现 localStorage 存储
- 添加历史记录面板
- 实现清除历史功能
```

---

## 里程碑

| 版本 | 日期 | 主要功能 |
|------|------|----------|
| v1.0.0 | 已完成 | 基础阻抗计算功能 |
| v1.1.0 | 2 周后 | TypeScript + ESLint + 测试 |
| v1.2.0 | 1 月后 | 性能优化 + Lighthouse 90+ |
| v1.3.0 | 2 月后 | 可访问性 AA 标准 |
| v1.4.0 | 3 月后 | PWA + 离线支持 |
| v1.5.0 | 4 月后 | 用户体验增强 |

---

## 待优化清单

| 优先级 | 功能 | 预估工时 | 依赖 |
|--------|------|----------|------|
| 🔴 高 | TypeScript 完整迁移 | 3 天 | 无 |
| 🔴 高 | Service Worker + PWA | 3 天 | 无 |
| 🔴 高 | Lighthouse > 90 | 2 天 | 无 |
| 🔴 高 | 可访问性 AA | 3 天 | 无 |
| 🟡 中 | ESLint + Prettier | 1 天 | 无 |
| 🟡 中 | 单元测试 | 3 天 | TypeScript |
| 🟡 中 | 计算历史 | 2 天 | 无 |
| 🟡 中 | 参数预设 | 2 天 | 无 |
| 🟡 中 | 结果导出 | 2 天 | 无 |
| 🟡 中 | 主题切换 | 1 天 | 无 |

---

## 资源链接

- [Vue 3 文档](https://vuejs.org/)
- [Vite 构建优化指南](https://vitejs.dev/guide/performance.html)
- [Web Vitals](https://web.dev/vitals/)
- [WCAG 2.1 指南](https://www.w3.org/WAI/WCAG21/quickref/)
- [Vitest 测试框架](https://vitest.dev/)
