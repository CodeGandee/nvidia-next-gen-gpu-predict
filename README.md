# NVIDIA 下一代数据中心 GPU 预测（v2）

本仓库是 `nvidia-next-gen-dc-gpu-v2` Kaoju 调研工作区的净化发布快照，主报告使用中文。研究目标是结合历代 NVIDIA 数据中心 GPU、同时代 LLM 工作负载、制造与封装约束以及 GPGPU 研究，建立可回测的定量规格预测模型，并给出下一代产品规格和硬件特性的条件预测。

## 快速入口

- [最终中文 PDF 报告](records/artifacts/research-records/artifact/artifact-paper-pdf-10d36fbb236e/template.pdf)
- [最终 MyST/Markdown 稿](records/artifacts/research-records/artifact/artifact-kaoju-paper-draft-myst-nvidia-next-gen-dc-gpu-v2-final-r8/paper-final-r4.myst.md)
- [主张状态表](records/views/research-records/view_manifest/view-kaoju-claim-status-table-nvidia-next-gen-dc-gpu-v2-final-r1/payload.json)
- [引用映射](records/artifacts/research-records/artifact/artifact-kaoju-citation-map-nvidia-next-gen-dc-gpu-v2-final-r3/payload.json)
- [研究目标与问题定义](intent/src/topic-overview.md)

## 快照范围

该快照仅来自 v2 Topic Workspace，不包含或依赖 v1 调研工作区。仓库保留研究自产的意图、中文报告、模型结果、数据表、审计记录、引用与可追溯性元数据。

为避免未经确认的第三方再分发，快照不包含第三方论文原文、抓取的网页与文本镜像、外部源码仓库、ACM LaTeX 模板、原始运行日志、临时文件、`state.sqlite` 或任何嵌套 `.git` 元数据。材料获取记录仍保留来源身份、链接、校验值和许可证姿态，读者应从原始发布方合法获取资料。

部分研究记录中的本地绝对路径属于生成时的溯源信息，克隆后可能不可解析；对应的托管内容位于同一记录目录时，应以仓库内相对路径为准。

## 许可说明

仓库未附加统一开源许可证，不应推定研究内容或其中引用材料获得了额外授权。第三方名称、商标、论文和数据的权利归各自权利人所有。

## 完整性

`SNAPSHOT-MANIFEST.sha256` 记录本次净化快照中除清单自身和 Git 元数据以外所有文件的 SHA-256，可用于核验下载内容。
