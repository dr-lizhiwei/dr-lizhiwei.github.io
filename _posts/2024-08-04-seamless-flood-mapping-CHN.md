---
layout: post
title: "突破云遮挡：基于 HLS 时间序列与历史水体数据的洪水无缝制图"
date: 2024-08-04
description: Li Z. et al., 2024, ISPRS J. Photogramm. Remote Sens.
lang: zh-CN
tags:
thumbnail: assets/img/blogs/2024-seamless-flood-mapping/thumbnail.png
---

Li, Z., Xu, S., & Weng, Q. (2024). Beyond clouds: Seamless flood mapping using Harmonized Landsat and Sentinel-2 time series imagery and water occurrence data. *ISPRS Journal of Photogrammetry and Remote Sensing*, 216, 185–199. [[HTML](https://doi.org/10.1016/j.isprsjprs.2024.07.022)] [[PDF]({{ '/assets/pdf/2024.10_ISPRS P&RS_Beyond clouds：Seamless flood mapping using Harmonized Landsat and Sentinel-2 time series imagery and water occurrence data.pdf' | relative_url }})] [[Code](https://github.com/dr-lizhiwei/SeamlessFloodMapper)]

#### **研究亮点**

- 提出 **SeamlessFloodMapper**，补全时间序列水体图中因云及云阴影遮挡而缺失的水体分类信息。
- 结合微调后的遥感基础模型、历史水体出现频率和时空优化，提高时序制图的完整性。
- 利用经一致化处理的 Landsat 与 Sentinel-2（HLS）影像，实现 **30 米分辨率**的洪水范围制图；联合观测通常可提供约 **2 至 3 天**的影像获取间隔。
- 在论文的模拟云遮挡试验中，洪水期平均重建 F1 分数由对比方法的 **0.871 提高至本文方法的 0.931**，洪水前后则由 **0.772 提高至 0.903**。
- 公开源代码、预训练模型与实验数据，支持方法复现和进一步研究。

#### **摘要**

洪水发生时，光学卫星观测往往受到云覆盖影响，水体图因此出现空间缺失。本研究利用经一致化处理的 Landsat 与 Sentinel-2（HLS）时间序列影像，开发了适用于多云多雨条件的洪水无缝制图方法。首先，利用微调后的遥感基础模型提取可观测区域的水体；随后，结合全球地表水（GSW）数据集中的历史水体出现频率，通过自适应局部阈值和“次最大稳定性”假设，重建被云及云阴影遮挡区域的水体分类信息；最后，利用时空马尔可夫随机场提高时序水体图的一致性。四个研究区的实验表明，该方法能够提高云遮挡区域的水体重建精度，并改善最大淹没范围和淹没持续情况的表达。研究还讨论了严重云遮挡下的不确定性，以及引入合成孔径雷达（SAR）数据进一步增强监测能力的可能性。

#### **1. 研究背景**

洪水监测需要兼顾观测及时性与空间完整性。Landsat 和 Sentinel-2 的联合观测提高了可用影像数量，但频繁云覆盖仍会在水体图中留下大面积空缺。直接舍弃有云影像，会减少追踪洪水快速变化所能利用的信息。

已有水体图补全方法为此提供了基础，但洪水变化通常比常年或季节性水体更快。对于低频发生洪水的区域，历史水体出现频率也可能存在较大不确定性。因此，本研究重点探索如何将当前可见的水体信息与历史水体记录结合，在不同云况下恢复空间连续的水体分布。

#### **2. 数据与研究区**

HLS（Harmonized Landsat and Sentinel-2）将 Landsat 与 Sentinel-2 观测进行一致化处理，生成 30 米地表反射率产品。两类卫星的联合观测通常可提供约 2 至 3 天的影像获取间隔，但实际可用观测仍受地点、影像覆盖范围和云况影响。云与云阴影掩膜来自 HLS 的质量标识（QA）波段。

这里的“无缝”指补全每个观测时刻水体图的空间空缺，并不意味着连续、无间断地直接观测洪水过程。

研究选择了 **印度阿萨姆邦、巴基斯坦信德省、巴西南里奥格兰德州和美国密歇根州**四个区域，涵盖大范围降雨洪水和溃坝洪水，以及不同的云覆盖和观测条件。

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-4.png" alt="四个洪水研究区的位置及HLS影像时序的云覆盖分布" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1434" height="739" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">原文图 4：四个研究区的位置及 HLS 时间序列的云覆盖分布。底图来源：NASA Visible Earth。</figcaption>
</figure>

#### **3. 研究方法**

该方法包括水体提取、云下水体重建和时间序列优化三个主要步骤。

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-1.png" alt="水体提取、云下水体重建及时空优化的整体流程" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1437" height="670" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">原文图 1：时间序列洪水无缝制图方法的整体流程。</figcaption>
</figure>

##### **3.1 基于遥感基础模型的水体提取**

研究在 Sen1Floods11 数据集上进一步微调 Prithvi-100M–Sen1Floods11 预训练模型。模型输入包括 HLS 的蓝、绿、红、窄近红外及两个短波红外波段，输出水体与非水体分类图。被云及云阴影遮挡的像元标记为缺失观测，留待后续重建。

##### **3.2 利用历史水体出现频率自适应重建**

历史水体出现频率表示某个位置在过去有效观测中出现水体的频率。本文采用的 GSW 水体出现频率数据基于 1984—2021 年的 Landsat 历史观测生成。

在自适应局部窗口内，方法将无云像元按历史水体出现频率分组，计算每组中当前识别为水体的像元占该组全部无云像元的比例。依据 **“次最大稳定性”（submaximal stability）假设**，利用这一比值随历史水体出现频率增加而总体上升的趋势，确定局部重建阈值。与直接使用像元数量相比，比值有助于减弱不同云量和水体变化对阈值选择的影响。

若某个云遮挡像元的历史水体出现频率高于局部阈值，则将其判定为水体，否则判定为非水体。这一步补全的是水体分类信息，而非恢复光学影像的光谱值。自适应窗口则用于适应不同区域的水体变化差异。

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-3.png" alt="利用局部统计与历史水体出现频率重建云下水体的示例" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1420" height="712" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">原文图 3：利用历史水体出现频率和局部分布统计重建云覆盖区域水体类别的示例。</figcaption>
</figure>

##### **3.3 时空优化与洪水范围识别**

时空马尔可夫随机场综合利用空间邻近像元和时间相近的观测，减少时序水体图中的分类不一致。优化时，重建像元的权重低于直接观测像元，以降低重建误差的影响。随后，以洪水发生前一段时间内的最大水体范围为基准，将这一范围之外新增的水体识别为洪水淹没区，并进一步合成最大水体范围与洪水持续时间指标等产品。

#### **4. 结果与分析**

##### **4.1 云覆盖条件下的时序洪水变化**

四个研究区的结果展示了该方法如何在连续 HLS 观测中补全水体图的空间空缺。与保留云覆盖缺失区域的初始水体图相比，重建后的时间序列能够更完整地表达洪水扩张和消退过程。

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-5.png" alt="四个研究区连续影像的初始与重建水体图对比" class="img-fluid" style="width:100%; max-width:760px; height:auto;" width="1250" height="1678" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">原文图 5：印度、巴基斯坦、巴西和美国研究区的时间序列水体重建示例。</figcaption>
</figure>

##### **4.2 云下水体重建精度**

论文在人工标注的参考水体图上叠加不同云量的云掩膜，模拟水体分类信息缺失的情形，定量评价重建表现，并与 Zhao 和 Gao（2018）的补全方法进行比较。

| 评价时期 | 对比方法平均 F1 | 本文方法平均 F1 | F1 绝对增量 |
| --- | --- | --- | --- |
| 洪水发生期间 | 0.871 | 0.931 | 0.060 |
| 洪水前后 | 0.772 | 0.903 | 0.131 |

这些 F1 分数是不同云量条件下的平均重建结果，用于衡量模拟云遮挡条件下的水体图重建表现，并非整套洪水监测流程的总体精度。研究还采用 3 米分辨率的 PlanetScope 影像进行目视对照；由于成像时间和云况可能不同，这部分对照不作为严格的逐像元定量验证。

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-8.png" alt="重建洪水图与独立PlanetScope高分辨率影像的对比" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1334" height="1028" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">原文图 8：重建洪水范围与独立 PlanetScope 高分辨率影像的对照。</figcaption>
</figure>

##### **4.3 最大淹没范围与洪水持续时间指标**

缺失观测还会影响从时间序列中合成的最大淹没范围和洪水持续时间指标。补全云遮挡区域后，这些衍生产品的空间完整性和一致性得到改善，有助于识别原始观测可能遗漏的受淹区域。

论文中的洪水持续时间图以时序观测中的淹没出现频率来表征持续情况，并非逐小时记录的实际受淹时长；解读时还需考虑观测间隔及重建误差。

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-9.png" alt="原始与重建水体时间序列合成的最大水体范围及洪水持续时间" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1434" height="1175" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">原文图 9：基于原始与重建水体图合成的最大水体范围及洪水持续时间对比。</figcaption>
</figure>

#### **5. 讨论与局限**

方法性能取决于水体提取精度、云掩膜质量，以及可用的无云观测信息。持续、密集的云覆盖会增大重建不确定性。根据论文的模拟试验，若希望重建 F1 分数通常高于 0.8，建议将方法用于云覆盖比例低于 96% 的情形。这一经验条件仅适用于论文测试的场景，不能视为任意区域或洪水事件的精度保证。

对于超出历史常见淹没范围的极端洪水，历史水体出现频率可能不足以支撑可靠重建，从而遗漏部分受淹区域。植被遮挡造成的水体漏检、云阴影与水体混淆，以及初始云掩膜误差也会影响结果。SAR 观测能够提供补充信息，但融合时需要处理光学与 SAR 成像机制不同所造成的水体图差异。

#### **6. 结论**

SeamlessFloodMapper 结合遥感基础模型水体提取、基于历史水体出现频率的自适应重建，以及时空一致性优化，增强了多云条件下光学影像时间序列的洪水监测能力。四个研究区的结果表明，该方法能够提高重建精度和水体图的空间完整性，并改善洪水衍生产品。公开的代码和数据也为进一步评价和改进该方法提供了基础。

#### **代码与资源**

- [源代码](https://github.com/dr-lizhiwei/SeamlessFloodMapper)
- [预训练模型与数据](https://drive.google.com/drive/folders/1c57gKA1L6q0v36gaPfBn0a3XnN1cYjwF?usp=sharing)
- [补充材料]({{ '/assets/pdf/2024.10_ISPRS P&RS_Seamless flood mapping_Appendix A Supplementary data.pdf' | relative_url }})

<p class="mt-4 text-muted"><small>请注意：以上内容由 AI 根据原始论文整理与翻译。</small></p>
