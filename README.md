# VRChat World Codex Skills

一组面向 Codex 的 VRChat Worlds 工作流 Skills：先把空间和职责设计清楚，再用有边界、可验证的方式实施到 Unity。

## 两个 Skill

### `design-modular-vrchat-world`

把自然语言中的世界想法整理成可实现的空间设计：

- 玩家旅程和角色分工
- 功能模块图及其连接类型
- 模块局部坐标、边界、入口、出口和视线
- 交互面、摆放面和跨模块接口
- 语义化 Unity 层级
- 灰盒顺序和模块交接信息

它负责设计，不负责修改 Unity。

### `build-vrchat-world`

把已经明确边界的设计安全地带进 Unity/VRChat 项目：

- 根据风险选择离线文档、只读诊断、源码修改、场景补丁或明确的运行/构建模式
- 检查当前项目规则、Git 状态、序列化所有权和 Unity 实例
- 保护脏工作区和无关改动
- 管理 UdonSharp ProgramAsset、场景 Apply、Undo、保存和编译检查
- 对超时、断连、`STARTED` 和 `PENDING` 结果进行恢复判断
- 区分静态、编译、UdonSharp、ClientSim、桌面、VR、多人和构建证据

它不会默认进入 Play Mode、运行 ClientSim、Build & Test 或上传。

## 推荐工作流

```text
需求或问题
  -> design-modular-vrchat-world
  -> 玩家旅程、模块边界和实现交接
  -> build-vrchat-world
  -> Unity 检查、有限修改、编译和针对性验证
```

如果只是问“这个空间应该怎么拆”，使用设计 Skill。

如果已经知道要改什么，并且问题是“如何安全地改进 Unity”，使用构建 Skill。

如果是新世界或大范围重组，先设计，再实施。

## 安装

将两个目录分别复制到 Codex 的 skills 目录：

```text
<Codex skills directory>/design-modular-vrchat-world/
<Codex skills directory>/build-vrchat-world/
```

Windows 默认位置通常是：

```text
%USERPROFILE%\.codex\skills\
```

安装后可以显式调用：

```text
$design-modular-vrchat-world
$build-vrchat-world
```

## 使用边界

- 当前项目的 `AGENTS.md`、贡献指南和其他项目规则优先于通用 Skill。
- 设计 Skill 不授权 Unity 修改。
- 构建 Skill 不自动推断运行、构建、上传或多人验收授权。
- 只读检查、编译证据和运行时证据必须分开描述。
- 本仓库不包含 Unity 项目、场景、素材或 VRChat 上传凭据。
- `build-vrchat-world/scripts/audit_vrchat_world.py` 是只读辅助快照工具，不替代完整的 Unity、VR、多人或发布验收。

## 目录结构

```text
.
├── build-vrchat-world/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
├── design-modular-vrchat-world/
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   └── references/
└── docs/
    └── VIDEO_INTRO_CN.md
```

## 当前状态

这是一个可迁移的工作流包，不是完整的 VRChat 世界模板。使用时应从目标项目的实时状态、项目规则和源文件出发，不要把本仓库中的示例结构当成所有项目的固定层级。

## License

本仓库采用 [MIT License](LICENSE)。
