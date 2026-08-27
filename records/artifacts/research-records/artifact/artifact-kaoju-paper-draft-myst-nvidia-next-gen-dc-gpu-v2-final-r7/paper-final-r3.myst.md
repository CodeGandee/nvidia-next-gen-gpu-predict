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
keywords:
  - NVIDIA
  - 数据中心 GPU
  - Feynman
  - 规格预测
  - 时间顺序回测
  - 可行域
  - 贝叶斯影响图
---

## 摘要

本文研究的不是“按历代增速猜下一代”，而是一个带时间因果约束的问题：在每一历史世代的规格代理决策时点之前，公开观察者能够看到哪些工作负载、制程、HBM、封装、互连、功耗与软件信号；这些信号如何移动可行域并改变联合规格选择；同一方法在滚动历史留出中是否优于朴素基线。证据库含 34 项材料，其中 16 篇学术论文均完成全文研读，32 项来源就绪，TSMC 2026 技术材料与 JEDEC HBM4 材料因访问粒度受限保留为部分证据。我们在一个答案隔离的 9 事件历史面板上比较三条不可混合的路线，并公开报告输入、拟合、逐折误差、拒绝理由和约束敏感性。路线 A 预声明 6 个指标×3 种解释变量组合：8 个变体在拟合前因无可评分折而拒绝，10 个完成拟合；后者形成的 30 个“变体×前置期”资格单元全部失败，故不发布统计中心。路线 B 的六折回测揭示 12 个目标根变量中 7 个仍依赖显式假设，且低精度代理的平均绝对对数误差为 0.982；它只用于敏感性和影响方向，不代表 NVIDIA 内部决策网络。路线 C 在 3 个时点、5 个架构条件与 5 组目标权重上形成 75 个条件，每条件抽样 1024 次，并显式枚举封装、良率、HBM、SerDes、功耗、热与机架约束。其 24 个月、balanced、架构未决条件给出的边际工程工作点为：471.8B 晶体管、296 SM、768 GB HBM、45.3 TB/s HBM 带宽、43.4 PFLOP/s 稠密 FP4、9.18 TB/s 双向 NVLink、2.6 kW 单 GPU、72 GPU 与 323 kW 机架；这些数值不是最可能值，同条件 q10/q90 不是置信区间，跨 25 条件外包络也没有覆盖概率。GTC 2026 对 Feynman 的官方边界仅包括 2028 路线图位置、Die Stacking、Custom HBM、Rosa CPU、BlueField-5、NVLink 8 CPO、Spectrum-7 204T CPO 与 ConnectX-10，并未披露任何 GPU 数值规格。全文据此把可支持结论、条件工程判断与未知严格分开，并给出逐项反证和更新规则。

## 结论先行：Feynman 规格预测

**结论先行：Feynman 下一代数据中心 GPU 的条件参数预测。** 主预测置顶，两个较低权重的工程情景、低置信影响图诊断和被回测拒绝的统计路线依次列后；后文再解释模型、证据和反证理由。

| 排序与模型 | 晶体管 / SM | HBM 容量 / 带宽 | 计算 / NVLink | 单 GPU TDP | 机架 GPU / 功率 | 资格与含义 |
|---|---:|---:|---:|---:|---:|---|
| 主预测（首选）；C：24m、balanced、架构未决 | 471.8B / 296；413–508B / 248–336 | 768 GB / 45.3 TB/s；576–1024 / 33.5–50.7 | FP4 43.4 PF / 9.18 TB/s；35.7–52.6 / 8.28–10.07 | 2.6 kW；2.6–3.0 | 72 / 323 kW；72–144 / 290–511 | 首页主结论；前者为条件 q50，后者为同条件 q10–q90。 |
| 次级情景 1；C：2T–1L | 311.2B / 192 | 576 GB / 33.2 TB/s | FP4 34.7 PF / 9.18 TB/s | 2.2 kW | 144 / 448 kW | 芯片/卡级收缩，但以更高机架密度补偿；2T 的模型内边际频率仅 16.8%。 |
| 次级情景 2；C：4T–2L | 908.5B / 584 | 768 GB / 44.0 TB/s | FP4 44.2 PF / 9.17 TB/s | 2.6 kW | 72 / 320 kW | 双主动层压力上界；2L 的模型内边际频率仅 8.3%。 |
| 低置信诊断；B：影响图 | 672B / — | 576 GB / 56 TB/s | 低精度代理 200 PF / 7.2 TB/s | 2.8 kW | — / — | 7/12 根为假设；只作敏感性诊断，不是可发布中心。 |
| 回测拒绝；A：环境回归 | — / — | — / — | — / — | — | — / — | 0/30 资格单元合格，不发布任何参数。 |

读表规则：24m 指 2026-03-20 信息截点。路线 C 分位数没有历史覆盖概率；16.8% 与 8.3% 是模型内边际选择频率，不是 NVIDIA 采用概率。路线 B 的低精度代理不等同于稠密 FP4，也不得与路线 C 平均。官方 Feynman GPU 数值规格截至证据冻结日仍为 0 {cite}`nvidia2026feynman`。

## 引言

数据中心 GPU 的公开规格具有强烈共趋势：晶体管、低精度吞吐、HBM 容量、互连带宽和系统功率大体随世代上升。把这些曲线外推很容易得到一个数字，却不能回答 NVIDIA 为什么在某一代选择那组数字，也无法判断预测是否偷看了发布后的信息。真正困难之处在于，产品公开日并非内部规格冻结日，公开观察者又看不到客户组合、成本、良率、采购合同和目标权重。因而，任何声称复原“内部公式”的模型都超出了证据。

本文把总问题改写为公开观察者可检验的形式：给定世代 $g$ 的规格代理时点 $\tau_g$，只允许公开时间早于 $\tau_g$ 的信息进入模型；在此信息集上重建需求压力、物理与供应可行域、系统瓶颈和交付风险；再以时间顺序样本外误差决定模型是否有资格发布数值中心。这个形式借鉴逆向优化从观测选择反推目标函数的思路，但同时承认只有在可行域、选择机制和足够多独立选择都被识别时，目标权重才可恢复 {cite}`keshavarz2011inverse`。在极小代际样本下，收缩或先验可以稳定计算，却不能创造缺失信息。

本文有四项主要贡献。第一，建立双时间戳边界，把事件发生、公开可得、代理截点和目标结果分离。第二，以“需求问题—可行约束—联合响应”的机制分类统一 Volta 至 Rubin 的公开材料，而不是按来源逐篇摘要。第三，用同一历史面板并列检验统计、影响图和工程可行域三条路线，明确何时必须拒绝预测。第四，在统计中心被拒绝后，仍给出具名条件下可复算的 Feynman 工程工作点、敏感性范围与反证登记，而不把工程区间包装成概率覆盖。

本文面向熟悉 GPU、LLM 系统和基本统计建模的体系结构研究者、平台架构师与容量规划者。结论是带明确条件和反证规则的研究情景，不是采购建议或 NVIDIA 产品事实；证据冻结日为 2026-08-27。

## 调查边界、证据与时间因果

证据总体包含 34 项：16 篇学术论文、13 份技术报告、3 个数据集、1 个模型和 1 项标准。16 篇论文均已全文研读并形成来源摘要；34 项中 32 项为 ready，TSMC 2026 A14/A16 相关研讨会材料和 JEDEC HBM4 材料因只能获得有限公开内容而标记 partial，二者只支持方向性工艺或接口事实，不支持 NVIDIA 采用、量产良率或具体 Feynman 数字。证据清单的数量、类型和状态见下图。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig01-evidence-inventory-r1}}

历史面板为每条记录保存四个时间概念：事件时间 $t^{event}$、首次公开可得时间 $t^{public}$、本次采集时间 $t^{collect}$ 和适用世代。只有满足 $t^{public}<\tau_g$ 的变量才可进入 $I_g(\tau_g)$。内部冻结日未知，因此 $\tau_g$ 不是事实，而是发布日前 18、24、30 个月的代理窗口；主工程对照采用 24 个月，18 和 30 个月用于敏感性。Feynman 的 24 个月截点为 2026-03-20，早于 2026-04-07 的 GTC 2026 路线图公开日，所以该披露只用于“当前官方边界”，绝不倒灌历史输入。历代公开日和代理截点见下图；图中的线表示分析截断，不表示 NVIDIA 的内部冻结日。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig02-historical-timeline-r1}}

历史标签和预测目标物理隔离：面板含 9 个历史事件、36 个已接受观测、43 个已接受标签和 27 个时点冻结行；Feynman 行没有数值标签，也没有特性结果标签。面板仍有 39 个预测变量空单元，空缺不以事后答案填补。这个设计使“现在知道的产品结果”不能通过同一字段意外进入预测输入。

### 十项问题与回答姿态

调查由十项有序问题组成，最终审计结论为 6 项 answered、4 项 partial。这里的“partial”不是未完成写作，而是证据边界本身：内部冻结日、私有目标函数、校准的未来分布和若干特性标签尚不可识别。

| 问题 | 核心问题 | 当前姿态 | 最短结论 |
|---|---|---|---|
| q01 | 历史规格时点及当时可见信息 | partial | 内部冻结日未知；以 18/24/30 个月代理构造公开信息集。 |
| q02 | LLM/HPC 需求如何量化 | answered | 至少需训练计算、token/上下文、KV cache、激活参数、MoE 通信、prefill/decode、低精度稳定性和并行拓扑。 |
| q03 | 技术与供应可行域如何量化 | answered | 制程、封装、HBM、SerDes、供电、冷却、机架功率、供应和软件成熟度需联合约束。 |
| q04 | 历代实际选择了哪些规格 | answered | 统一到 chip/card/node/rack 层级的 43 个标签，不混用精度与带宽口径。 |
| q05 | 哪个受约束决策模型最能解释选择 | partial | 可恢复公开观察者决策管线，不能恢复 NVIDIA 私有效用函数。 |
| q06 | 小样本如何识别与量化不确定性 | answered | 时间回测、收缩和显式拒绝优先；先验不替代数据。 |
| q07 | 是否稳定优于朴素基线 | answered | 否；路线 A 没有任何统计合格中心。 |
| q08 | 当前输入与情景是否外推 | answered | 24 个月为主对照；18 个月右删失，当前信息整体位于高压外推区。 |
| q09 | 下一代规格分布是什么 | partial | 只能给路线 C 条件边际分位数和外包络，不能给有覆盖率的后验分布。 |
| q10 | 新硬件特性的采用概率是什么 | partial | 只保留影响图诊断和反证；不发布已校准采用概率。 |

### 层级、口径与不确定性语言

