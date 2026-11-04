# Paper Contract（论文契约）

本文件简要记录论文的目标，是供 Human 阅读的权威依据。讨论和修改时应保持它的实用性，不要把它变成完整的研究台账。

以下控制词是协作提示，而非僵硬的权限制度：

- **locked**（锁定）——Agent 可以分析或提出修改，但不得静默改变其含义。
- **bounded**（有界）——Agent 可以在写明的边界内调整。
- **free**（自由）——Agent 可以处理实现或措辞，同时尊重更高层的决定。
- **unresolved**（未决）——Human 与 Agent 尚未确定；应灵活推进、保留不确定性，并在作出影响重大或难以撤销的选择前询问。

## Paper identity

论文身份：依次填写工作标题、目标投稿场所、论文类型、预期读者和一句话定位。提交前须核实当前官方规则。

- Working title: TODO Paper Title
- Target venue: unresolved (verify current official rules before submission work)
- Paper type: unresolved
- Intended readers: TODO
- One-sentence positioning: TODO

## Operating mode

Human 通过设置 `Mode` 声明论文的运行方式；Agent 遵守所声明的边界，不得静默扩大。

- Mode: unresolved (`collaborative` or `autonomous`)

**collaborative**（协作）模式下，Human 参与每个实质性步骤；Agent 按要求起草和修改，并将重大选择整理成决策包。

**autonomous**（自主）模式下，Human 提供简报和材料，Agent 自行完成起草、自审、润色以及 `main`、`submission` 和 `blind` 构建；思路塑造和证据分析只能作为提案准备。修改锁定项、批准发布或最终提交之前，Agent 必须停下来取得 Human 批准。

## What readers should believe

读者应当相信什么：在中心论点中写出最希望读者接受的一项结论。贡献尚未获批准；为当前论文能够支持的每项贡献各写一条，数量不限，并记录其为核心、辅助还是可选，以及证据变化时能否弱化或删除。

### Central thesis — unresolved

TODO: state the single most important conclusion the paper wants readers to accept.

### Contributions

No contributions have been approved yet. Add one entry per contribution that
the current paper can defend; there is no required number of contributions.

For each contribution, record whether it is central, supporting, or optional and whether it may be weakened or removed if the evidence changes.

## What must not change silently

本节只记录影响重大的承诺，例如：

- 中心主张的科学内涵；
- 主要比较或公平性条件；
- 主叙事脉络；
- 得出诚实结论所必需的限制或负面结果；
- 稳定论文接口（例如 `\MainResult{}`）的含义。

为每项锁定主张链接证据：`.agents/memory/project/experiments.md` 中的问题及其对应的 `assets/MANIFEST.yaml` 条目。证据仍处于计划阶段时必须明确说明，绝不能将计划中的结果写成观察结果。

当前锁定项：

Current locked items:

- TODO

## What may evolve

记录 Agent 无须反复请求批准即可继续工作的有界范围。请用具体语言描述边界，不要只写“酌情调整”。局部句子措辞可自由调整，但不得改变主张强度或科学含义。

- 引言示例和段落边界：可自由调整，但不得改变主要框架。
- Local sentence wording: free unless it changes claim strength or scientific meaning.
- TODO

## Unresolved

这是工作队列，不是失败清单。明确保留候选方案和不确定性，包括候选标题、中心论点、目标受众与投稿场所的适配。Agent 应优先进行低风险、可逆的工作，并以简明决策包将重大选择交给 Human。

- TODO: title candidates
- TODO: central thesis
- TODO: target audience and venue fit

## Story and structure

在此记录叙事结构与各节职责。

### Narrative arc — unresolved

TODO：描述偏好的叙事推进方式，例如问题 → 缺口 → 洞见 → 方法 → 证据。

### Section responsibilities

| 章节 | 读者任务 | 必须保留 | 可调整内容 |
|---|---|---|---|
| 摘要 | TODO | TODO | 措辞和压缩 |
| 引言 | TODO | TODO | 示例和段落边界 |
| 相关工作 | TODO | TODO | 分组和顺序 |
| 方法 | TODO | TODO | 局部解释顺序 |
| 实验 | TODO | TODO | 已批准问题范围内的呈现顺序 |
| 结论 | TODO | TODO | 已批准主张范围内的压缩与强调 |

## Writing style

描述具体选择，而不只是“清晰”或“专业”等形容词。提供一些可供 Agent 一致应用的正反例，包括定位和语气、解释密度、主张强度、偏好的段落推进方式及应避免的术语；仅在目标投稿场所确定且当前规则经核实时加载该场所的补充风格。

### Current style — unresolved

- Positioning and voice: TODO
- Explanation density: TODO
- Claim-strength discipline: TODO
- Preferred paragraph moves: TODO
- Terms or expressions to avoid: TODO
- Venue-specific overlay: TODO; load only when the target venue is active and current rules have been verified.

## Human decisions required

以下事项最终由 Human 负责：

- 核心贡献和主张；
- 某项主张是否可以弱化、删除，或需要更多实验；
- 主要叙事和论文定位；
- 主要指标、基线、评估公平性和结果解释；
- 稳定论文接口含义的变更；
- 最终发布批准。

请 Human 决定之前，Agent 应先获取相关背景、受影响章节、备选方案和风险。
