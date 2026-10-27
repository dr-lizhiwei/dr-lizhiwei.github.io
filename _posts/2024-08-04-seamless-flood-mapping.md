---
layout: post
title: "Beyond clouds: Seamless flood mapping with Landsat and Sentinel-2 time series"
date: 2024-08-04
description: Li Z. et al., 2024, ISPRS J. Photogramm. Remote Sens.
seo_description: SeamlessFloodMapper reconstructs cloud-covered water maps using HLS time series and historical water occurrence, with four-site experiments and open code and data.
lang: en
translation_key: seamless-flood-mapping
tags:
thumbnail: assets/img/blogs/2024-seamless-flood-mapping/thumbnail.png
---

Li, Z., Xu, S., & Weng, Q. (2024). Beyond clouds: Seamless flood mapping using Harmonized Landsat and Sentinel-2 time series imagery and water occurrence data. *ISPRS Journal of Photogrammetry and Remote Sensing*, 216, 185–199. [[HTML](https://doi.org/10.1016/j.isprsjprs.2024.07.022)] [[PDF]({{ '/assets/pdf/2024.10_ISPRS P&RS_Beyond clouds：Seamless flood mapping using Harmonized Landsat and Sentinel-2 time series imagery and water occurrence data.pdf' | relative_url }})] [[Code](https://github.com/dr-lizhiwei/SeamlessFloodMapper)]

## **Highlights**
{: .h4}

- Develop **SeamlessFloodMapper** to reconstruct missing water-map labels in areas obscured by clouds and cloud shadows.
- Combine a fine-tuned foundation model, historical water occurrence, and spatiotemporal refinement.
- Support spatially seamless flood mapping at **30 m resolution**, using combined HLS observations with typical acquisition intervals of approximately **2–3 days**.
- Achieve average reconstruction F1-scores of **0.931 during floods** and **0.903 before/after floods**, compared with **0.871** and **0.772** for the benchmark method in the reported simulation experiments.
- Release source code, a pretrained model, and experimental datasets.

## **Abstract**
{: .h4}

Clouds often obscure optical satellite observations at the time when flood information is most needed. This study develops a reconstruction approach for spatially continuous flood monitoring with Harmonized Landsat and Sentinel-2 (HLS) image time series. A fine-tuned foundation model first extracts visible water areas. Historical water occurrence from the Global Surface Water (GSW) dataset then supports the reconstruction of water-map labels in areas obscured by clouds and cloud shadows, using an adaptive local threshold and a submaximal stability assumption. Spatiotemporal Markov random field modeling improves the consistency of the reconstructed sequence. Experiments at four sites show improved reconstruction accuracy and more complete representations of maximum inundation and inundation persistence. The study also discusses uncertainty under heavy cloud cover and the potential for synthetic aperture radar (SAR) data to improve monitoring.

## **1. Introduction**
{: .h4}

Flood monitoring requires both timely observations and spatially complete information. Combining Landsat and Sentinel-2 increases the number of available optical observations, but frequent cloud cover can still leave large gaps in water maps. Discarding cloudy scenes reduces the information available for following rapidly changing flood events.

Existing water-map gap-filling methods provide a useful starting point, but floodwater changes more rapidly than many permanent or seasonal water bodies. Historical water occurrence can also be uncertain in areas that flood infrequently. We therefore investigate how current clear-sky observations and historical water information can be combined to reconstruct water maps under changing cloud conditions.

## **2. Data and study sites**
{: .h4}

HLS combines Landsat and Sentinel-2 observations into harmonized 30 m surface reflectance products. The combined observations support a typical acquisition interval of approximately 2–3 days, although usable observations depend on location, image coverage, and cloud conditions. Cloud and cloud-shadow masks are obtained from the HLS quality-assessment (QA) band.

Here, “seamless” refers to filling spatial gaps in water maps at the available observation dates; it does not imply uninterrupted direct observation of a flood.

Four study sites represent different flood processes and observation conditions: **Assam, India; Sindh, Pakistan; Rio Grande do Sul, Brazil; and Michigan, USA**. They include widespread rainfall-driven floods and a dam-failure event, providing different tests of changing water extent and cloud coverage.

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-4.png" alt="Locations of the four flood study sites and their HLS cloud cover distributions" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1434" height="739" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">Fig. 4 from the paper. Study-site locations and cloud-cover distributions in the HLS time series. Basemap credit: NASA Visible Earth.</figcaption>
</figure>

## **3. Methodology**
{: .h4}

The method contains three stages: water extraction, cloud-covered water-map reconstruction, and time series refinement.

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-1.png" alt="Workflow combining water extraction, cloud reconstruction, and spatiotemporal refinement" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1437" height="670" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">Fig. 1 from the paper. Workflow of the proposed seamless time series flood mapping method.</figcaption>
</figure>

### **3.1 Water extraction with a foundation model**
{: .h5}

The study further fine-tunes the pretrained Prithvi-100M–Sen1Floods11 model on the Sen1Floods11 dataset. Six HLS bands—blue, green, red, narrow near-infrared, and two shortwave-infrared bands—provide the input. The model produces an initial water/non-water map, while pixels affected by clouds and cloud shadows are marked as missing observations.

### **3.2 Adaptive reconstruction using water occurrence**
{: .h5}

Historical water occurrence records how frequently a location has been observed as water. The GSW occurrence data used in this study are derived from Landsat observations spanning 1984–2021.

Within an adaptive local window, clear pixels are grouped by historical water occurrence. For each group, the method calculates the proportion of clear pixels currently identified as water. The introduced **submaximal stability assumption** uses the generally increasing relationship between this ratio and historical occurrence to select a local reconstruction threshold. Ratios are less sensitive than raw pixel counts to changes in cloud cover and water extent.

A cloud-covered pixel is labeled as water if its historical occurrence exceeds the local threshold, and as non-water otherwise. This step reconstructs classification labels rather than optical reflectance values. The adaptive window helps accommodate spatial differences in water dynamics.

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-3.png" alt="Example of adaptive threshold selection and water-map reconstruction under clouds" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1420" height="712" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">Fig. 3 from the paper. Reconstruction of cloud-covered water classes using historical occurrence and local distribution statistics.</figcaption>
</figure>

### **3.3 Spatiotemporal refinement and flood delineation**
{: .h5}

A spatiotemporal Markov random field model uses nearby pixels and observations close in time to reduce inconsistencies in the reconstructed sequence. Reconstructed pixels receive lower weights than directly observed pixels to limit the influence of reconstruction errors. Water outside the maximum extent observed during the pre-flood reference period is then identified as floodwater. The sequence also supports maximum water extent maps and flood-duration indicators.

## **4. Results and analysis**
{: .h4}

### **4.1 Following floods through cloudy observations**
{: .h5}

The four-site experiments demonstrate how reconstruction fills spatial gaps in water maps across successive HLS acquisitions. The resulting sequence represents flood expansion and recession more completely than the original maps with missing cloud-covered regions.

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-5.png" alt="Initial and reconstructed water maps for successive flood observations at four sites" class="img-fluid" style="width:100%; max-width:760px; height:auto;" width="1250" height="1678" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">Fig. 5 from the paper. Time series reconstruction examples in India, Pakistan, Brazil, and the USA.</figcaption>
</figure>

### **4.2 Reconstruction accuracy**
{: .h5}

Simulation experiments apply cloud masks at different coverage levels to manually annotated reference water maps, creating controlled gaps in the water labels. The paper compares the proposed reconstruction method with the gap-filling method of Zhao and Gao (2018).

| Evaluation period | Benchmark mean F1 | Proposed mean F1 | Absolute F1 gain |
| --- | --- | --- | --- |
| During floods | 0.871 | 0.931 | 0.060 |
| Before/after floods | 0.772 | 0.903 | 0.131 |

These are mean F1-scores across the tested cloud-cover levels. They describe water-map reconstruction under simulated missing-observation conditions, rather than the overall accuracy of the full flood-monitoring workflow. Comparisons with 3 m PlanetScope imagery provide additional visual evidence. Differences in acquisition time and cloud cover prevent these comparisons from serving as strict pixel-level quantitative validation.

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-8.png" alt="Comparison of reconstructed flood maps with higher-resolution PlanetScope observations" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1334" height="1028" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">Fig. 8 from the paper. Reconstructed flood maps compared with independent PlanetScope images.</figcaption>
</figure>

### **4.3 Maximum extent and flood-duration indicators**
{: .h5}

Missing observations can propagate into estimates of maximum inundation and flood duration. Reconstructing the time series improves the spatial completeness and consistency of these derived products, helping identify flood-affected areas that would otherwise be omitted from the available observations.

The paper’s flood-duration maps use the frequency of inundation in the observation sequence as an indicator of persistence. They do not provide an hourly record of actual inundation duration; interpretation also depends on observation intervals and reconstruction errors.

<figure class="my-4 text-center">
  <img src="/assets/img/blogs/2024-seamless-flood-mapping/fig-9.png" alt="Maximum water extent and flood duration before and after time series reconstruction" class="img-fluid" style="width:100%; max-width:850px; height:auto;" width="1434" height="1175" loading="lazy" decoding="async" data-zoomable>
  <figcaption class="caption">Fig. 9 from the paper. Maximum water extent and flood-duration maps composed from original and reconstructed water-map sequences.</figcaption>
</figure>

## **5. Discussion and limitations**
{: .h4}

Performance depends on water extraction, cloud masks, and the availability of clear-sky information. Persistent, dense cloud cover increases uncertainty. Based on the paper’s simulation experiments, cloud cover below 96% was recommended to maintain a typical reconstruction F1-score above 0.8. This empirical condition applies to the tested scenarios and does not guarantee accuracy for other locations or flood events.

Historical occurrence can provide insufficient information about extreme floods extending beyond historically common inundation areas, potentially causing omissions of floodwater. Water obscured by vegetation, confusion between cloud shadows and water, and errors in initial cloud masks also affect the results. SAR observations offer complementary information, but differences between optical and SAR imaging mechanisms must be addressed when combining their water maps.

## **6. Conclusions**
{: .h4}

SeamlessFloodMapper combines foundation-model water extraction, adaptive occurrence-based reconstruction, and spatiotemporal refinement to improve flood monitoring with cloudy optical image time series. The four-site results demonstrate benefits for reconstruction accuracy, spatial completeness, and derived flood products. The released code and data support further evaluation and development of the approach.

## **Code and resources**
{: .h4}

- [Code](https://github.com/dr-lizhiwei/SeamlessFloodMapper)
- [Pretrained model and datasets](https://drive.google.com/drive/folders/1c57gKA1L6q0v36gaPfBn0a3XnN1cYjwF?usp=sharing)
- [Supplementary material]({{ '/assets/pdf/2024.10_ISPRS P&RS_Seamless flood mapping_Appendix A Supplementary data.pdf' | relative_url }})

<p class="mt-4 text-muted"><small>Please note: the content above was compiled and translated by AI based on the original paper.</small></p>