同名指标只有在层级和语义一致时才能比较。本文以 chip 表示逻辑芯片或多裸片逻辑总和，以 card 表示单个 SXM/加速器封装，以 node 表示 8 GPU 基本系统，以 rack 表示 72 或 144 GPU 平台。低精度吞吐必须同时注明数值格式、稠密或稀疏以及峰值或交付代理；NVLink 统一为单 GPU 双向总带宽；TDP 是单 GPU/加速器的报告功率包络，不等于墙上功率；机架功率另含 CPU、网络、内存、转换和冷却开销。

| 标签 | 在本文中的含义 | 允许的语言 |
|---|---|---|
| 官方披露 | 可由 NVIDIA 一手公开材料逐字定位的产品或路线图事实 | “官方列出”“官方披露” |
| 来源事实 | 论文、标准或供应商材料直接支持的事实 | “来源报告”“标准定义” |
| 研究解释 | 多来源机制综合，未声称为内部因果 | “证据支持的解释” |
| 模型条件输出 | 给定模型、时点、架构和权重后的计算结果 | “条件工程工作点/条件分位数” |
| 未知 | 公开证据不能区分或尚无可校准样本 | “未披露”“不可识别”“保持未决” |

全文禁止把工程 q10/q50/q90 称为 80%、90% 置信区间、可信区间或预测区间，也禁止对三条路线取平均、交集或所谓共识中心。

## 需求与可行域：规格问题的两套分类

规格形成不是“工作负载需要什么”单方面决定，也不是“制造能做什么”单方面决定。第一套分类描述需求侧压力：训练计算、模型状态与 KV 容量、内存流量、MoE/张量并行通信、延迟和集群交付。第二套分类描述解法与约束：计算格式、片上存储、HBM、scale-up/scale-out、封装堆叠、供电散热、RAS 和隔离。二者之间由可行域和多目标选择连接。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig03-demand-resource-map-r1}}

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig04-taxonomy-matrix-r1}}

### 共同数学语言

令 $g$ 为产品世代，$\tau_g$ 为该世代的公开观察者规格代理时点，$I_g(\tau_g)$ 为当时可见信息集。把连续规格写为

$$
y_g=(T_g,S_g,C_g,B_g,L_g,P_g,N_g,W_g),
$$

其中 $T_g$ 是晶体管数，$S_g$ 是启用 SM 数，$C_g$ 是单卡 HBM 容量，$B_g$ 是 HBM 带宽，$L_g$ 是单 GPU 双向 scale-up 带宽，$P_g$ 是单 GPU 功率包络，$N_g$ 是机架 GPU 数，$W_g$ 是机架功率。离散特性向量 $h_g$ 包含数值格式步进、多计算裸片、主动逻辑堆叠、HBM 代际步进、NVLink 代际步进、功率平滑和 CPO 放置等选择。$a$ 表示架构条件，例如横向计算 tile 数与主动逻辑层数。

信息集可分为需求代理 $d_g$、供给/技术代理 $z_g$ 与平台/商业代理 $p_g$：

$$
I_g(\tau_g)=\{d_g,z_g,p_g: t^{public}<\tau_g\}.
$$

公开观察者的共同决策抽象为

$$
(y_g,h_g)=\underset{(y,h)\in F_g(I_g,a)}{\operatorname{argmax}}\; U(y,h;d_g,w_g)-\lambda_g R(y,h;z_g,p_g),
$$

其中 $F_g$ 是由制程、封装、HBM、互连、功率、冷却与系统条件共同形成的可行集合；$U$ 是工作负载效用；$w_g$ 是计算、容量、带宽、互连、生命周期等目标权重；$R$ 是良率、成本、供应、软件与进度风险代理；$\lambda_g\ge 0$ 是风险惩罚强度。公开资料能观察 $y_g$ 的部分发布标签和 $I_g$ 的若干代理；$F_g$ 只能近似；$w_g$、$\lambda_g$、绝对成本与 NVIDIA 内部效用保持未知。逆向优化只能在这些结构被充分约束时推断显露偏好，因此本文不把上式当成已识别的 NVIDIA 公式 {cite}`keshavarz2011inverse`。

Roofline 给出解释资源瓶颈的最小模型：若算术强度为 $A$，峰值计算为 $\Pi$，内存带宽为 $B$，则可实现性能上界 $P_{attainable}=\min(\Pi,BA)$；增加 Tensor Core 峰值在带宽受限区不会等比例转化为应用性能 {cite}`williams2009roofline`。该关系解释为何 GPU 世代需要同时调整计算、片上复用、HBM 和互连，而不能只最大化一个指标。Accel-Sim 一类经过校验的模拟框架说明微架构与工作负载相互作用可以被定量研究，但本文没有把模拟器误用为尚未公开的 Feynman 绝对性能证据 {cite}`khairy2020accelsim`。

### 需求问题分类

训练需求可粗分为总计算和时间预算：参数量并不是唯一尺度，token 数、序列长度、激活重计算、优化器状态、并行效率和容许训练时长共同决定有效 FLOP。推理则要区分 prefill 的矩阵吞吐与 decode 的容量、带宽和延迟；长上下文扩大 KV cache，MoE 把参数容量与每 token 激活计算解耦，却引入 all-to-all 和负载不均衡。公开模型数据只能构造压力代理，不能代表 NVIDIA 的客户 workload mix。

从 AlexNet 的卷积训练开始，GPU 上高密度矩阵计算成为可观察的需求信号 {cite}`krizhevsky2012alexnet`。Transformer 以注意力和前馈层为核心，把长序列、矩阵乘和跨设备并行推到前台 {cite}`vaswani2017attention`；T5 将统一文本到文本训练和更大预训练规模变成公开参照 {cite}`raffel2020t5`；GPT-3 展示了大规模 dense 自回归模型的训练计算与模型状态压力 {cite}`brown2020gpt3`；Switch Transformer 通过稀疏专家提高参数规模，同时使 token 路由与跨设备通信成为体系结构变量 {cite}`fedus2021switch`；Llama 2 提供开放权重规模和上下文的另一类可核验锚点 {cite}`touvron2023llama2`。

近期系统研究进一步改变需求向量。Megatron-LM 表明张量、流水和数据并行的组合决定通信形态 {cite}`narayanan2021megatron`；FlashAttention 通过 I/O 感知分块减少 HBM 访问，说明片上存储和数据搬运算法可改变有效带宽需求，而不是简单服从序列长度外推 {cite}`dao2022flashattention`；MegaBlocks 以块稀疏执行缓解 MoE 动态性，说明软件调度成熟度必须与硬件格式和通信共同建模 {cite}`gale2023megablocks`。DeepSeek-V3 的 MoE 训练报告提供了 2024 年底之前可见的计算、通信和低精度信号 {cite}`deepseek2024v3`；DeepSeek-V4 代表证据冻结点附近更新的模型设计，但只能进入相应晚时点情景，不能倒灌早期世代 {cite}`deepseek2026v4`。Epoch AI 的模型趋势数据和 MLPerf Training v6.0 结果可用于校验当前计算规模与系统扩展趋势，但二者都不是 NVIDIA 的需求权重 {cite}`epoch2026models` {cite}`mlperf2026training`。

### 供给与物理约束分类

供给侧首先决定 $F_g$ 的边界。制程节点与逻辑密度影响可容纳的晶体管，但实际产品还受光罩、裸片面积、缺陷密度和设计规则约束；先进封装扩展总逻辑与 HBM 边缘，却增加封装面积、互连能耗、装配良率和供应风险。TSMC 2017 与 2020 年报能证明当时公开的制程和先进封装发展方向，却不能证明 NVIDIA 的具体采用日期或成熟良率 {cite}`tsmc2017annual` {cite}`tsmc2020annual`。TSMC 2026 A14/A16 相关材料在本调查中仍属部分来源，只用作未来可行域方向，不进入绝对良率或 Feynman 节点断言 {cite}`tsmc2026a13`。

HBM 的约束至少包含每 stack 容量、pin 速率、stack 数、控制器/PHY 边缘、封装面积、功耗和供给。JEDEC HBM4 公开信息支持接口演进方向，但本调查未取得足以支撑 NVIDIA 产品数字的完整标准证据，所以 HBM4 不能直接决定 Feynman 的 12/16 stack、容量或带宽 {cite}`jedec2025hbm4`。NVIDIA 公开的 NVHBM 概念描述定制 base die 通过 NVLink Fusion 面向 custom XPU，它说明“定制 HBM”存在一种系统实现路径，却不是 Feynman GPU 的规格披露 {cite}`nvidia2026nvhbm`。

功率和冷却同时约束单卡与机架。提高 $P_g$ 可能换取更多计算和 I/O，但机架功率 $W_g$ 还由 GPU 数 $N_g$、CPU、交换、存储、VRM 损耗和冷却系数共同决定。因而 2.6 kW 单 GPU 与 323 kW 机架工作点不是简单的 $72\times2.6$；144 GPU 情景更不能在不改变供电、液冷和瞬态控制的情况下线性复制。

### 解决机制分类

计算机制包括 Tensor Core、混合精度、稀疏与专用数据搬运；存储机制包括寄存器、共享内存/L1、L2、压缩和 HBM；通信机制包括片内网络、裸片间互连、NVLink scale-up 与网络 scale-out；集成机制包括多裸片、2.5D/3D 堆叠和定制 base/I/O die；平台机制包括供电、直接液冷、功率平滑、故障隔离、MIG、机密计算和 RAS。分类矩阵的核心含义是：同一个需求压力通常需要多层协同响应，而同一个硬件特性也会引入新的成本与失败模式。

## 历史公开信息与规格演化

Volta V100 把第一代 Tensor Core、FP16 矩阵计算、HBM2 和 NVLink 2 组合成训练加速平台，说明早期深度学习需求并非只以更多 CUDA core 响应 {cite}`nvidia2017volta`。Ampere A100 增加 TF32、BF16、结构化稀疏、HBM2e、NVLink 3 与 MIG，把训练易用性、推理密度、内存带宽和多租户隔离放进同一产品 {cite}`nvidia2020a100`。Hopper H100 以 FP8 Transformer Engine、HBM3、NVLink 4 和 Tensor Memory Accelerator 回应大型 Transformer 的低精度稳定性、数据搬运和规模化通信 {cite}`nvidia2022hopper`。

Blackwell 把优化边界进一步推向封装与机架：B200 采用多裸片封装、新一代 Tensor Core/FP4、HBM3e 与 NVLink 5；第三方体系结构分析可帮助理解其片上与系统结构，但不能替代官方规格口径 {cite}`luo2025blackwell`。Blackwell Ultra 延续这一平台方向，以更大 HBM 和高密度液冷系统面向 reasoning、长上下文与机架级部署 {cite}`nvidia2025blackwellultra`。Rubin 的公开材料已经按 Vera CPU、GPU、HBM、NVLink、网络和机架描述整个平台，显示规格选择单元从芯片扩大到交付系统 {cite}`nvidia2026rubin`。NVIDIA FY2026 年报提供需求、供给集中、资本和平台业务背景，但财务披露不能识别某一规格的内部权重 {cite}`nvidia2026annual`。

