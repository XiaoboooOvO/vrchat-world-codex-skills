# 推荐的外部开源技能

核对日期：2026-09-26。

本页只推荐与当前 Blender → Unity 制作和导出相关的少数技能；不代表要安装或采用上游技能包中的全部内容。

## 来源

上游项目：[arjun988/blender-skills](https://github.com/arjun988/blender-skills)。上游仓库将其许可标为 MIT；使用或复制技能文件时，以当时的上游 LICENSE 为准。本仓库仅记录推荐与链接，不复制第三方技能文件。

## 推荐子集

| 技能 | 适用任务 | 使用边界 |
| --- | --- | --- |
| unity-export | Blender 资产导入 Unity；核对比例、朝向、材质、骨架或碰撞导出 | 目标为 Unity 时使用；轴向仍须按资产和项目合同确认 |
| export-pipeline | Blender 到不同引擎或交换格式的导出 | 按目标格式和目标引擎选项；不要把示例预设当成通用轴向合同 |
| blender-modeler | 一般建模、blockout、网格整理和场景组织 | 需要实际建模或整理时使用 |
| blender-director | 涉及多个制作环节的 Blender 任务规划 | 仅在跨多个专业流程时使用；简单局部编辑可直接选专用技能 |
| asset-optimization | 有明确性能预算或优化目标的资产处理 | 按项目目标使用，不作为所有导出的固定门槛 |
| lod-pipeline | 需要制作或修订 LOD 的交付 | 只有任务包含 LOD 时使用 |
| collision-proxy | 需要碰撞代理或碰撞网格的交付 | 只有任务包含碰撞时使用 |

其中 unity-export 和 export-pipeline 是我们已在 Blender → Unity 资产流程中用到的外部技能；其余列为按任务推荐的候选。

## 本地适配说明

本机安装的 unity-export 和 export-pipeline 副本已增加朝向与坐标映射提示。这些是本地修改，不代表上游已包含或接受这些改动。更新本地副本时应先比较差异，避免覆盖本地适配。

技能文件的存在不代表 Blender MCP 已连接，也不代表技能中的任一工具在当前会话可用。项目规则与资产合同优先于外部技能的通用建议。
