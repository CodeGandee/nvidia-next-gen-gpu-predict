---
title: "从历史时点可知信息到 Feynman：NVIDIA 数据中心 GPU 规格决策的定量重建与条件预测"
authors:
  - name: "nvidia-survey 研究组"
language: zh-CN
paper_line: nvidia-next-gen-dc-gpu-v2-final
structure_profile: mechanism-first-temporal-decision-survey
taxonomy_version: v2-final-r1
problem_taxonomy:
  - workload-demand-pressure
  - physical-and-supply-feasibility
  - system-bottleneck
  - economic-and-delivery-risk
  - small-sample-identifiability
solution_taxonomy:
  - compute-and-numeric-format
  - on-chip-memory-and-hbm
  - scale-up-and-scale-out-interconnect
  - packaging-and-stacking
  - power-and-cooling
  - ras-confidential-computing-and-mig
  - statistical-bayesian-and-engineering-models
design_dimensions:
  - hierarchy
  - mechanism
  - resource
  - decision-time-observability
  - continuous-or-discrete-action
  - hardware-placement
  - evidence-depth
lecture_sections: []
---

## 摘要

章节任务：用一个自洽段落给出对象、历史时点截断、三路模型、统计拒绝、条件工程预测和主要限制。

## 引言

章节任务：说明为什么“当时能看到什么”比事后趋势拟合更关键，提出总问题、界定读者、贡献与有界 survey necessity。

## 调查边界、证据与时间因果

章节任务：定义 34 项材料、16 篇全文论文、证据截止日、公开时间与目标世代；解释双时间戳和答案隔离，明确不使用 v1。

### 十项问题与回答姿态

章节任务：将 q01--q10 映射到后续章节，保留 6 项 covered、4 项 partial/weak 的审计结果。

### 层级、口径与不确定性语言

章节任务：统一 GPU/板卡/节点/机架、稠密/稀疏、精度、单双向带宽、TDP 与机架功率；定义“官方披露”“来源事实”“研究解释”“模型条件输出”和“未知”。

## 需求与可行域：规格问题的两套分类

章节任务：先给问题分类，再给解决机制分类，避免按产品名或论文清单组织。

### 共同数学语言

章节任务：定义世代 $g$、规格代理时点 $\tau_g$、当时信息集 $I_g$、可行域 $F_g$、连续规格向量 $y_g$、离散特性 $h_g$、多目标效用 $U$、风险项 $R$ 与条件架构 $a$；说明哪些量可观察、可估计、仅为假设或保持未知。

### 需求问题分类

章节任务：训练计算、参数/激活/KV 容量、内存流量、MoE/张量并行通信、延迟与集群交付压力。

### 供给与物理约束分类

章节任务：制程/光罩/晶体管、HBM、先进封装、互连、功率/散热、良率/供应与软件成熟度。

### 解决机制分类

章节任务：计算与数值格式、存储层次、HBM、互连、封装/堆叠、系统供电散热、RAS/机密计算/MIG。

## 历史公开信息与规格演化

章节任务：按机制与约束变化解释 Volta--Rubin 的规格标签和公开时序；图表不宣称内部冻结日。

### 工作负载信号如何进入规格选择

章节任务：用 AlexNet、Transformer、T5、GPT-3、Switch、Llama 2、DeepSeek、FlashAttention、Megatron 与 MegaBlocks 说明计算、容量、带宽和互连需求。

### 制程、HBM、封装与互连如何移动可行域

章节任务：用 TSMC 报告、NVIDIA 架构资料、HBM4 公开材料与 GPGPU 论文说明供给侧变化和证据限制。

## 从公开观测到规格：三路数学模型

章节任务：定义共同符号、可行域、多目标决策、预测影响图与工程包络；任何方程都必须定义符号和假设。

### 共同决策框架

章节任务：给出信息集、可行域、效用/风险、观测模型和模型资格门槛。