从 2013 至 2026 的产品发布编年数据用于统一公开日期和产品层级，而不是把营销发布时间当成冻结日 {cite}`nvidia2013to2026chronology`。2025 年公开路线图提供当时可见的代际顺序，GTC 2026 材料则更新了 Feynman 平台标签；两者属于不同公开时点，必须分别进入相应信息集 {cite}`nvidia2025roadmap`。历史压力与联合响应的机制时间线如下。

### 工作负载信号如何进入规格选择

历史映射不是“某篇模型论文导致某颗 GPU”，而是把公开信号压缩为资源压力。训练 FLOP、低精度稳定性和时间预算提高计算边际效用；参数、优化器状态、激活和 KV cache 提高容量压力；长序列、低复用 decode 与稀疏路由提高 HBM/片上存储压力；张量并行、专家路由和更大 failure domain 提高 NVLink、网络与 RAS 压力。随后必须经过供给侧可行域，才能形成规格选择。

例如，FlashAttention 降低注意力的 HBM 流量，会减弱“序列长度必然等比例要求 HBM 带宽”的朴素关系；MoE 又可能降低每 token 的激活计算却增加通信和总参数容量。因此本文只把模型论文作为可日期化的压力代理，并保留软件算法能够改变硬件需求弹性的路径，不把参数量或训练 FLOP设为单一决定变量。

### 制程、HBM、封装与互连如何移动可行域

制程密度提高可扩大单裸片逻辑上限，多裸片与先进封装则绕开单一光罩/良率约束；但总晶体管扩张会同时推高跨裸片通信、封装面积、热流密度和装配风险。HBM 代际和 stack 能力扩展容量/带宽，却消耗封装边缘和功率；NVLink 提高 scale-up 带宽，又会增加 SerDes、交换与光电层级的设计负担。因而历代联合响应可被解释为“需求压力使某些资源的边际效用上升，供给进步移动可行域，平台交付风险再过滤候选”，而不是任一外生变量的固定倍数映射。

## 从公开观测到规格：三路数学模型

三条路线共享时间截断和历史标签，却回答不同问题。路线 A 检验环境变量能否在历史上形成合格的统计预测中心；路线 B 检验公开代理和显式假设如何沿影响图传播到规格网格与特性节点；路线 C 在预声明物理和系统约束内枚举工程设计空间。它们的输出语义不可互换，也不能平均。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig05-decision-pipeline-r1}}

### 共同试验协议与评分定义

三路正式试验读取同一份答案隔离的 9 事件历史面板，目标 Feynman 的数值规格和特性结果字段均为空。所有历史输入遵守 `public_available_date < cutoff_date`，输出文件在同一 CPU、Python 3.12.14、随机种子 20260827 和无网络条件下生成；总执行时间 92.866 秒，其中 A、B、C 分别为 0.758、0.546、90.982 秒。共同之处止于数据边界与可复算执行；三路不共享似然、先验或“置信度”。

| 项目 | 路线 A | 路线 B | 路线 C |
|---|---|---|---|
| 问题 | 历史环境变量能否预测规格增速 | 压力与公开假设如何传播到规格/特性 | 哪些离散设计在工程约束下最优 |
| 历史评价 | rolling-origin；18/24/30m | 6 个严格时点留出折 | 4 个已知平台 sanity check |
| 计算量 | 18 变体；4096 后验抽样/折 | 4000 抽样/回测折；20000 目标抽样 | 75 条件×1024 技术抽样 |
| 主要分数 | MALE、CRPS、覆盖、方向、OOD | 连续 MALE/覆盖；特性 Brier | 可行率、约束绑定、条件分位数 |
| 发布规则 | 必须同时通过全部资格门槛 | 只作诊断，不作已校准采用概率 | 只发布具名条件工程工作点 |

三类分数统一按实际可评分的历史留出数 $n$ 计算，且数值越低越好。对正的连续规格，平均绝对对数误差定义为 $\operatorname{MALE}=n^{-1}\sum_{i=1}^{n}\lvert\log \hat y_i-\log y_i\rvert$；例如 MALE 0.10 对应约 $e^{0.10}-1=10.5\%$ 的典型乘法偏差，MALE 0.69 约对应 2 倍。若 $F_i$ 是预测累积分布函数，则 $\operatorname{CRPS}=n^{-1}\sum_i\int[F_i(z)-\mathbf{1}\{y_i\le z\}]^2\,\mathrm{d}z$，它同时惩罚错误中心和错误区间 {cite}`gneiting2007scoring`。对二元特性，Brier score 为 $n^{-1}\sum_i(p_i-o_i)^2$。CRPS 有目标量纲，只能在同一指标、同一前置期和相同结果尺度内比较；留出折不足时，任何看似低的均值都不能补足统计资格。严格留未来评估遵循 leave-future-out 原则 {cite}`burkner2020lfo`。

### 路线 A：历史环境回归如何拟合、如何失败

#### 响应、解释变量与先验

对规格指标 $k$ 的相邻公开世代转移 $g-1\rightarrow g$，路线 A 先计算年化对数增长

$$
r_{gk}=\frac{\log y_{gk}-\log y_{g-1,k}}{\Delta t_g},\qquad r_{gk}=\alpha_k+x_g^\top\beta_k+\varepsilon_{gk},
$$

其中 $x_g$ 是在目标截点前公开、按训练折中位数与稳健尺度标准化的环境变化率。截距 $\alpha_k$ 围绕训练折的中位年化增长收缩，精度为 0.5；环境斜率的高斯 ridge 精度为 4.0；残差方差采用 shape 2.5 的 inverse-gamma 先验，年化 log-scale 下限为 0.05。高斯似然与共轭更新产生参数后验，并把下一世代的预测变换回对数规格上的 Student-$t$ 分布；每折 4096 次后验抽样用于 CRPS 与覆盖评分。一个预测变量至少需要 3 个训练转移，两个变量为保证自由度实际至少需要 4 个，即 $\max(3,p+2)$。

三个基线与模型使用完全相同的留出折：M0 沿用上一代规格；M1 以训练折中位 log-drift/CAGR 外推；M2 使用 $\theta=0.63$ 的集成移动平均式 log-drift。某个“变体×前置期”只有在至少 3 折、MALE 与 CRPS 都优于各自最佳基线、CRPS 在多数折改善、任何单折占正向 CRPS 改善不超过 80%、经验 90% 覆盖至少 $2/3$，且无稳健标准化距离大于 4 或 ridge 杠杆超过 $4(p+1)/n$ 的留出点时才合格。该规则在看结果前固定，未按 Feynman 输出选择变体。

#### 18 个变体究竟拟合了什么

六个目标各有三种变体：`mechanism-supply` 只使用与目标同机制的供给代理，`workload-demand` 只使用公开前沿训练计算的对数代理，`demand-plus-supply` 同时使用二者。下表中的“历史折”是跨 18/24/30m 可构造的实际滚动留出折总数；0 表示在任何前置期都无法形成一次合法拟合，而不是“拟合后被统计拒绝”。

| 目标规格 | 变体 | 解释变量 | 历史折 | 执行结果 |
|---|---|---|---:|---|
| 单卡功率 | mechanism-supply | card power envelope | 0 | 拟合前拒绝 |
| 单卡功率 | workload-demand | frontier training compute | 7 | 完成 |
| 单卡功率 | demand-plus-supply | demand + card power envelope | 0 | 拟合前拒绝 |
| 启用 SM | mechanism-supply | logic density | 5 | 完成 |
| 启用 SM | workload-demand | frontier training compute | 7 | 完成 |
| 启用 SM | demand-plus-supply | demand + logic density | 2 | 完成 |
| HBM 带宽 | mechanism-supply | per-stack HBM bandwidth | 0 | 拟合前拒绝 |
| HBM 带宽 | workload-demand | frontier training compute | 5 | 完成 |
| HBM 带宽 | demand-plus-supply | demand + per-stack bandwidth | 0 | 拟合前拒绝 |
| HBM 容量 | mechanism-supply | per-stack HBM capacity | 0 | 拟合前拒绝 |
| HBM 容量 | workload-demand | frontier training compute | 5 | 完成 |
| HBM 容量 | demand-plus-supply | demand + per-stack capacity | 0 | 拟合前拒绝 |
| scale-up 带宽 | mechanism-supply | deployed scale-up link bandwidth | 0 | 拟合前拒绝 |
| scale-up 带宽 | workload-demand | frontier training compute | 7 | 完成 |
| scale-up 带宽 | demand-plus-supply | demand + deployed link bandwidth | 0 | 拟合前拒绝 |
| 晶体管 | mechanism-supply | logic density | 6 | 完成 |
| 晶体管 | workload-demand | frontier training compute | 10 | 完成 |
| 晶体管 | demand-plus-supply | demand + logic density | 3 | 完成 |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig16-route-a-variant-matrix-r1}}

折构造按目标世代与前置期逐一尝试。累计 303 次候选折拒绝中，155 次是截点前不足所需的连续世代转移，108 次是截点前没有严格可比的上一代规格标签，40 次是目标环境端点缺失。这些是“目标世代×前置期×变体”层面的构造事件，同一变体可贡献多次，不能与 8 个变体相加。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig18-route-a-fold-rejections-r1}}

#### 30 个资格单元的误差与拒绝原因

下表逐项给出 10 个完成变体在三个前置期的实际折数、模型/最佳朴素基线 MALE、模型/最佳朴素基线 CRPS 以及拒绝码。`N` 无折；`F` 少于 3 折；`C` 平均 CRPS 更差；`L` 平均 MALE 更差；`M` CRPS 未在多数折获胜；`D` 无正改善或由单折贡献超过 80%；`U` 90% 区间覆盖低于 $2/3$；`O` 至少一个留出点越过预声明 OOD 距离或杠杆界。数值保留足够有效位以复核量级，科学计数法尤其用于暴露尾部分布失控。

