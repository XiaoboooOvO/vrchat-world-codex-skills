# VRChat World Codex Skills

面向 Codex 的三项自有技能。按任务选择；常规工作不必先经过模块设计。

## 自有技能

### design-modular-vrchat-world

当任务需要定义或修改空间模块、职责边界或模块接口时，用它整理玩家旅程、模块关系、局部空间约束和实现交接。模块边界已明确时，常规局部修改不需要调用它。

它负责设计，不负责修改 Unity。

### build-vrchat-world

Unity/VRChat 项目的实现、诊断和修复入口。边界已明确时可直接使用；遵循项目规则，只在请求范围内做必要检查和修改。

### coordinate-transform-audit

核对坐标系、轴向、角度、尺度和父级变换；适用于单个资产导入后旋转、镜像、偏移或比例异常，也适用于多坐标系换算。不要求模块化，也不授权导入素材或修改场景。

## 如何选择

- 需要拆分或调整模块、职责、边界或接口：先用 design-modular-vrchat-world；若还要改 Unity，再交给 build-vrchat-world。
- 模块边界和修改范围已清楚，任务是 Unity 局部实现、诊断或修复：直接用 build-vrchat-world。
- 坐标、轴向或导入角度不明：用 coordinate-transform-audit；若审计后需要改 Unity，再按项目规则使用 build-vrchat-world。

## 外部开源技能推荐

按需使用 Blender 技能，不把外部技能包当作项目依赖。来源、推荐子集和本地适配说明见 [推荐的外部开源技能](docs/RECOMMENDED_OPEN_SOURCE_SKILLS.md)。

## 安装

把需要的技能目录复制到 Codex skills 目录：

- design-modular-vrchat-world/
- build-vrchat-world/
- coordinate-transform-audit/

可以只安装当前工作会用到的技能。

## 使用边界

- 目标项目的 AGENTS.md、合同和其他项目规则优先于通用技能。
- 设计技能只负责设计；坐标技能只负责核验或换算；它们都不授权 Unity 修改。
- build-vrchat-world 不会因为技能已安装，就扩大用户请求或推断未授权的副作用。
- 技能只按任务需要提供检查建议；不要求每次工作列出无关的测试或验收层。
- audit_vrchat_world.py 是只读快照工具，不能替代本次任务所需的实际依据。

## 文件结构

- build-vrchat-world/：Unity/VRChat 实施与诊断
- coordinate-transform-audit/：坐标与导入朝向审计
- design-modular-vrchat-world/：模块与空间设计
- docs/：技能说明及外部推荐

这是可迁移的工作流包，不是完整的 VRChat 世界模板。使用时以目标项目的实时状态和项目规则为准。

## License

本仓库采用 [MIT License](LICENSE)。
