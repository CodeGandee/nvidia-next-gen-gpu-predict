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

本文研究的不是“按历代增速猜下一代”，而是一个带时间因果约束的问题：在每一历史世代的规格代理决策时点之前，公开观察者能够看到哪些工作负载、制程、HBM、封装、互连、功耗与软件信号；这些信号如何移动可行域并改变联合规格选择；同一方法在滚动历史留出中是否优于朴素基线。证据库含 34 项材料，其中 16 篇学术论文均完成全文研读，32 项来源就绪，TSMC 2026 技术材料与 JEDEC HBM4 材料因访问粒度受限保留为部分证据。我们在一个答案隔离的 9 事件历史面板上比较三条不可混合的路线：环境回归统计外推、贝叶斯预测影响图、可行域约束工程设计空间。路线 A 的 18 个变体中 10 个可执行、8 个因无可评分折而拒绝；30 个资格单元中统计合格数为 0，故不发布统计中心。路线 B 的六折回测揭示 12 个目标根变量中 7 个仍依赖显式假设，且低精度代理的平均绝对对数误差为 0.982；它只用于敏感性和影响方向，不代表 NVIDIA 内部决策网络。路线 C 在 3 个时点、5 个架构条件与 5 组目标权重上形成 75 个条件，每条件抽样 1024 次。其 24 个月、balanced、架构未决条件给出的边际工程工作点为：471.8B 晶体管、296 SM、768 GB HBM、45.3 TB/s HBM 带宽、43.4 PFLOP/s 稠密 FP4、9.18 TB/s 双向 NVLink、2.6 kW 单 GPU、72 GPU 与 323 kW 机架；这些数值不是最可能值，同条件 q10/q90 不是置信区间，跨 25 条件外包络也没有覆盖概率。GTC 2026 对 Feynman 的官方边界仅包括 2028 路线图位置、Die Stacking、Custom HBM、Rosa CPU、BlueField-5、NVLink 8 CPO、Spectrum-7 204T CPO 与 ConnectX-10，并未披露任何 GPU 数值规格。全文据此把可支持结论、条件工程判断与未知严格分开，并给出逐项反证和更新规则。

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

### 共同决策框架

路线 A 的连续观测模型以规格对数增长为响应。对指标 $k$、世代转移 $g-1\rightarrow g$，令

$$
r_{gk}=\frac{\log y_{gk}-\log y_{g-1,k}}{\Delta t_g},\qquad r_{gk}=\alpha_k+x_g^\top\beta_k+\varepsilon_{gk},
$$

其中 $\Delta t_g$ 是两次公开事件之间的年数，$x_g$ 是严格在截点前可得且经过标准化的需求或供给代理，$\alpha_k$ 是截距，$\beta_k$ 是带经验贝叶斯 ridge 收缩的系数，$\varepsilon_{gk}$ 是高斯增长误差；由此在对数规格上形成 Student-$t$ 预测分布。资格不是“模型跑通”，而是滚动历史留出中相对上一代沿用、log-drift/CAGR 和单变量趋势基线，在多数折上改善误差和 proper score，保持方向与区间覆盖，并通过分布外与杠杆诊断。Proper scoring rule 的目的正是同时惩罚错误中心和不恰当不确定性 {cite}`gneiting2007scoring`；时间序列预测中的 leave-future-out 逻辑要求训练数据严格早于验证结果 {cite}`burkner2020lfo`。

路线 B 把根变量 $X$、中间压力 $Z$、连续规格 $Y$ 与离散特性 $H$ 因子化为

$$
p(Y,H,Z,X\mid I_g)=p(X\mid I_g)\prod_j p(Z_j\mid \operatorname{pa}(Z_j))\prod_k p(Y_k\mid \operatorname{pa}(Y_k))\prod_m p(H_m\mid \operatorname{pa}(H_m)),
$$

其中 $\operatorname{pa}(\cdot)$ 表示图中的父节点。公开派生根有日期与区间；无法观察的 memory demand、scale-up demand、供应信心、软件成熟度、TCO 压力等根以宽先验标记为 assumption。连续输出最后投影到可行规格网格，离散节点用 Brier score 回测。这个图没有 decision 或 utility 节点，因此它是预测影响图，不是 NVIDIA 的决策网络。

路线 C 先抽取工艺、tile、主动层、HBM、SerDes、频率、功耗和机架条件 $\theta$，只保留满足 $c_j(y,h,a,\theta)\le 0$ 的样本，再对目标权重 $w$ 求

$$
s^*(\theta,a,w)=\underset{s\in\mathcal{G}(a),\;c_j(s,\theta)\le 0}{\operatorname{argmax}}\; w^\top q(s,\theta)-\rho(s,\theta),
$$