| 规格 | 变体 | 前置期 | 折数 | MALE：模型 / 基线 | CRPS：模型 / 基线 | 拒绝码 |
|---|---|---:|---:|---:|---:|---|
| 单卡功率 | demand | 18m | 3 | 0.4263 / 0.4244 | 234.7 / 242031 | L,D,O |
| 单卡功率 | demand | 24m | 2 | 0.3849 / 0.4534 | 265.5 / 10144 | F,D |
| 单卡功率 | demand | 30m | 2 | 0.6595 / 0.7228 | 360.2 / $9.18\times10^{14}$ | F,D |
| 启用 SM | supply | 18m | 3 | 17.0076 / 0.3073 | $3.98\times10^{108}$ / 32.19 | C,L,M,D,O |
| 启用 SM | supply | 24m | 2 | 5.9364 / 0.3606 | $4.33\times10^{18}$ / 38.88 | F,C,L,M,D,O |
| 启用 SM | supply | 30m | 0 | — | — | N |
| 启用 SM | demand | 18m | 3 | 1.9566 / 0.3073 | 2983 / 32.19 | C,L,M,D,O |
| 启用 SM | demand | 24m | 2 | 2.2400 / 0.3606 | 3285 / 38.88 | F,C,L,M,D |
| 启用 SM | demand | 30m | 2 | 0.7789 / 0.4609 | 48379 / 463245 | F,L,D,O |
| 启用 SM | demand+supply | 18m | 2 | 2.5471 / 0.3606 | 5146 / 41.01 | F,C,L,M,D,O |
| 启用 SM | demand+supply | 24m | 0 | — | — | N |
| 启用 SM | demand+supply | 30m | 0 | — | — | N |
| HBM 带宽 | demand | 18m | 2 | 0.6162 / 0.4756 | 6549 / $6.90\times10^7$ | F,L,D,U |
| HBM 带宽 | demand | 24m | 2 | 0.5703 / 0.4756 | 6183 / $1.01\times10^7$ | F,L,D,U |
| HBM 带宽 | demand | 30m | 1 | 1.1152 / 0.8534 | 11567 / 8466 | F,C,L,M,D,U |
| HBM 容量 | demand | 18m | 2 | 0.6262 / 0.3391 | 86.72 / $8.77\times10^8$ | F,L,D,U |
| HBM 容量 | demand | 24m | 2 | 0.5774 / 0.3391 | 83.31 / $6.40\times10^7$ | F,L,D |
| HBM 容量 | demand | 30m | 1 | 0.1074 / 0.2051 | 56.83 / 104.90 | F,D |
| scale-up 带宽 | demand | 18m | 3 | 0.1700 / 0.1255 | 307.0 / 1182 | L |
| scale-up 带宽 | demand | 24m | 2 | 0.2056 / 0.2029 | 464.2 / 4360 | F,L,D |
| scale-up 带宽 | demand | 30m | 2 | 0.2193 / 0.2029 | 499.5 / 16321 | F,L,D,O |
| 晶体管 | supply | 18m | 4 | 6.8383 / 0.2642 | $1.47\times10^{72}$ / $1.86\times10^6$ | C,L,D,O |
| 晶体管 | supply | 24m | 2 | 3.1615 / 0.0671 | $2.50\times10^{11}$ / 137.15 | F,C,L,M,D,O |
| 晶体管 | supply | 30m | 0 | — | — | N |
| 晶体管 | demand | 18m | 4 | 0.6712 / 0.2642 | 196.1 / $1.86\times10^6$ | L,D,O |
| 晶体管 | demand | 24m | 3 | 0.7960 / 0.1402 | 8589 / $1.70\times10^{20}$ | L,D |
| 晶体管 | demand | 30m | 3 | 0.1928 / 0.1402 | 570.3 / $8.99\times10^{34}$ | L,D,O |
| 晶体管 | demand+supply | 18m | 3 | 0.8476 / 0.2199 | 279.2 / $2.48\times10^6$ | L,M,D,O |
| 晶体管 | demand+supply | 24m | 0 | — | — | N |
| 晶体管 | demand+supply | 30m | 0 | — | — | N |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig17-route-a-lead-error-ratios-r1}}

跨 30 个资格单元，`N/F/C/L/M/D/U/O` 的出现次数依次为 6/15/8/21/8/23/4/12；一个单元可以有多个理由。局部看，单卡功率 24m、30m 和 HBM 容量 30m 的 MALE 优于基线，若只挑这三个数字会产生“模型有效”的错觉；但它们分别只有 2、2、1 折，CRPS 改善又由单折支配。反面例子更直接：SM-supply 18m 的 MALE 17.008 意味着典型乘法误差约 $e^{17}$，晶体管-supply 18m 的 MALE 6.838 约为 $e^{6.838}\approx 932$ 倍；相应 CRPS 爆炸说明 Student-$t$ 在少样本和巨大外推杠杆下产生失控尾部。

预声明超参数敏感性只对有折的 supply 主变体执行。六个目标中只有 SM 与晶体管可运行，各检验 ridge 精度 1/4/16 与年化 scale floor 0.03/0.05/0.10 的 $3\times3=9$ 个组合，共 18 个网格单元；合格数仍为 0。其余四个 supply 主变体没有合法折，不能用换超参数“救活”。因此路线 A 的负结果同时经基线比较、资格门槛和固定网格敏感性支持，而不是一次默认参数偶然失败。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig06-route-a-eligibility-r1}}

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig07-route-a-error-r1}}

路线 A 能支持的结论是“现有公开历史不足以识别环境回归中心”，而不是“需求或供给与规格无关”。强共趋势、39 个预测变量空单元和极少留出折使斜率无法稳定分离。技术预测研究同样警告，少量技术世代上的指数规律可能在拟合内稳定、在样本外失效 {cite}`farmer2016predictable`。任何路线 A Feynman 数字因此均不进入首页表，也不用于收窄 B 或 C。

### 路线 B：贝叶斯预测影响图如何传播、如何校验

#### 图结构、根变量与估计

路线 B 的图有 30 个节点和 67 条有向边：12 个归一化根变量进入 6 个潜在压力节点，再进入 6 个二元硬件特性与 6 个连续规格。其联合分布写为

$$
p(Y,H,Z,X\mid I_g)=p(X\mid I_g)\prod_j p(Z_j\mid \operatorname{pa}(Z_j))\prod_k p(Y_k\mid \operatorname{pa}(Y_k))\prod_m p(H_m\mid \operatorname{pa}(H_m)).
$$

每个根在 $[0,1]$ 内使用下界—众数—上界的独立三角分布。二元特性以带独立高斯系数先验的 logistic CPD 拟合，取 MAP 与 Hessian 的 Laplace 近似后抽样；连续规格对年化 log-growth 使用高斯先验线性 CPD，抽样参数与残差，再以最近对数距离投影到预声明可行规格网格。目标的六个潜在压力均值分别为 compute 0.701、memory 0.727、physical 0.665、power 0.446、risk 0.354、scale 0.702。图中没有 decision/utility 节点，根也按独立边际抽样，所以它不是已识别的 NVIDIA 决策网络。

| 根变量 | 证据类 | 众数 | 三角区间 | 实际含义与缺失量 |
|---|---|---:|---:|---|
| compute demand | derived | 0.835 | 0.772–0.899 | 截点前 frontier training FLOP 的 log 映射；非客户组合 |
| cooling headroom | derived | 0.660 | 0.560–0.760 | 已部署最高卡功率的设施能力代理；非剩余余量 |
| HBM readiness | derived | 0.832 | 0.752–0.912 | 已部署每 stack 容量/带宽等权代理；非供货承诺 |
| link readiness | derived | 0.818 | 0.728–0.908 | 已部署单 GPU 双向带宽的 log 映射 |
| process headroom | derived | 0.672 | 0.592–0.752 | 公开有效逻辑密度代理；非 foundry yield |
| memory demand | assumption | 0.835 | 0.595–1.000 | 以 frontier compute 代替状态、上下文、KV 与 batch mix |
| packaging readiness | assumption | 0.752 | 0.502–1.000 | 缺 CoWoS 产能、attach/bond yield、成本和进度 |
| reliability pressure | assumption | 0.800 | 0.580–1.000 | 以 failure-domain 扩张代替现场失效率/服务成本 |
| scale-up demand | assumption | 0.835 | 0.595–1.000 | 以 frontier compute 代替并行与拓扑需求 |
| software readiness | assumption | 0.760 | 0.580–0.940 | 基于 Transformer/FlashAttention 日期的序数代理 |
| supply confidence | assumption | 0.500 | 0.150–0.850 | 分配、良率、成本与产能预留均不可见 |
| TCO pressure | assumption | 0.713 | 0.493–0.933 | 已部署功率等级代理；非价格、利用率或内部效用 |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig21-route-b-root-intervals-r1}}

目标根中 7/12，即 58.33%，是显式 assumption；五个 `derived` 根仍含归一化边界、等权或替代量。compute、memory 与 scale-up 又共享 0.835 的 frontier-compute 中心，而模型没有共同观测父节点或协方差，可能重复放大同一信号。图 8 的审计因此把这一比例视为主观性下限。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig08-route-b-root-audit-r1}}

#### 六折历史回测的逐代数据

回测折依次留出 Volta、A100、H100、B200、Blackwell Ultra 与 Rubin；每折只使用该决策截点前公开的根、特性和规格，泄漏检查 6/6 通过。Volta 之前没有足够连续规格转移，只评分特性先验；其余每个单元报告“预测中位数/观察值（绝对对数误差）”。Rubin 没有严格可比 TDP 标签，故该格为空。

| 留出世代 | 晶体管 B | HBM 容量 GB | HBM 带宽 TB/s | NVLink TB/s | TDP W | 低精度代理 PF |
|---|---:|---:|---:|---:|---:|---:|
| Volta | — | — | — | — | — | — |
| A100 | 41.63/54.2 (0.264) | 55.46/40 (0.327) | 2.328/1.555 (0.404) | 0.707/0.600 (0.164) | 403/400 (0.008) | 0.800/0.312 (0.942) |
| H100 | 67.45/80 (0.171) | 82.87/80 (0.035) | 4.985/3.352 (0.397) | 1.319/0.900 (0.383) | 521/700 (0.295) | 3.208/1.979 (0.483) |
| B200 | 189.14/208 (0.095) | 77.87/192 (0.902) | 5.191/8.000 (0.432) | 1.709/1.800 (0.052) | 636/1200 (0.634) | 1.686/10 (1.780) |
| Blackwell Ultra | 218.26/208 (0.048) | 150.79/288 (0.647) | 8.602/8.000 (0.073) | 1.998/1.800 (0.104) | 1135/1400 (0.210) | 9.142/15 (0.495) |
| Rubin | 299.83/336 (0.114) | 181.80/288 (0.460) | 11.918/22 (0.613) | 2.604/3.600 (0.324) | — | 14.875/50 (1.212) |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig19-route-b-fold-error-heatmap-r1}}

逐指标聚合如下。90% 覆盖为 1.0 只表示 5/5 或 4/4，并不构成精确校准；六个连续输出有 99.990%–99.995% 的原始抽样被离散网格改变，宽网格区间和边界聚集会机械提高覆盖。

