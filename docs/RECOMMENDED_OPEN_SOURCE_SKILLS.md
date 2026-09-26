# 外部技能与工具推荐

核对日期：2026-09-26。

按具体任务选用技能；本页列出来源与适用范围，不把外部技能包当作项目依赖。技能已安装、项目中实际调用过技能、MCP 工具可用、Unity Editor 已连接，是四种不同的状态。

## 游戏设计：一套三个技能

来源：[MistRain-1/game-design-skill](https://github.com/MistRain-1/game-design-skill)，仓库自身采用 [MIT License](https://github.com/MistRain-1/game-design-skill/blob/main/LICENSE)。三个同级技能应作为完整套件安装；`game-design` 负责按问题选择另外两个。

| 技能 | 适用任务 |
| --- | --- |
| game-design | 游戏设计问题的入口与路由 |
| game-production | 核心体验、玩法循环、规则、系统、制作范围与风险 |
| level-design | 地图、路径、导航、遭遇、空间节奏与关卡验证 |

讨论玩家体验、地图和关卡时使用；它们提供设计判断，不负责操作 Unity。单纯安装这套技能，不能证明它已参与某个项目的设计。

## Unity MCP：工具与技能分开看

来源：[CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp)，其 [unity-mcp-skill](https://github.com/CoplayDev/unity-mcp/blob/beta/unity-mcp-skill/SKILL.md) 声明的技能名为 `unity-mcp-orchestrator`；上游采用 [MIT License](https://github.com/CoplayDev/unity-mcp/blob/beta/LICENSE)。

`unity-mcp-orchestrator` 是操作 Unity Editor 的工作流技能。Unity MCP 是另外的服务器和工具连接；技能文件存在或工具名出现，都不能证明当前 Editor 已连接或目标项目正确。实际操作前先确认工具、精确项目实例、场景和 Editor 状态。

本仓库的 `build-vrchat-world` 已包含 [Unity MCP 工作流参考](../build-vrchat-world/references/unity-mcp-workflow.md)，只在任务确实使用 Unity MCP 时读取。独立的 `unity-mcp-orchestrator` 可按需补充工具用法；目标项目规则和本仓库的操作边界优先。

## Blender → Unity 资产流程

来源：[arjun988/blender-skills](https://github.com/arjun988/blender-skills)。上游仓库将其许可标为 MIT；使用或复制技能文件时，以当时的上游 LICENSE 为准。本仓库仅记录推荐与链接，不复制第三方技能文件。

| 技能 | 适用任务 | 使用边界 |
| --- | --- | --- |
| unity-export | Blender 资产导入 Unity；核对比例、朝向、材质、骨架或碰撞导出 | 目标为 Unity 时使用；轴向仍须按资产和项目合同确认 |
| export-pipeline | Blender 到不同引擎或交换格式的导出 | 按目标格式和目标引擎选项；示例预设不是通用轴向合同 |
| blender-modeler | 一般建模、blockout、网格整理和场景组织 | 需要实际建模或整理时使用 |
| blender-director | 涉及多个制作环节的 Blender 任务规划 | 跨多个专业流程时使用；简单局部编辑可直接选专用技能 |
| asset-optimization | 有明确性能预算或优化目标的资产处理 | 按项目目标使用 |
| lod-pipeline | 制作或修订 LOD | 任务包含 LOD 时使用 |
| collision-proxy | 制作碰撞代理或碰撞网格 | 任务包含碰撞时使用 |

本机的 `unity-export` 和 `export-pipeline` 副本已增加朝向与坐标映射提示；这是本地修改，不代表上游已包含这些内容。更新时先比较差异。上游还有大量 `genre-*` 技能，主要用于 Blender 资产的类型化美术指导；它们不能代替 `game-design` 套件的玩法与关卡设计。

## 本机历史使用核对

以下是截至 2026-09-26 能从既有项目文档和会话记录核对的范围；这些记录不代表当前会话的工具连接状态。

| 技能或工具 | 已核对状态 |
| --- | --- |
| game-production、level-design | 实际用于世界地图、玩家路线与空间可读性的规划讨论；没有查到同次讨论调用总入口 game-design 的证据 |
| unity-mcp-orchestrator | 曾被明确选用并读取，用于 Unity 场景检查流程；Unity MCP 工具也有实际调用记录，但当前 Editor 连接仍须实时确认 |
| blender-director | 实际用于 Blender 制作输入包和工作单规划；该记录不代表建模或渲染已执行 |
| unity-export、export-pipeline | 本机副本的朝向与坐标适配已核对；本轮没有定位到可独立核对的项目调用记录 |
| blender-modeler、asset-optimization、lod-pipeline、collision-proxy、genre-* | 已安装或列为按需候选；本轮没有定位到具体项目调用记录 |

技能文件的存在不代表 Blender MCP 已连接，也不代表技能中的工具在当前会话可用。项目规则与资产合同优先于外部技能的通用建议。