其中 $\mathcal{G}(a)$ 是架构 $a$ 下的离散规格网格，$q$ 是训练计算/功率、decode 内存/功率、HBM 容量、NVLink/功率和生命周期效率的归一化目标，$\rho$ 是制造、能耗与交付风险代理。对条件 $c=(\tau,a,w)$ 收集可行最优样本后报告边际分位数 $Q_{0.1}(Y_k\mid c)$、$Q_{0.5}(Y_k\mid c)$ 和 $Q_{0.9}(Y_k\mid c)$。这些是模型内部条件分位数，不是历史校准的概率区间。

三类回测分数统一按实际可评分的历史留出数 $n$ 计算，且数值越低越好。对正的连续规格，平均绝对对数误差定义为 $\operatorname{MALE}=n^{-1}\sum_{i=1}^{n}\lvert\log \hat y_i-\log y_i\rvert$，其中 $\hat y_i$ 是点预测、$y_i$ 是观察值。若 $F_i$ 是第 $i$ 个留出结果的预测累积分布函数，则连续秩概率分数为 $\operatorname{CRPS}=n^{-1}\sum_{i=1}^{n}\int_{-\infty}^{\infty}[F_i(z)-\mathbf{1}\{y_i\le z\}]^2\,\mathrm{d}z$。对二元特性，Brier score 定义为 $n^{-1}\sum_{i=1}^{n}(p_i-o_i)^2$，其中 $p_i$ 是预测概率，$o_i\in\{0,1\}$ 是结果。这里的 $n$ 不是面板总事件数；缺少预测或可比较标签的折不进入分母。CRPS 的量纲随目标而变，因而只在同一指标、同一截点和相同结果尺度内比较。

### 路线 A：历史统计外推及其拒绝

路线 A 对 card power、SM、HBM 容量、HBM 带宽、scale-up 带宽和晶体管六个指标各预声明 mechanism-supply、workload-demand、demand-plus-supply 三个变体，共 18 个变体；每个可执行变体在 18、24、30 个月截点上评估。数据要求严格，某个截点若没有足够早期预测变量和可比较标签就不补值，直接形成拒绝。

结果是 10 个变体完成拟合、8 个因没有可评分的滚动留出折而拒绝。10 个完成变体产生 30 个“变体×截点”资格单元，其中 6 个没有可评分折，其余单元最多只有 1–4 折；15 个单元少于最低留出折数，21 个单元的平均绝对对数误差差于最佳朴素基线，23 个单元的 CRPS 改善缺失或被单一折支配，12 个单元至少含一个预声明分布外留出点。统计合格单元数、合格变体数和通过资格审定的预测中心数均为 0。

这不是只由保守阈值造成的形式拒绝。两个能形成可评分折的预注册主模型在 18 个月截点上均发生数量级失控：SM 模型只有 3 个留出折，平均绝对对数误差为 17.008，而最佳朴素基线为 0.307；其平均 CRPS 约为 $3.98\times10^{108}$，基线为 32.19。晶体管模型只有 4 个留出折，平均绝对对数误差为 6.838，对应基线为 0.264；其平均 CRPS 约为 $1.47\times10^{72}$，基线约为 $1.86\times10^6$。CRPS 只在同一指标与同一截点内比较；这里的数量级爆炸揭示小样本外推和尾部分布失控，不用于跨指标排序。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig06-route-a-eligibility-r1}}

下图按指标比较路线 A 与最佳朴素基线的历史误差。个别单元或指标可以局部改善，但资格规则要求在合理截点、关键输出和 proper score 上稳定改善；挑选局部胜者会把小样本噪声变成事后模型选择。技术预测文献同样警告，强共趋势与少量技术世代会制造貌似稳定的指数规律，而样本外误差通常比拟合内曲线更能约束结论 {cite}`farmer2016predictable`。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig07-route-a-error-r1}}

因此，路线 A 的正确产出是负结果：历史公开环境回归没有获得发布中心的资格。即使某些被拒绝拟合可以算出中位数和宽区间，这些数字也不进入 Feynman 规格表，不用于收窄路线 B 或 C，更不能被称作“统计预测”。

### 路线 B：贝叶斯预测影响图

路线 B 含 12 类目标根变量。compute demand、cooling headroom、HBM readiness、link readiness 和 process headroom 可由带日期的公开量映射；memory demand、packaging readiness、reliability pressure、scale-up demand、software readiness、supply confidence 与 TCO pressure 仍需宽的序数假设。因此目标根的显式假设比例为 $7/12=58.33\%$，而这个比例只是主观性的下限：五个“derived”根仍依赖人为归一化区间、等权组合或替代量。特别是 process headroom 不等于 foundry yield，cooling headroom 只是已部署功率等级的能力代理，packaging readiness 不含 CoWoS 产能、attach/bond yield、成本或进度。compute、memory 与 scale-up demand 又共享同一个 frontier-compute 中心代理 0.835，导出图没有共同观测父节点或协方差结构，因而不能排除同一信号被重复放大的可能。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig08-route-b-root-audit-r1}}