| 连续规格 | 可评分折 | 平均 MALE | 经验 90% 覆盖 | 主要误差位置 |
|---|---:|---:|---:|---|
| 晶体管 | 5 | 0.138 | 1.0 | A100 0.264 最大 |
| NVLink 双向带宽 | 5 | 0.205 | 1.0 | H100 0.383、Rubin 0.324 |
| 单卡 TDP | 4 | 0.287 | 1.0 | B200 0.634 |
| HBM 带宽 | 5 | 0.384 | 1.0 | Rubin 0.613 |
| HBM 容量 | 5 | 0.474 | 1.0 | B200 0.902、Blackwell Ultra 0.647 |
| frontier low-precision 代理 | 5 | 0.982 | 0.8 | B200 1.780、Rubin 1.212 |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig09-route-b-male-r1}}

#### 二元特性校验与 Feynman 诊断输出

特性基线是在同折可见历史正例频率上平滑得到的常数预测。Brier 越低越好；“模型优于基线”仍不等于概率已校准，因为每节点只有六折且正例极少。

| 特性节点 | 历史正例 | 模型 Brier | 频率基线 | 判断 |
|---|---:|---:|---:|---|
| GPU-package CPO | 0 | 0.020 | 0.102 | 数字较低只奖励持续低预测；无正例可验证采用 |
| HBM 代际步进 | 3 | 0.273 | 0.315 | 局部改善，样本不足 |
| 多计算裸片 | 3 | 0.293 | 0.386 | 局部改善，样本不足 |
| 新数值格式 | 4 | 0.334 | 0.302 | 劣于基线 |
| NVLink 代际步进 | 5 | 0.289 | 0.202 | 劣于基线 |
| rack power smoothing | 1 | 0.137 | 0.202 | 只有一个正例 |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig20-route-b-feature-brier-r1}}

目标影响图使用 2026-08-27 决策截点与 20000 次抽样。未条件化均值为：多计算裸片 0.751、HBM 步进 0.752、新格式 0.721、NVLink 步进 0.855、功率平滑 0.379、GPU-package CPO 0.212。GTC 2026 的 NVLink 8 与节点语义完全一致，故该节点在披露后固定为 true；固定值 1.0 是条件，不是模型置信度。Die Stacking、Custom HBM 与平台级 CPO 的拓扑/容量/放置不等价，均未固定。

| 路线 B 目标规格 | q05 | 中位数 | q95 | 解释限制 |
|---|---:|---:|---:|---|
| 晶体管 B | 480 | 672 | 960 | 受网格与 7 个假设根影响 |
| HBM 容量 GB | 384 | 576 | 768 | 非 Custom HBM 官方解码 |
| HBM 带宽 TB/s | 32 | 56 | 64 | 上界聚集明显 |
| low-precision 代理 PF | 100 | 200 | 300 | 不等同路线 C 的稠密 FP4 |
| NVLink 双向 TB/s | 4.8 | 7.2 | 12 | NVLink 8 只固定代际，不固定带宽 |
| 单卡 TDP W | 1600 | 2800 | 2800 | q50/q95 同为网格上界 |

因此路线 B 的 672B/576GB/56TB/s/200PF/7.2TB/s/2.8kW 只展示假设如何沿图传播。低精度与 HBM 容量的历史误差、两个劣于基线的特性节点、几乎全面的网格投影和 58.33% 假设根共同阻止其成为首页中心。

### 路线 C：可行域约束设计空间如何求解

#### 24 个月输入包络、离散网格与方程

路线 C 的主条件以 2026-03-20 为截点。每次技术抽样从下表连续区间的对称三角分布抽取一个 $\theta$，众数为区间中点；容量等少数变量按列出的离散可得性另行抽取。再对 tile、主动层、die area、HBM、TDP、NVLink lane 与机架规模的笛卡尔网格逐个候选检查约束。这里的区间是公开证据加工程假设形成的压力测试输入，不是测量误差后验。

| 输入组 | 24m 连续范围或离散值 | 用途 | 关键限制 |
|---|---|---|---|
| 逻辑制造 | 密度 190–240 MTr/mm²；layout 0.85–0.93；缺陷 0.040–0.095/cm²；聚类 $\alpha$ 2.4–4.8 | 晶体管与 die yield | 非 NVIDIA/TSMC 成熟良率 |
| 逻辑结构 | tile 2/4；主动层 1/2；die 620/740/850 mm²；reticle 858 mm² | 架构网格 | Die Stacking 未说明 die 角色 |
| SM/计算 | compute fraction 0.51–0.60；0.70–0.92 BTr/SM；bin 0.04–0.09；1.70–2.02 GHz；90k–114k FP4 op/SM/cycle | SM 与峰值计算 | 只是稠密 FP4 代理模型 |
| 计算能耗/热 | 0.028–0.047 pJ/FP4 op；TDP 2200/2600/3000 W；冷却 2700–3300 W；热流 1.65–2.45 W/mm² | 功率与热约束 | 不含 3D 热阻测量 |
| HBM | stack 8/12/16；36/48/64 GB 每 stack，可得率 1/0.85/0.20；2.75–3.65 TB/s 每 stack | 容量与原始带宽 | 非 HBM 采购/良率预测 |
| HBM 控制/功率 | 15–21 TB/s 每 tile；效率 0.89–0.97；38–62 W 每 stack | 控制器瓶颈和卡功率 | 控制器位置未知 |
| 封装 | footprint 5000–6500 mm²；attach yield 0.995–0.9988；最低 assembly yield 0.87–0.93 | 面积与装配代理 | 无实际 bond/attach 数据 |
| NVLink | 192/224/256 lane；125–180 Gb/s；编码效率 0.94；0.60–1.10 pJ/bit | 双向带宽与 I/O 功率 | 不代表 NVLink 8 正式 lane 定义 |
| 机架 | 72/144 GPU；功率上限 390–590 kW；固定功率 55–92 kW；每 GPU 开销 300–540 W | rack power | 非设施输入功率 |
| workload | training AI 2400–6000；decode AI 45–140；scale-up 强度 7000–18000 FLOP/B；利用率 0.56–0.78 | roofline 与交付计算 | 不代表客户 workload mix |

裸片良率代理为 $Y_d=(1+D A_{cm^2}/\alpha)^{-\alpha}$；已知良裸片筛选使它只进入成本/可行性，不再对逻辑 die 数幂乘。晶体管容量为

$$
T=\frac{n_T n_L A_d d\eta_{layout}[1-0.04(n_L-1)]}{1000},
$$

其中 $n_T$ 为横向 tile 数、$n_L$ 为主动层数、$A_d$ 为单 die 面积、$d$ 为 MTr/mm²。封装装配代理为 $Y_p=y_{attach}^{n_Tn_L+n_{HBM}}$，footprint 为 $1.12n_TA_d+112n_{HBM}+860+120(n_L-1)$ mm²。HBM 带宽取 stack 原始和控制器上限的较小值再乘控制效率；NVLink 双向带宽为 $n_{lane}r\times0.94\times2/8000$ TB/s。扣除 HBM、NVLink、7.5% 转换损耗与固定 I/O 后得到逻辑功率；峰值计算取硅面积上限和 $P_{logic}/(1000E_{op})$ 功率上限的较小值，交付训练代理再取计算、HBM roofline、NVLink roofline 的最小值并乘软件利用率。

候选依次检查 reticle、die yield、package assembly、footprint、card cooling、至少 128 SM 且按 8 SM 粒度、HBM controller、正逻辑功率、heat flux 与 rack power；只有全部通过才计算目标。对每次 $\theta$，枚举所有离散候选并保留固定 log-linear 目标最高者：

$$
s^*(\theta,a,w)=\underset{s\in\mathcal{G}(a),\;c_j(s,\theta)\le 0}{\operatorname{argmax}}\sum_{m=1}^{5}w_m\log\!\left(\frac{q_m(s,\theta)}{q_{m,0}}\right).
$$

五个 $q_m$ 依次为训练交付计算/MW、decode 有效内存带宽/MW、HBM 容量、NVLink/MW、三年生命周期效率；成本项是 2026 美元代理，不是售价、毛利或 NVIDIA TCO。若一个抽样的整个离散网格都无候选，才记为“未找到可行解”。

#### 75 个条件如何组成、实际运行了多少

| 权重方案 | 训练计算/MW | decode 内存/MW | HBM 容量 | NVLink/MW | 生命周期效率 |
|---|---:|---:|---:|---:|---:|
| balanced | 0.31 | 0.19 | 0.14 | 0.14 | 0.22 |
| training-centric | 0.45 | 0.10 | 0.10 | 0.15 | 0.20 |
| memory-centric | 0.18 | 0.32 | 0.22 | 0.10 | 0.18 |
| scaleup-centric | 0.20 | 0.10 | 0.10 | 0.35 | 0.25 |
| lifecycle-centric | 0.20 | 0.12 | 0.10 | 0.10 | 0.48 |

五类架构为架构未决网格优化器、`2T-1L`、`2T-2L`、`4T-1L`、`4T-2L`。三个时点×五架构×五权重构成 75 个条件，每条件 1024 次。18m 截点 2026-09-20 晚于证据冻结日 2026-08-27，因此明确右删失，只作敏感性。

| 前置期 | 截点 | 信息完整 | 条件 | 请求抽样 | 找到可行候选 | 单条件最低可行率 |
|---:|---|---|---:|---:|---:|---:|
| 30m | 2025-09-20 | 是 | 25 | 25,600 | 25,487 | 0.9717 |
| 24m | 2026-03-20 | 是 | 25 | 25,600 | 25,588 | 0.9980 |
| 18m | 2026-09-20 | 否，右删失 | 25 | 25,600 | 25,593 | 0.9990 |
| 合计 | — | — | 75 | 76,800 | 76,668 | — |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig22-route-c-condition-feasibility-r1}}

“76,668 次找到可行候选”只表示在我们写入的网格与不等式内至少存在一个点，不是 99.8% 制造良率。单个技术抽样会检查数千到数万离散候选，候选被拒的数量也不等于晶圆良率；只有最终每抽样是否存在最优解进入上述分母。

#### 架构、目标函数与时点敏感性

24m、balanced 的五种架构条件给出如下 q50。架构未决行就是首页主工作点；固定行用来回答“如果 die stacking 最终是哪一种逻辑拓扑，结果怎样”。

