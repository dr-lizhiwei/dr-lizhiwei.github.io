---
layout: post
title: 多云地区时间序列土地利用/覆盖制图
date: 2024-06-05
description: Li Z. et al., 2024, Remote Sens. Environ.
tags: 
thumbnail: assets/img/blogs/2024_lulc mapping/thumbnail.png
---

Li, Z., Weng, Q., Zhou, Y., Dou, P., & Ding, X. (2024). Learning spectral-indices-fused deep models for time-series land use and land cover mapping in cloud-prone areas: The case of Pearl River Delta. *Remote Sensing of Environment*, 308, 114190. [[HTML](https://doi.org/10.1016/j.rse.2024.114190)] [[PDF]](https://zhiweili.net/assets/pdf/2024.7_RSE_Learning%20spectral-indices-fused%20deep%20models%20for%20time-series%20land%20use%20and%20land%20cover%20mapping%20in%20cloud-prone%20areas.pdf)

 

#### **亮点**

- 提出了一种结合深度学习模型和时间序列重建的新颖土地利用与覆盖（LULC）制图方法。
- 在多云和多雨地区（珠三角）实现高时间密度的10米无缝LULC制图。
- 2019-2022年期间，年度制图平均总体精度高达87.01%，优于现有的LULC产品。
- 具有生成无缝近实时分类图和高质量的月度、季度和年度LULC数据集的潜力。




#### **摘要**

使用光学卫星影像进行土地利用和土地覆盖（LULC）动态变化制图可能受到各种云雨天气条件的干扰，这些干扰会导致高时间密度的LULC制图存在空间不连续问题。本研究开发了一种集成的时间序列LULC制图方法，通过结合光谱指数融合的深度学习模型和时间序列重建技术，来提高多云地区LULC制图的精度和频次。该方法首先通过时间序列滤波重建受云污染的像元，在此过程中，由深度模型初始化生成的云掩膜在重建过程中得到优化和更新。然后，将重建的时间序列影像输入到一个基于全球范围收集的样本训练的光谱指数融合深度模型中进行分类。最后，进行分类后处理，包括时空众数滤波和考虑水陆交互的时间序列优化，以提高LULC制图的准确性和一致性。本研究将该方法应用于多云多雨的珠三角地区（即粤港澳大湾区），并使用Sentinel-2时间序列影像作为实验数据。该方法实现了2-5天时间频次的无缝LULC制图，并生成了大湾区地区10米分辨率的年度LULC产品。评估结果显示，2019-2022年连续四年的年度制图的平均总体精度为87.01%，优于现有LULC产品，包括ESA WorldCover (83.98%)、Esri Land Cover (85.26%)和Google Dynamic World (85.06%)。本研究的评估结果还显示了应用不同云掩膜情况下LULC制图精度的显著差异，强调了它们在时间序列LULC制图中的关键作用。该方法有望通过使用全球数据集训练的深度模型为世界范围其它地区生成无缝和近实时的土地利用和土地覆盖图。这一方法可以在不同时间间隔内为多云和多雨地区的各种土地和水体动态提供高质量的LULC数据集。尽管在多云地区获得高质量LULC数据具有挑战性，本研究为LULC动态制图和提供可靠的年度LULC产品提供了一种新方法。

 

#### **1.** **研究背景**

土地利用和土地覆盖（LULC）数据集在土地利用规划和管理、生态环境保护以及农业等应用中起着至关重要的作用。LULC制图一直是一个热门的研究课题，并且随着数据获取和处理能力的进步不断发展。在过去的几十年里，LULC制图的空间分辨率从中分辨率提高到高分辨率，达到了米级甚至亚米级。同时，LULC制图的时间频次也从年度制图提升到近实时制图。最近的机器学习技术，特别是深度学习，极大程度地革新了LULC制图领域，并广泛用于生产新的区域和全球LULC产品。上述方面的LULC制图进展标志着在实现基于密集时间序列影像的精确和连续LULC制图方面取得了重要成果。

尽管如此，在LULC制图领域仍存在两个主要问题。一方面，光学时间序列影像数据中的云覆盖降低了时间序列LULC制图中的数据可用性。同时，精确的云掩膜对于高时间密度近实时LULC制图尤其是在多云地区的重要性不容忽视。然而，常用的云掩膜往往不够精确，仍有进一步改进的空间，这在最近的多项研究中得到了证实。特别是对于Sentinel-2影像，Sentinel-2 Level 1-C云掩膜产品被发现普遍低估了云的存在，这是不可忽视的。其它现有的云检测方法，如Sen2Cor、MAJA和Fmask，在有效区分云和高亮地表以及识别薄卷云和云阴影方面表现出不同的局限性。这些局限性强调了继续改进云检测技术以提升LULC制图能力的必要性。此外，揭示云和不同云掩膜对LULC制图准确性的定量影响也是另一个需要进一步探索的问题。另一方面，识别动态变化的LULC类别，特别是水域变化（如稻田），具有挑战性但对准确的年度LULC制图非常重要。同时，在年度LULC制图中，综合利用一年内所有可用的时间序列影像，有望进一步提升制图精度。

为提高多云和多雨地区的高时间密度LULC制图，本研究提出了一种集成的时间序列LULC制图方法，以改进在密集云覆盖和变化的水域条件下的LULC制图。该方法旨在生成和合成高精度空间无缝的近实时、月度、季度和年度LULC产品。具体地，构建了分别用于云与云阴影检测和LULC分类的融合任务特定光谱指数的深度模型。通过基于时间序列优化的云掩膜精细化，将有望减少云覆盖对LULC制图的影响。同时，时间序列影像中云覆盖区域的重建将有助于提高LULC制图的准确性。特别是后分类处理过程中考虑的时间变化模式有助于识别如农作物等可能频繁发生在水陆交互中的类别。本研究的目标包括：1）开发一种在多雨和多云地区进行高质量时间序列LULC制图的综合方法；2）揭示云对LULC制图的影响以及时间序列重建和使用密集影像时间序列进行LULC制图的益处；3）在研究区域生产一系列优于其它现有产品的LULC产品。该方法有望应用于世界其它地区，特别是在多云地区生成高度可靠的LULC产品。

 

#### **2.** **研究区域和数据**

广东-香港-澳门大湾区（以下简称大湾区）（图1），包含珠江三角洲地区在内的11个主要城市，作为中国最发达的地区之一，在近几十年经历了快速的土地利用和土地覆盖变化。大湾区的多云和多雨天气条件对高时间密度的LULC制图构成了挑战，特别是在每年的雨季，该地区会出现密集的云层覆盖。珠江和沿海环境的存在导致了大湾区中土地和水体相互作用频繁，从而引起LULC类型的高度动态变化。因此，本研究选择大湾区作为研究区域，以检验所提出的方法在多云地区进行LULC制图的有效性。

<div align=center><img src="/assets/img/blogs/2024_lulc mapping/Fig. 1.png" alt="" width="650"/></div>

图1. 研究区域珠江三角洲及该区域Sentinel-2影像月平均云覆盖百分比。上图：研究区域的位置和验证样本点的分布；下图：2019至2022年间研究区域内Sentinel-2影像的平均每月云覆盖百分比。

 

本研究通过GEE平台导出了从2018年12月1日到2023年1月31日跨越4年的大湾区Sentinel-2地表反射率时间序列影像数据集。所有导出的Sentinel-2影像光谱波段的空间分辨率统一重采样为10米，时间分辨率因不同区域而异为2至5天。典型地，Sentinel-2A/B卫星影像每5天覆盖一次大湾区的大部分地区，研究期间总共获得了299次覆盖。在这4年间，大湾区的Sentinel-2时间序列影像中云覆盖密集，估计的平均云覆盖率高达51.61%（基于本研究方法生成云掩膜统计，未包含薄云和云阴影）。图1中提供了每年的月平均云覆盖百分比，这表明由于密集云覆盖，在大湾区进行高质量和高时间密度的LULC制图具有挑战性。为了高效处理密集时间序列影像数据，如图1所示，大湾区的Sentinel-2时间序列被划分为40 × 30部分重叠的影像瓦片进行逐块数据获取和处理，实验仅涉及覆盖大湾区范围的695个瓦片。此外，本研究通过人工解译Google Earth中的高分辨率卫星影像收集样本点，以全面评估时间序列LULC产品。如图1所示，通过分层随机抽样选择了大湾区的1263个样本点，覆盖了2018年12月至2023年1月之间的多个日期，以考虑LULC变化区域。因此，在上述期间内发生LULC变化的样本点将与多个日期和LULC类别关联，而在整个研究期间内同一LULC类别的样本点仅与单一LULC类别关联，以用于对时间序列LULC产品进行更全面的综合评估。

 

#### **3.** **研究方法**

本研究提出了一种集成的多云地区高时间密度LULC制图方法，该方法包含四个主要步骤（图2）。首先，所提出的方法通过基于光谱指数融合深度学习模型生成时间序列Sentinel-2影像的初始云与云阴影掩膜。然后，通过时间序列滤波重建Sentinel-2时间序列影像中被云或云阴影覆盖的像元，在此过程中，初始的云与云阴影掩膜被迭代优化和更新以改善重建效果。接着，将重建后的时间序列影像输入到另一个全球样本库训练的深度模型中进行LULC分类。最后，进行分类后处理，包括时空众数滤波和考虑水陆交互的时间序列优化，以提高LULC制图的准确性和一致性。通过定量评价和与现有LULC产品在大湾区范围进行比较，评估所生成的LULC产品的精度，以及云覆盖对LULC制图的影响。

<div align=center><img src="/assets/img/blogs/2024_lulc mapping/Fig. 2.png" alt="" width="600"/></div>

<center>图2. 本研究所提出的时间序列LULC制图方法流程图</center>  



#### **4.** **结果与分析**

使用覆盖大湾区的4年Sentinel-2时间序列影像作为实验数据，总共存在695块时间序列影像瓦片。所有时间序列影像瓦片都根据图1所示的流程逐块处理，使用预训练的云与云阴影检测模型和LULC分类模型。对于所构建的融合光谱指数的深度学习模型，本研究在云与云阴影检测以及LULC分类两个任务上分别进行了精度验证，均在所对比的方法模型中取得了最佳表现。通过合成和拼接时间序列LULC分类图瓦片，最终可以生成整个大湾区的月度、季度和年度LULC分类图。本研究将生成的大湾区LULC产品命名为GBACover，通过使用人工标记的LULC样本对其进行定量精度评估，并将其与其它全球LULC产品在大湾区进行比较，全球LULC产品在大湾区进行比较，包括ESA WorldCover、Esri Land Cover和Google Dynamic World。所有三个现有的LULC产品均是基于机器学习方法生成，使其与所提出方法生成的LULC产品具有可比性。

考虑到四个比较产品之间的差异，本研究将LULC产品类别颜色方案统一为ESA WorldCover产品的相同方案，LULC类型的命名按照Dynamic World训练数据集中的定义进行统一。评估结果表明，在2019年至2022年连续四年中，GBACover在大湾区年度LULC制图中的总体精度最高。与此同时，Google Dynamic World和Esri Land Cover在个别年份的表现较好。评估显示，GBACover在2019-2022年大湾区年度制图中的平均总体精度为87.01%，优于ESA WorldCover的83.98%（仅2020和2021年平均）、Esri Land Cover的85.26%和Google Dynamic World的85.06%。如果在精度评估中排除ESA WorldCover中的湿地类别，因缺少其验证样本，那么2020年和2021年ESA WorldCover的平均总体精度为85.82%，这高于其实际精度，因为湿地类别的准确识别具有挑战性。值得注意的是，不同时间段合成的LULC产品精度存在时间差异。尽管GBACover在年度尺度上实现了87.01%的平均总体精度，但所提出方法生成的时间序列LULC产品在近实时尺度上的平均总体精度为80.13%。图3展示了2019年至2022年连续4年中大湾区珠江河口地区的年度LULC分类图，其展示了GBACover相对于其它LULC产品在陆地与水体类别转换发生频繁地区（如稻田）的显著差异。

<div align=center><img src="/assets/img/blogs/2024_lulc mapping/Fig. 3.png" alt="" width="900"/></div>

<center>图3. 2019-2022年珠江口区域LULC分类图比较</center>  

本研究还评估了使用不同云掩膜对生成的时间序列LULC分类结果精度的影响。具体地，使用QA60、Sen2Cor、s2cloudless以及所提出的SIFDM模型在时间序列优化前后的掩膜进行比较，以定量评估云和云阴影掩膜精度对LULC制图的影响。具体来说，基于未重建的原始Sentinel-2时间序列影像生成的时间序列LULC分类图，使用大湾区中的人工标记样本进行验证。在验证之前，从生成的时间序列LULC分类图中排除由所比较的掩膜标记的云或云阴影像元，这将使得评估使用不同掩膜进行LULC制图表现成为可能。评估结果表明，利用本研究提出的SIFDM模型生成的优化和初始云掩膜，相较于其它比较的掩膜，在云和云阴影掩膜中表现最佳，分别在时间序列LULC制图中实现了81.16%和68.06%的最佳总体精度。优化后掩膜甚至可以比SIFDM生成的原始掩膜贡献更高的总体LULC分类精度，确认了时间序列优化在提高云掩膜精度方面的益处。更精确的云掩膜有助于提高LULC制图的精度。使用s2cloudless生成的两组掩膜，在灰度掩膜分割的二值化阈值分别为25和50时，分别导致了59.35%和57.04%的总体LULC分类精度。使用Sen2Cor掩膜进行LULC分类的总体精度为64.21%，高于s2cloudless，可能是由于Sen2Cor掩膜中标注了额外的云阴影信息。QA60生成的较不精确的云掩膜导致了47.99%的总体LULC分类精度，用户在应用QA60掩膜进行Sentinel-2影像解译时应注意这一点。此外，值得注意的是，在基于深度学习的卫星影像解译相关研究中，很少考虑云掩膜的精度。这一疏忽引起了对在多云条件下使用光学卫星影像进行陆地和水体动态精确制图的关注。本研究不仅通过结合先进的云掩膜和LULC分类模型提供了一种在多云地区进行LULC制图的综合方法，还评估了云掩膜对LULC制图的影响。评估结果表明，应用不同云掩膜进行LULC制图的精度差异显著，从47.99%到81.16%不等，强调了精确的云掩膜对时间序列LULC制图的重要性。

 

#### **5.** **讨论**

##### **5.1 时间序列重建对LULC制图的益处**

本研究应用Whittaker滤波对影像时间序列中受云与云阴影影响的像元进行重建，以提升多云地区的LULC制图结果。在图4中，以农业用地的LULC制图为例，农业用地可能被水覆盖或种植作物，并且在一年内水和作物之间的土地覆盖类别变化可能会发生多次。在这种情况下，LULC类型（如作物和湿地）的制图结果会随所涉及的影像而变化，导致涉及土地和水体相互作用的LULC类型的分类偏差。由于云覆盖在影像时间序列中随机发生，准确识别涉及土地和水体相互作用的LULC类别变得更加困难。对影像时间序列中受云或云阴影影响的区域进行重建对于准确的LULC制图是必要的，以最小化由随机云覆盖和选取固定时间范围影像引起的时间序列制图中的偏差和错误。基于重建后的无云时间序列影像，可以生成高质量的年度、季度甚至月度的LULC分类图。此外，可以考虑时间序列变化模式来优化制图结果。

<div align=center><img src="/assets/img/blogs/2024_lulc mapping/Fig. 4.png" alt="" width="900"/></div>

图4. 使用原始和重建的无云影像进行时间序列制图的比较。上图：使用原始影像生成的结果，其中时间序列中的缺失点由云覆盖引起。中图：使用重建影像和分类后处理后的时间序列制图结果。下图：基于原始和重建的无云影像获得的NDVI和NDWI时间序列。

 

##### **5.2 使用密集时间序列影像进行年度LULC制图**

现有的年度LULC产品通常基于植被生长期获取的影像生成。然而，光学卫星影像在这些多雨和多云季节遭受密集云层覆盖，导致用于年度LULC制图的无云影像较为有限。因此，年度制图结果仅基于一张或几张有效的卫星观测影像生成。在本研究中，年度LULC分类图基于全年所有可用的Sentinel-2影像生成和合成。此外，进行时间序列LULC分类图的分类后处理，以提高时间序列的一致性并滤除噪声。因此，年度LULC制图的准确性和鲁棒性可以得到提高。使用密集影像时间序列进行LULC制图有望捕捉到周期性的LULC变化模式（例如作物区的土地和水体相互作用），这些模式可以通过时间序列的分类后处理和分析来识别。在图5中，可以从密集时间序列LULC分类图中获取LULC类型的频次，从中可以以高精度和直观的方式定量测量年度LULC变化趋势（例如，四年间从作物到建筑区的变化趋势）。因此，密集时间序列的分类后处理和分析有助于提升LULC制图的准确性和鲁棒性。

<div align=center><img src="/assets/img/blogs/2024_lulc mapping/Fig. 5.png" alt="" width="900"/></div>

图5. 从年度LULC频次图中识别变化趋势的示例。在此示例中，可以从其相应的年度LULC频次图清晰地解译从作物到建筑区的过渡，这些频次图是基于密集时间序列LULC分类图生成的，并表示在一年内检测到某一类别的次数与观测总次数的比例。

 

##### **5.3 局限性**

尽管所提出的时间序列LULC制图方法在云掩膜和LULC分类方面优于比较方法，但所提出方法仍存在局限性。一方面，深度模型的性能受限于本研究中使用的训练样本的数量和质量，特别是用于训练LULC分类模型的Dynamic World训练数据集，该数据集粗糙且缺乏对象边界细节，从而限制了模型在识别桥梁和道路等小尺寸细物体方面的表现，仍有通过高质量训练标签进行进一步改进的空间。同时，通过使用最新的深度模型结构（如基于视觉Transformer的基础大模型，可以进一步提高深度模型的性能，这些模型已被证明在影像解译中有效，可以挖掘所提出方法的潜力。另一方面，由于所提出的制图方法涉及多个步骤，尤其是云与云阴影检测、时间序列重建和LULC分类，可能会发生累积的处理错误。此外，由于云的遮挡，短期的LULC变化可能无法有效重建和捕捉，或者可能在分类后处理过程中被平滑，这将导致近实时和每月尺度的LULC制图精度下降。

 

#### **6. 结论**

本研究提出了一种使用密集Sentinel-2时间序影像列进行LULC制图的综合方法。尽管在不同时间尺度上的分类精度上存在差异，该方法可以用于多云地区的近实时、月度、季度和年度制图。通过开发深度模型以提高云掩膜和LULC分类的准确性、采用时间序列重建方法填补云覆盖区域、并应用时间序列分类后处理和分析，提出的方法在云掩膜和LULC分类方面展示出了优越性。在粤港澳大湾区的应用表明，该方法可以生成准确的LULC分类图，在年度尺度上的平均总体精度为87.01%，在近实时尺度上的精度为80.13%，优于比较的年度LULC产品。本研究评估了云覆盖对LULC制图的影响，提出了开发先进云与云阴影检测方法以提高LULC制图精度的必要性，这在本研究中已得到验证。本文还讨论了时间序列重建和使用密集时间序列影像进行LULC制图的益处，展示了它们对LULC制图的贡献，特别是在改善涉及陆地和水体交互的LULC类型以及多云地区的制图结果方面。

所提出方法中的深度模型是在全球收集的数据集上训练的，因而可以用于研究区域以外的其它地区的LULC制图。同时，所提出的方法还可以用于单一LULC类别的近实时监测（例如农田、湿地和淹没土地的时间序列监测），因此具有广泛的潜在应用。然而，所提出的方法在深度模型性能和多重处理步骤带来的误差传播方面的局限性留有很多改进空间，例如与最新的基础大模型集成以及在LULC分类图生产过程中引入质量控制。此外，研究区的实地调查是进一步验证LULC产品所必需的，特别是在具有挑战性的制图场景中，例如草地/灌木、湿地和淹没植被类别。未来，随着更先进的深度模型（例如基础大模型）的引入和多模态数据（例如Sentinel-1和Sentinel-1的结合）的应用，多云和多雨地区的密集影像时间序列LULC制图可以得到进一步增强。SAR影像的潜力可以得到充分利用，以有利于在持续云覆盖期间识别土地动态变化。

 

#### **主要作者简介：**

**李志伟**，博士，香港理工大学土地测量及地理资讯学系研究助理教授。主要研究兴趣为多云多雨环境遥感，研究方向包括卫星影像云检测与去除，多源数据融合，土地覆盖制图，洪水监测等。个人主页：https://zhiweili.net/。

 

**翁齐浩**，欧洲科学院外籍院士、 美国科学促进会（AAAS）‍会士、电气与电子工程师协会（IEEE）会士、美国地理学会（AAG）会士、美国摄影测量与遥感学会（ASPRS）会士、亚太人工智能学会（AAIA）会士，现任香港理工大学地理信息学和人工智能讲座教授、曾任美国印第安纳州立大学城市与环境变化中心主任和教授和美国航天局高级研究员。现为地球观测组织的全球城市观测和信息系统项目负责人并任《国际摄影测量与遥感学会期刊》（ISPRS J P&RS）主编。翁教授的研究侧重于遥感科学和技术在城市环境与生态系统中的应用、土地利用和土地覆盖的变化和城市化的环境效应等。



论文已支持Open Access，点击[阅读原文](https://doi.org/10.1016/j.rse.2024.114190 )即可获取全文。