在六个时间顺序留出折上，第一折没有可用规格预测，其余连续指标实际只有 5 个留出结果，TDP 只有 4 个。平均绝对对数误差分别为：晶体管 0.138、NVLink 双向带宽 0.205、TDP 0.287、HBM 带宽 0.384、HBM 容量 0.474、frontier low-precision 代理 0.982。除低精度代理的 90% 网格区间覆盖为 0.8 外，其余为 1.0；但这里的“1.0”至多表示 4/4 或 5/5。六个连续输出有 99.990%–99.995% 的抽样被投影到离散可行网格，宽区间和上界聚集会机械提高覆盖，不能据此声称良好校准。

{{figure:artifact-kaoju-paper-display-nvidia-next-gen-dc-gpu-v2-final-fig09-route-b-male-r1}}

离散特性的平均 Brier score 与常数频率基线提供更直接的反证。HBM 代际步进为 0.273 对 0.315，多计算裸片为 0.293 对 0.386，rack power smoothing 为 0.137 对 0.202，表面上有所改善；但 power smoothing 历史上只有 1 个正例。新数值格式为 0.334 对 0.302、NVLink 代际步进为 0.289 对 0.202，均差于基线。GPU-package CPO 为 0.020 对 0.102，看似较好，却来自 0 个历史正例，实际只奖励“持续预测低概率”，不能验证采用概率。

当前未条件化影响图均值为：多计算裸片 0.751、HBM 代际步进 0.752、新数值格式 0.721、NVLink 代际步进 0.855、功率平滑 0.379、GPU-package CPO 0.212。该目标影响图的决策截点为 2026-08-27，故可使用 2026-04-07 的官方路线图；它与严格停在 2026-03-20 的路线 C 主条件不是同一信息集。GTC 2026 已明确列出 NVLink 8，只有语义完全相同的“NVLink 代际步进”节点可以固定为 true；固定后的数值 1.0 是已披露条件，不是模型置信度。由于新数值格式和未条件化 NVLink 的 Brier 均差于基线，CPO 没有正例，power smoothing 只有一个正例，正文不把上述均值发布为产品采用概率。

为说明语义冲突，路线 B 的网格投影中位数包括 672B 晶体管、576 GB HBM、56 TB/s HBM 带宽、7.2 TB/s 双向 NVLink、2.8 kW TDP 与 200 PFLOP/s 的 frontier low-precision 代理。它们受宽假设根和网格上界影响；其中 low-precision 代理没有定义成路线 C 的稠密 FP4，故不能比较或平均。该表仅是模型诊断，不是最终预测中心。

### 路线 C：可行域约束的工程设计空间

路线 C 在 30、24、18 个月三个信息时点上，分别组合五类架构条件和五组目标权重。下文以 `2T-1L` 表示两个横向 compute tile 与一个主动逻辑层，其余记号同理；五类架构为“架构未决网格优化器”、`2T-1L`、`2T-2L`、`4T-1L`、`4T-2L`。权重包括 balanced、training-centric、memory-centric、scaleup-centric、lifecycle-centric。三个时点、五类架构和五组权重取笛卡尔积，共 75 个条件，每条件请求 1024 个样本。balanced 权重依次为训练计算/功率 0.31、decode 内存/功率 0.19、HBM 容量 0.14、NVLink/功率 0.14、生命周期效率 0.22；其他四组权重用于检验目标函数敏感性，而不是 NVIDIA 客户份额。

24 个月的 25 个条件共请求 25,600 个样本，其中 25,588 个找到模型内可行结果，最低单条件可行率为 0.9980；这只是优化器满足内置不等式的比例，不是芯片/封装良率或量产成功率。balanced、架构未决主条件下 1024/1024 样本通过模型可行性筛选。优化器的模型内部选择频率为：4 个横向 tile 83.2%、1 个主动逻辑层 91.7%、16 个 HBM stack 62.7%、72 GPU 机架 64.9%。这些比例来自输入分布和目标函数下的设计选择频率，不是 NVIDIA 采用概率。约束绑定频率中，package assembly 99.2%、package footprint 60.1%、card cooling 57.2%、rack power 31.2%、compute power 24.5%、HBM controller 15.3%、die yield 6.6%；由于缺少绝对缺陷密度、bond yield 与热阻数据，绑定频率只能解释模型内部瓶颈。四个历史 sanity check 只表明已知 A100、H100、B200 和 Rubin 没有越出若干内置容量边界；它们不是训练外预测校准，且 B200 的 transistor-capacity 项未核。

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