| 架构条件 | 晶体管 B / SM | HBM GB / TB/s | 稠密 FP4 PF | NVLink TB/s | TDP W | rack GPU / kW |
|---|---:|---:|---:|---:|---:|---:|
| 架构未决 | 471.8 / 296 | 768 / 45.29 | 43.44 | 9.175 | 2600 | 72 / 323.2 |
| 2T-1L | 311.2 / 192 | 576 / 33.23 | 34.69 | 9.177 | 2200 | 144 / 447.6 |
| 2T-2L | 462.4 / 296 | 576 / 33.04 | 44.62 | 9.152 | 2600 | 144 / 445.3 |
| 4T-1L | 474.6 / 296 | 768 / 45.44 | 43.87 | 9.214 | 2600 | 72 / 319.5 |
| 4T-2L | 908.5 / 584 | 768 / 43.97 | 44.22 | 9.171 | 2600 | 72 / 320.4 |

在架构未决、balanced 的 1024 次最优解中，4 tile 占 83.20%，1 active tier 占 91.70%，16 HBM stack 占 62.70%，72 GPU 机架占 64.94%，所有解都要求达到模型定义的 CPO-class SerDes 带宽。这些是输入分布与目标函数下的优化选择频率，不是 NVIDIA 架构采用概率；尤其 `4T-1L` 仍可包含非主动的堆叠 cache/I/O/base die。

保持架构未决，只改变五组目标权重，24m q50 如下。它直接量化未知私有效用函数会把工作点移动多少。

| 目标权重 | 晶体管 B / SM | HBM GB / TB/s | FP4 / 交付 PF | NVLink TB/s | TDP W | rack GPU / kW |
|---|---:|---:|---:|---:|---:|---:|
| balanced | 471.8 / 296 | 768 / 45.29 | 43.44 / 29.23 | 9.175 | 2600 | 72 / 323.2 |
| training-centric | 469.0 / 296 | 384 / 24.28 | 50.31 / 33.47 | 9.175 | 2600 | 144 / 445.3 |
| memory-centric | 472.0 / 296 | 768 / 46.55 | 32.68 / 21.92 | 9.211 | 2200 | 144 / 450.0 |
| scaleup-centric | 357.6 / 240 | 384 / 24.03 | 38.82 / 25.99 | 9.200 | 2200 | 144 / 448.5 |
| lifecycle-centric | 469.7 / 296 | 384 / 23.89 | 51.69 / 34.49 | 9.163 | 2600 | 72 / 329.5 |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig24-route-c-objective-sensitivity-r1}}

目标权重把 HBM 容量从 768 GB 降到 384 GB、HBM 带宽约减半，并能把 rack 中位数从 72 改到 144 GPU；所以主行不是跨目标函数“最可能”的中心。时点敏感性同样显著：balanced/架构未决 q50 从 30m 的 430.4B、256 SM、576 GB、29.51 TB/s、36.44 PF、7.80 TB/s、2.4 kW、72 GPU/296 kW，移动到 24m 主行；右删失 18m 则为 497.3B、328 SM、768 GB、53.93 TB/s、51.94 PF、10.70 TB/s、3.0 kW、144 GPU/468 kW。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig25-route-c-vintage-sensitivity-r1}}

#### 哪些约束真正压住主工作点

对 24m、balanced、架构未决的每个已选最优设计，若约束相对裕量不超过 10% 就记为“绑定”。频率不是某个物理事件的概率，而是定位主工作点对哪些模型假设最敏感。

| 约束 | 绑定频率 | 数学/工程含义 | 读者应如何解释 |
|---|---:|---|---|
| package assembly yield | 0.9922 | $y_{attach}^{n_{logic}+n_{HBM}}$ 接近最低阈值 | 最大依赖；实际 bond 数据缺失 |
| package footprint | 0.6006 | tile、HBM 与额外层面积接近 5000–6500 mm² 上限 | 4T 与 12–16 stack 的直接压力 |
| card cooling | 0.5723 | 离散 TDP 接近抽样冷却上限 | 2.6–3.0 kW 需强液冷资格 |
| rack power | 0.3115 | 固定功率加 GPU/开销接近 390–590 kW | 决定 72/144 GPU 分支 |
| compute power | 0.2451 | 硅峰值与能耗峰值差在 10% 内 | 计算开始受功率而非面积限制 |
| HBM controller | 0.1533 | stack 原始带宽接近 tile controller 上限 | 多 stack 不必等比例增加有效带宽 |
| die yield | 0.0664 | clustered-defect yield 接近最低阈值 | 不是 package yield |
| heat flux | 0.0029 | 逻辑功率密度接近输入上限 | 低频不代表真实 3D 热问题很小 |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig23-route-c-binding-frequencies-r1}}

历史 sanity check 把 A100、H100、B200、Rubin 的已知标签代回容量边界，检验方程是否连已知产品都排除。四例均通过，但这是必要而非充分条件。

| 历史平台 | 冷却利用率 | HBM 带宽利用率 | HBM 容量利用率 | 晶体管容量利用率 | pJ/峰值 op | 结论 |
|---|---:|---:|---:|---:|---:|---|
| A100 SXM 80GB | 1.000 | 0.971 | 1.000 | 0.994 | 1.282 | 通过 |
| H100 SXM | 1.000 | 0.957 | 1.000 | 0.994 | 0.354 | 通过 |
| B200 SXM | 1.000 | 0.980 | 0.938 | 未核 | 0.100 | 通过；晶体管项缺失 |
| Rubin GPU | 1.000 | 0.982 | 1.000 | 0.992 | 0.066 | 通过 |

这些检查没有历史留出误差，也没有验证封装装配、成本或热阻绝对值。路线 C 的 q10/q50/q90 因而是“给定三角输入、架构与权重时，优化器输出的边际工程分位数”，不是置信区间、可信区间或校准概率；不同指标的边际 q50 也未必来自同一个联合候选。

## 小样本识别、回测与拒绝

三条路线的比较单位、可检验性和失败模式如下。表中的“中心”指能否把某个 q50 解释为经历史资格审定的预测中心，而不只是程序输出。

| 路线 | 主要输入 | 输出 | 时间回测 | 可发布统计中心 | 主要失败 |
|---|---|---|---|---|---|
| A 环境回归 | 9 事件面板、严格截点代理 | 连续规格 Student-$t$ 外推 | rolling-origin，比较三类朴素基线 | 否 | 0/30 资格单元合格；共趋势、折数不足、OOD。 |
| B 预测影响图 | 公开派生根与宽假设根 | 规格网格、特性节点、敏感性 | 6 折 MALE、Brier | 否 | 7/12 根为假设；无 decision/utility；若干特性不如基线。 |
| C 工程设计空间 | 预声明物理/系统范围、架构、权重 | 条件边际 q10/q50/q90 | 历史 sanity check，无覆盖校准 | 否；仅具名工程工作点 | 缺联合 BOM、绝对制造与热模型；区间无覆盖概率。 |

### 为什么没有统计中心

规格世代不是独立同分布样本。工作负载规模、工艺、HBM、封装、互连和功率几乎同时上升，只有少数代际转移可用，预测变量又有 39 个空单元；在这种条件下，不同机制模型可以拟合同一历史曲线。ridge 和经验贝叶斯收缩可以防止数值爆炸，却不能区分“需求推动”与“供给允许”两条共趋势路径。路线 A 中 21/30 资格单元的对数误差不如最佳朴素基线，加上 0 个合格单元，已经满足停止中心预测的规则。

更重要的是，区间覆盖率在极少折上很容易显得理想：路线 B 多数连续指标的 90% 网格区间覆盖为 1.0，但这些区间宽、离散投影接近上界，且只有六折。把 1.0 写成“校准良好”会忽略有限样本与网格截断。本文采用的判断是：不能从现有历史证据识别统计中心，也不能给 Feynman 宣称频率覆盖或贝叶斯可信度。

三路线的范围重叠也不增加资格。路线 A 的尾部外推未通过资格审定且回测失败；路线 B 的区间由先验、共享代理和离散网格强烈决定；路线 C 的范围来自工程条件。它们在数量级上重叠最多只能说明“没有明显方向矛盾”，不能验证路线 C、构造多模型共识区间或收窄外包络。

### 条件概率能说什么、不能说什么

路线 B 可以回答“如果把 packaging readiness 或 memory demand 的假设区间上调，哪些输出节点随之上移”，也可以显示某个特性节点对父变量的方向敏感性。它不能回答 NVIDIA 在私有成本、良率、客户权重和进度下的真实采用概率，更不能把路线图上的 Die Stacking 自动映射成 multi-compute-die=true。唯一被官方事实固定的节点是 NVLink generation step；Custom HBM、Die Stacking 和平台 CPO 因语义或放置不等价而保持未映射。

### 工程包络如何补充而非替代统计识别

路线 C 回答“在给定范围、架构和目标权重下，哪些联合方案通过模型约束并取得较高目标值”。它将单变量趋势无法表达的封装、HBM、功耗、机架和目标冲突显式化，适合产生可反证的设计压力情景；但它没有经历史覆盖校准，也没有 foundry 级 die area、缺陷密度、bond/attach yield、热阻、真实 BOM 和供应曲线。故 q50 只能称为具名工程工作点，q10/q90 只能称为同条件分位数，跨条件最小 q10 到最大 q90 只能称为外包络。

## 当前观测与 Feynman 官方边界

GTC 2026 路线图把 Feynman 放在 2028 位置，并列出 Die Stacking、Custom HBM、Rosa CPU、BlueField-5、NVLink 8 CPO、Spectrum-7 204T CPO 与 ConnectX-10 {cite}`nvidia2026feynman`。这些标签构成官方边界：Die Stacking 证明存在堆叠集成方向，却未说明堆叠的是 compute、cache、I/O 或 base die；Custom HBM 未说明代际、stack 数、容量、pin rate 或控制器位置；NVLink 8 的代际步进已披露，但单 GPU 带宽、lane 组织、效率和 CPO 放置未披露；Spectrum-7 的 204T CPO 是交换机层事实，不是 GPU-package CPO 证据。Rosa、BlueField-5 和 ConnectX-10 是平台伴随组件，不是 GPU 数值规格。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig14-feynman-spec-table-r1}}

截至证据冻结日，官方 Feynman GPU 数值规格数量为 0。任何晶体管、SM、HBM 容量/带宽、FP4、NVLink 数值、TDP 或机架功率都来自本文的条件模型，不得与上段官方标签放在同一事实栏。NVHBM 的 custom base die 与 NVLink Fusion 面向 custom XPU 的材料也只说明一条可能的产业路径，不能补全 Feynman 的 Custom HBM 数字。

## 下一代数值规格：工作点、条件带与外包络

下表的工作点固定为 24 个月截点（2026-03-20）、balanced 权重、架构未决网格优化器的各指标边际 q50。同条件带为该条件下边际 q10–q90；外包络是在同一 24 个月截点、5 个架构×5 组权重共 25 条件中取最小 q10 与最大 q90。三列都不是“最可能值”或带覆盖率区间，不同指标的边际分位数也不保证来自同一个联合样本。