### 路线 A：历史统计外推及其拒绝

章节任务：呈现 18 个变体、30 个 lead/variant 单元和无合格中心；解释为何不能发布统计中心或覆盖概率。

### 路线 B：贝叶斯预测影响图

章节任务：呈现条件连续规格、离散特性、根节点主观性、投影到规格网格和校准不足；明确它不是内部决策网络。

### 路线 C：可行域约束的工程设计空间

章节任务：呈现 3 个时点、5 个架构、5 组目标、每条件 1024 抽样，以及工程工作点、条件带和外包络的语义。

## 小样本识别、回测与拒绝

章节任务：比较三路模型的输入、输出、可检验性、基线和失败；让负结果成为结论核心。

### 为什么没有统计中心

章节任务：给出折数不足、相对朴素基线的误差和非可辨识性证据。

### 条件概率能说什么、不能说什么

章节任务：给出 Route B 的 MALE/Brier 事实和 58.33% 显式假设下限；避免把条件概率写成真实采用概率。

### 工程包络如何补充而非替代统计识别

章节任务：解释 Route C 的可行性筛选、目标权重与架构敏感性以及不具备联合 BOM 的限制。

## 当前观测与 Feynman 官方边界

章节任务：把 GTC 2026 的官方披露与数值未知分栏；说明 Die Stacking、Custom HBM、Rosa、BlueField-5、NVLink 8 CPO 与 Spectrum-7 的系统含义。

## 下一代数值规格：工作点、条件带与外包络

章节任务：逐项给出 24 个月 balanced/unresolved 工程工作点、同条件 q10/q90 与跨 25 条件外包络；解释为何三者不等于“最可能值/置信区间”。

### 计算与晶体管

章节任务：晶体管、SM 与 dense FP4；不与 Route B 原生低精度代理量合并。

### HBM 容量与带宽

章节任务：容量、带宽、堆栈/封装条件及上界堆积。

### NVLink、TDP 与机架

章节任务：双向 NVLink、单 GPU TDP、机架 GPU 数和机架功率；解释电源与冷却的系统依赖。

## 硬件特性：官方披露、条件判断与反证

章节任务：三栏呈现“官方已披露”“证据支持的工程假设”“仍未解决”。

### 堆叠与多裸片拓扑

章节任务：官方 Die Stacking 不等于多计算裸片；4x1 为工作拓扑，4x2 仅为压力上界。

### Custom HBM、存储层次与数值格式

章节任务：说明 12--16 堆栈是工程条件而非官方数字；新格式采用判断受 Brier 退化约束。

### CPO、RAS、机密计算与系统平台

章节任务：系统级 CPO 为官方路线，GPU 封装内 CPO 保持未解决；增强 RAS/机密计算仅作平台连续性推断。

## 条件权衡、反证与更新规则

章节任务：逐项写出改善资源、代价、依赖条件、失败条件和未来公开信息触发的更新。

## 研究缺口与方法含义

章节任务：从无合格统计中心、根变量主观性、缺失 die area/defect/bond-yield/thermal-resistance 和零/单正例特性推导下一步证据需求。

## 局限

章节任务：集中呈现样本数、公开代理、部分来源、语义不一致、条件区间、联合可制造性与外推限制。

## 结论

章节任务：综合可支持的历史决策逻辑、模型资格、Feynman 数值工作点/范围、硬件特性边界和最关键的可证伪条件。

## 参考文献

章节任务：由 Citation Map 解析全部读者可见引用；每个具名来源和来源特定表格行均可独立追溯。

## 附录：十项问题覆盖矩阵

章节任务：用短表给出 q01--q10 的章节定位、回答姿态和限制。

## 附录：模型与来源可复核信息

章节任务：记录答案隔离面板哈希、三路输出哈希、r1/r2/r3 命名映射、34 项材料状态和预测更新登记格式，不暴露内部提示或代理过程。