| 指标与层级 | 工程工作点 q50 | 同条件 q10–q90 | 25 条件外包络 |
|---|---:|---:|---:|
| 晶体管，chip，B | 471.778 | 412.978–508.435 | 243.962–978.444 |
| 启用 SM，chip | 296 | 248–336 | 152–648 |
| HBM 容量，card，GB | 768 | 576–1024 | 288–1024 |
| HBM 带宽，card，TB/s | 45.286 | 33.521–50.718 | 21.810–51.131 |
| 稠密 FP4 峰值，card，PFLOP/s | 43.443 | 35.685–52.555 | 26.250–64.818 |
| NVLink，card，TB/s 双向 | 9.175 | 8.282–10.071 | 8.191–10.144 |
| 单 GPU TDP，card，W | 2600 | 2600–3000 | 2200–3000 |
| 机架 GPU 数，rack | 72 | 72–144 | 72–144 |
| 机架功率，rack，kW | 323.217 | 289.777–510.842 | 264.888–513.871 |

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig10-route-c-spec-ranges-r1}}

### 计算与晶体管

471.8B 晶体管与 296 SM 是 `4T-1L` 倾向下的边际工作点，不是官方 tile 计数。固定架构的 balanced 中位数显示：`2T-1L` 为 311.2B、192 SM、34.69 PFLOP/s 稠密 FP4、2.2 kW；`2T-2L` 为 462.4B、296 SM、44.62 PFLOP/s、2.6 kW；`4T-1L` 为 474.6B、296 SM、43.87 PFLOP/s、2.6 kW；`4T-2L` 为 908.5B、584 SM、44.22 PFLOP/s、2.6 kW。以同为四个横向 tile 的 `4T-1L` 为基线，`4T-2L` 的晶体管增加 91.4%、SM 增加 97.3%，但稠密 FP4 仅增加 0.79%，delivered training proxy 仅增加 1.74%；比较固定在 24 个月、balanced、相同功率候选网格，在该上下文中第二主动层更像封装、热与供电压力上界，而不是工作中心。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig11-route-c-architecture-r1}}

路线 B 的 low-precision 指标以另一组历史语义和网格定义，不能转换为这里的稠密 FP4。本文因此只把 43.4 PFLOP/s 作为路线 C 的条件工作点，不与 200 PFLOP/s 的路线 B 诊断取均值或比例。

### HBM 容量与带宽

768 GB 与 45.3 TB/s 的工作点来自 12–16 stack、单 stack 容量/速率和封装/控制器范围的联合抽样。1024 GB 同时是主条件 q90 和跨条件上界，提示离散候选网格存在上界聚集；它不能被解释为“90% 不超过 1 TB”。同理，45.3 TB/s 是 balanced 条件下内存目标与功率、控制器、封装边缘共同作用的结果，而非 Custom HBM 官方数字。

工程反证门槛比中心更有用：若正式 HBM 无法达到 48 GB/stack 或系统级带宽落到约 33.5 TB/s 的主条件 q10 以下，576–1024 GB 和 45.3 TB/s 工作点需要下修；若官方容量/带宽超出 25 条件外包络，则必须扩展 stack、pin rate、压缩或存储层次可行域，不能把正式值裁剪回当前网格。

### NVLink、TDP 与机架

9.18 TB/s 是单 GPU 双向 NVLink 条件工作点；NVLink 8 代际已由官方披露，但任何带宽数字仍属模型输出。路线 C 主条件中 `requires_cpo_class_serdes` 对全部样本为真，说明该带宽工作点对 CPO-class SerDes 能力是硬依赖；与此同时，24 个月时点的 NVLink 8 CPO 执行敏感性仅为 0.32，而且明确是 elicited roadmap-execution sensitivity，不是特性采用概率。两者必须并读：模型主解需要这种能力，但 2026-03-20 时点并没有充分公开证据保证其按期执行。若正式单 GPU 双向带宽低于约 8.28 TB/s，主 scale-up 情景失效，需要重算并行效率、交换层与 72/144 GPU 机架选择。

2.6–3.0 kW 的单 GPU 条件带意味着直接液冷、VRM/busbar、瞬态控制和维护设计成为近必要的平台依赖。8 GPU 节点的派生工作点为 6.144 TB HBM 与 347.5 PFLOP/s 稠密 FP4；72 GPU 机架边际工作点约 323 kW，主条件 q90 在 144 GPU 分支上升至约 511 kW。该功率包含系统系数，不能由 GPU TDP 简单相乘，也不等于数据中心设施输入功率。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig12-rack-power-r1}}

## 硬件特性：官方披露、条件判断与反证

硬件特性必须同时回答三个问题：哪里已有官方事实，模型在什么条件下支持哪种实现，哪条新证据会推翻判断。下图用证据层级而非单一“会/不会”标签组织特性。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig13-feature-evidence-r1}}

| 特性 | 官方已披露 | 条件工程判断 | 仍未知或反证 |
|---|---|---|---|
| Die Stacking | Feynman 路线图标签 | `4T-1L` 为工作解释；堆叠可位于 cache/I/O/base | 不能推出多 compute die 或两主动层；若官方确认两主动层且晶体管显著高于 508B，则上调 `4T-2L`。 |
| Custom HBM | Feynman 路线图标签 | 12–16 stack、768 GB、45.3 TB/s 为条件工作情景 | 代际、stack 数、容量、带宽、base/controller 与良率均未披露。 |
| NVLink 8 CPO | NVLink 8 与系统 CPO 路线 | 9.18 TB/s 双向、CPO-class SerDes 是工程情景 | CPO 在交换机、GPU package 或其他层级未定；Spectrum CPO 不证明 GPU-package CPO。 |
| 新数值格式 | 未披露 Feynman 格式 | 低精度/缩放/软件协同仍有需求动机 | 路线 B Brier 差于基线，不给采用概率；若下一代 Tensor Core 无新格式则反证该节点。 |
| 直接液冷与功率平滑 | 未披露具体 Feynman 功能 | 2.6–3.0 kW 条件使冷板、供电和瞬态控制成为强依赖 | power smoothing 只有一个历史正例；若卡级资格低于 2.6 kW，依赖显著减弱。 |
| RAS/机密计算/MIG | 无具体 Feynman GPU 披露 | 更大 failure domain、长任务和多租户提高隔离、遥测、恢复价值 | 具体粒度、性能代价与可信执行边界未知。 |
| Rosa/BlueField-5/Spectrum-7/ConnectX-10 | 平台组件已列名 | CPU、DPU、交换与 NIC 共同构成 rack-scale 交付边界 | GPU-facing 带宽、coherence、offload 与故障域未披露。 |

来源说明：“官方已披露”列以 GTC 2026 路线图第 66 页的 Feynman 平台边界为准 {cite}`nvidia2026feynman`；A100 的 MIG 连续性先例来自其官方架构说明 {cite}`nvidia2020a100`。其余两列是本文在已声明模型条件下的工程判断与反证规则，不是来源事实。

### 堆叠与多裸片拓扑

“Die Stacking”描述垂直集成，不等于“多个横向 compute tile”，也不等于“两个主动计算层”。路线 C 的架构未决条件允许两个或四个横向 tile，以及一个或两个主动层，正是为了保留这些解释。`4T-1L` 可同时兼容“存在堆叠，但堆叠 die 是 cache、I/O 或 base logic”；`4T-2L` 则检验相同四横向 tile 基线上增加第二主动层对晶体管、SM、功率和热约束的压力。官方若披露 die 角色、层数、面积或 bond 技术，应首先修改架构条件，而不是只调整晶体管倍率。

### Custom HBM、存储层次与数值格式

Custom HBM 的工程价值可能来自定制 base die、控制器位置、协议、可靠性、与 GPU/交换的邻接或封装协同，而不只来自下一代 DRAM cell。本文的 12–16 stack 和 768 GB 是可行域条件，不是对官方标签的解码。若最终容量低于 576 GB，但引入更大片上缓存、压缩或更高有效带宽，当前模型需要扩展存储层次变量，不能简单判定“路线图失败”。

新数值格式同样不能按世代节拍机械外推。格式是否有用取决于训练稳定性、累加精度、缩放语义、编译器/框架和代表性模型。路线 B 对新格式的 Brier 劣于常数基线，所以本文只保留方向性假设：若工作负载继续接受更低精度且软件栈成熟，格式或专用缩放机制的边际效用上升；正式架构没有新格式则直接反证该特性节点。

### CPO、RAS、机密计算与系统平台

CPO 的层级是最容易发生语义偷换的部分。官方路线图的 NVLink 8 CPO 与 Spectrum-7 204T CPO 支持“光学进入 scale-up/网络系统”的事实，却没有说明光引擎在 GPU package。路线 B 的 GPU-package CPO 历史标签为零正例，故 0.212 的条件均值不能发布为采用概率。官方若明确 CPO 只在交换机，本调查将确认系统级判断并反证 GPU-package 节点；若明确位于 GPU package，则反向更新放置变量。

更高功率、更大 scale-up domain 和更长训练/推理任务会提高故障隔离、遥测、可恢复执行、机密计算和资源分区的效用。A100 的 MIG 提供过平台连续性先例 {cite}`nvidia2020a100`，但不能据此断言 Feynman 的具体 MIG 粒度或机密计算能力。本文把增强 RAS 与 rack-scale confidential computing 列为合理系统需求，不赋予官方状态或数值概率。

## 条件权衡、反证与更新规则

预测的可用性来自预先写明如何失败。每个工作点都绑定改善资源、代价、依赖和可观察触发器；正式披露一旦越界，应保留旧预测登记并重跑新版本，而不是事后改写旧区间。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig15-disconfirmation-triggers-r1}}

| 触发器 | 被反证或更新的结论 | 更新动作 |
|---|---|---|
| 官方晶体管显著高于 508B 且确认两个主动逻辑层 | `4T-1L` 工作拓扑和主晶体管带 | 上调 `4T-2L` 权重，加入层间带宽与热阻约束。 |
| 量产封装无法容纳 4 compute tile 与 12–16 HBM stack | `4T-1L`、768 GB 工作点 | 退回 `2T-1L` 或 `2T-2L`，重算封装边缘、容量和晶体管。 |
| 持续卡级冷却资格低于 2.6 kW或 3D 热阻超限 | 主计算带与双主动层情景 | 下修频率/功率，重新优化 SM、FP4 与机架密度。 |
| HBM 小于 48 GB/stack 或总带宽低于约 33.5 TB/s | 576–1024 GB 与 45.3 TB/s 工作点 | 修改 HBM 离散网格和存储层次，重跑所有目标权重。 |
| NVLink 8 单 GPU双向带宽低于约 8.28 TB/s | 主 scale-up 情景 | 重算通信效率、交换层和 72/144 GPU 选择。 |
| 官方明确 CPO 只位于交换机 | GPU-package CPO 假设 | 置该节点为 false，保留系统 CPO 为 true。 |
| 官方明确 CPO 位于 GPU package | 当前未决放置 | 置放置节点为 true，加入封装光电功耗与热约束。 |
| 任一正式数字超出 24 个月外包络 | 当前可行域不完备 | 扩展输入或架构空间；禁止把观察值裁剪到旧上界。 |

这里的更新规则也解决“当前观察如何进入未来提案”的核心问题：新模型、基准或供应信息首先改变 $I_g$ 中的需求/可行域变量，其次改变约束或目标敏感性，最后才改变规格输出；官方规格本身只能用于事后评分和下一版训练，不能回写原预测时点。

## 研究缺口与方法含义

最优先的缺口不是再找一条 CAGR，而是增加可辨识信息。第一，需要更可信的历史 $\tau_g$ 代理，例如首个 tape-out、HBM qualification、系统 bring-up 或客户采样日期；这会直接改善 q01 和时间回测。第二，需要逐代 die area、reticle 使用、缺陷密度、wafer/package/bond yield、HBM 分配与热阻范围；这些量决定 $F_g$，也是当前 `4T-2L` 压力上界过宽的根因。第三，需要按训练、prefill、decode、MoE 和 HPC 分层的公开 workload mix 与系统利用率，才能把需求代理变成可估计边际效用。

第四，离散特性需要更多独立正负例和一致标签。CPO 零正例、power smoothing 一正例使任何概率校准都不可信；新格式和 NVLink 节点又没有击败频率基线。第五，需要导出联合可行样本与联合 BOM/制造模型；当前边际 q50 拼在一起不一定是同一个设计。第六，后续验证应在正式 Feynman 数字发布时使用 proper score、预登记范围和未改写的旧版本评估，而不是只检查中心是否“接近”。

方法上，负结果本身具有结构含义：当历史样本不能识别环境回归中心时，研究应该从“点预测竞赛”降级为条件设计空间、敏感性和反证；当工程模型缺少制造参数时，宽包络是诚实边界，而不是可以靠更复杂统计模型自动收窄的噪声。

## 局限

本研究只重建公开观察者的决策逻辑，不声称恢复 NVIDIA 内部冻结日、客户权重、目标函数、成本、良率、供应合同或量产阈值。18/24/30 个月截点是代理，24 个月主情景并不更接近未知内部日期；18 个月时点在当前证据冻结日右删失。

历史面板只有 9 个事件，并存在 39 个预测变量空单元和强共趋势。路线 A 的统计拒绝意味着本文没有经历史资格审定的中心；路线 B 的 7/12 假设根、网格投影和稀少特性正例意味着其概率不能解释为真实采用率；路线 C 的分位数没有历史覆盖校准，外包络也没有概率质量。

工程模型缺少绝对 die area、缺陷密度、bond/attach yield、热阻、真实 BOM、供应与进度分布，亦未建立完整软件性能模型。所有边际分位数可能来自不同联合样本；制造成本与三年能耗只作模型内代理，不能用于报价或 TCO 决策。

两项来源仍为 partial：TSMC 2026 材料不支撑具体成熟良率或 NVIDIA 采用，JEDEC HBM4 材料不支撑产品 stack、容量和带宽。官方 Die Stacking 不证明多横向 compute die 或两个主动计算层，Custom HBM 不证明本文任何数值，平台 CPO 不证明 GPU-package CPO。本文也不把三条路线平均、取交集或包装为共识概率。

## 结论

历史证据支持的 NVIDIA 数据中心 GPU 规格形成逻辑是一个分层、受约束的联合选择过程：在代理时点冻结公开可见信息，把训练/推理/通信需求转成计算、容量、带宽、scale-up、可靠性和 TCO 压力；用制程、封装、HBM、互连、功率、冷却与供应构成可行域；在交付风险和平台协同下联合选择芯片、单卡、节点与机架规格。Volta 到 Rubin 的公开演化与这条机制链一致，但一致性不是对私有目标函数的识别。

定量结论首先是拒绝：路线 A 在 30 个资格单元中没有任何统计合格中心；路线 B 的影响方向可用于敏感性，但 58.33% 的目标根为显式假设且若干特性 Brier 不如基线。因此最终数字只来自路线 C 的具名工程情景。24 个月 balanced/架构未决工作点为约 471.8B 晶体管、296 SM、768 GB HBM、45.3 TB/s HBM 带宽、43.4 PFLOP/s 稠密 FP4、9.18 TB/s 双向 NVLink、2.6 kW 单 GPU、72 GPU 与 323 kW 机架；其同条件带和跨条件外包络必须与数字一起阅读，且均无覆盖概率。

Feynman 的官方事实目前仍是非数值路线图标签：2028 位置、Die Stacking、Custom HBM 与由 Rosa、BlueField-5、NVLink 8 CPO、Spectrum-7 和 ConnectX-10 组成的平台方向。`4T-1L`、12–16 HBM stack、9.18 TB/s、2.6 kW 或 GPU-package CPO 都不是官方披露。未来最有信息量的观察不是另一条趋势线，而是 die 角色与层数、HBM stack/容量/pin rate、NVLink 单 GPU带宽、卡级冷却资格、封装/良率和 CPO 放置；它们将直接触发本文已登记的可行域更新或反证。

## 参考文献

本文末书目收录正文使用的 34 项来源，包括 NVIDIA、TSMC 与 JEDEC 的一手材料，LLM 与 GPU 系统论文，定量方法论文、数据集和标准。TSMC 2026 与 JEDEC HBM4 两项只能获得部分公开内容，正文在相应主张附近保留这一限制，且不以二者支持 NVIDIA 采用、量产良率或具体 Feynman 数值。

## 附录：十项问题覆盖矩阵

| ID | 完整问题 | 定位 | 姿态与限制 |
|---|---|---|---|
| q01 | 对每个历史 GPU 世代，什么日期最接近其规格决策或冻结点，NVIDIA 在该日期之前实际能够观察到哪些定量信号？ | 调查边界、时间线 | partial；内部日期不可见，只能做 18/24/30 个月敏感性。 |
| q02 | 当时的 LLM/HPC 模型规模、训练计算量、精度、上下文、KV Cache、批量、延迟、MoE 通信和推理时扩展需求如何量化？ | 需求问题分类 | answered；公开模型不是客户 workload mix。 |
| q03 | 当时的制程、光罩、晶体管、HBM、封装、互连、功耗、散热、良率、供应和软件条件如何量化及表达不确定性？ | 供给与物理约束 | answered；成熟良率、合同与绝对阈值缺失。 |
| q04 | NVIDIA 从 Volta、Ampere、Hopper、Blackwell/Blackwell Ultra 到最新公开平台实际选择了哪些芯片、显存、计算、互连、功耗与系统规格？ | 历史规格演化 | answered；面板有 43 个统一标签，部分 die 数值未披露。 |
| q05 | 哪个受约束多目标决策模型最能解释 NVIDIA 如何在工作负载效用、TCO、产品分层和交付风险之间选择规格？ | 共同决策框架、三路线 | partial；可解释公开管线，不能复原私有效用。 |
| q06 | 在历史小样本、输出相关和缺失变量条件下，如何识别参数、选择先验或正则化并量化模型不确定性？ | 小样本识别 | answered；以收缩、时间回测与拒绝控制过拟合。 |
| q07 | 数学模型在滚动历史留出回测中能否稳定优于上一代沿用、CAGR 和单变量趋势基线，哪些证据组真正贡献预测力？ | 路线 A、回测与拒绝 | answered；不能稳定优于，0 个统计合格中心。 |
| q08 | 截至当前证据冻结点，模型输入向量和低/中/高情景分别是什么，与历史分布相比是否发生外推？ | 路线 B/C、当前边界 | answered；24 个月为主，18 个月右删失，当前为高压外推。 |
| q09 | 数学模型对下一代 GPU 的计算吞吐、显存容量与带宽、互连、功耗、芯片/系统规模给出什么后验分布和 50%/90% 区间？ | 下一代数值规格 | partial；只给条件 q10/q50/q90 与外包络，不称后验或覆盖区间。 |
| q10 | 新数值格式、注意力/MoE 加速、片上存储、chiplet、scale-up/scale-out、机密计算、MIG、RAS 等特性的采用概率与反证条件是什么？ | 硬件特性、反证规则 | partial；不给已校准采用率，保留官方/工程/未知三层。 |

## 附录：模型与来源可复核信息

最终试验使用答案隔离的历史面板 `real-history-panel-v2.json`，SHA-256 为 `1bed7326efaae56c85c5b4a0c9fa63bf5c2907bf1ad25126766d3dbd10e579e3`。面板的目标世代数值与特性标签均为空；目标输入只能从截点前公开变量形成。最终三路线清单 SHA-256 为 `2e107752d93065be73fc693981f93fc07eab067d9e6f47ec4968cf0d43e621ad`。

路线 A 输出 SHA-256 为 `acf04069cf9b2bf71b9a82be95d99a7d5f2f72f61d3f5910df19e0325efdb771`，使用 18/24/30 个月截点与 4096 后验抽样控制；路线 B 输出 SHA-256 为 `4f54e68dc40e35583c25ac748efce56043ab3d9a1d0fb90f09955f608f1d76bd`，历史回测每折 4000 抽样、目标 20000 抽样；路线 C 输出 SHA-256 为 `47ca57720382f335d46eba1550764a80c5bb64560060a5136a718689044a35e1`，75 条件各 1024 抽样。共同随机种子为 20260827，执行环境为 Python 3.12.14；清单同时记录 Pixi lock 与实现文件哈希。

版本后缀只表示本研究数据与计算的修订序号，不表示模型路线或置信等级：来源总体 r3 含 34 项材料，核心主张审计 r2 含 18 条主张，三路线试验 r2 提供本文数值，综合、审计与稿件版本从各自 r1 起记。更早的同名试验或旧图表不进入本文最终数字；后续更新保留旧哈希和差异。

所有 34 项来源均有稳定身份与来源摘要；16 篇学术论文均完成全文研读。32 项 ready，TSMC 2026 与 JEDEC HBM4 两项 partial。更新登记至少保存：新证据公开时间、采集时间、受影响变量/约束、旧预测哈希、正式观察值、是否越过同条件带或外包络、评分结果、模型修订和新哈希。正式产品数字发布后，旧预测只追加评分，不追溯改写。
