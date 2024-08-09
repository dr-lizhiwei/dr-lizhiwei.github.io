---
layout: page
title: Research
permalink: /research/
description: 
nav: true
nav_order: 1
display_categories:
horizontal: false
---

##### **Grants**  

- **PI**: Near-Real-Time Flood Monitoring in Cloud-Prone Areas Incorporating Multi-Sensor Satellite Imagery,  The Hong Kong Polytechnic University, HKD 730,800, 02/2024-01/2026. (Terminated)&emsp;

- **PI**: Intelligent Reconstruction and Fusion of Multisource Remote Sensing Data for High-resolution Dynamic Land Use Mapping, The Hong Kong Polytechnic University, HKD 250,000, 09/2022-08/2024.  &emsp;

- **Co-I**: A GeoAI Framework for Urban Flood Hazard Monitoring, Risk Assessment, and Scenario-based Projection, The Hong Kong Polytechnic University, HKD 1,600,000, 06/2022-05/2024.

- **PI**: Thick Cloud Processing Methods for Time-series Remote Sensing Images in Tensor Space,  National Natural Science Foundation of China (NSFC), CNY 300,000, 01/2022-12/2024.  &emsp;


##### **Research Interests**  

My research primarily focuses on <u>Remote Sensing of Cloudy and Rainy Environments</u>, which involves applying big Earth data and geospatial artificial intelligence (GeoAI) for environmental research and applications, especially in cloudy and rainy tropical/subtropical regions. Current research topics include but are not limited to the following:

- Cloud Detection ([2017](https://zhiweili.net/assets/pdf/2017.3_RSE_Multi-feature%20combined%20cloud%20and%20cloud%20shadow%20detection%20in%20GaoFen-1%20wide%20field%20of%20view%20imagery.pdf); [2019](https://zhiweili.net/assets/pdf/2019.4_ISPRS%20P&RS_Deep%20learning%20based%20cloud%20detection%20for%20medium%20and%20high%20resolution%20remote%20sensing%20images%20of%20different%20sensors.pdf); [2022](https://zhiweili.net/assets/pdf/2022.6_ISPRS%20P&RS_Cloud%20and%20cloud%20shadow%20detection%20for%20optical%20satellite%20imagery%EF%BC%9AFeatures,%20algorithms,%20validation,%20and%20prospects.pdf)) and Removal ([2019](https://zhiweili.net/assets/pdf/2019.8_RS_Thick%20Cloud%20Removal%20in%20High-Resolution%20Satellite%20Images%20Using%20Stepwise%20Radiometric%20Adjustment%20and%20Residual%20Correction.pdf); [2021](https://zhiweili.net/assets/pdf/2021.7_ISPRS%20P&RS_Combined%20deep%20prior%20with%20low-rank%20tensor%20SVD%20for%20thick%20cloud%20removal%20in%20multitemporal%20images.pdf); [2024](https://zhiweili.net/assets/pdf/2024.10_ISPRS%20P&RS_Beyond%20clouds%EF%BC%9ASeamless%20flood%20mapping%20using%20Harmonized%20Landsat%20and%20Sentinel-2%20time%20series%20imagery%20and%20water%20occurrence%20data.pdf))

- Land Use & Land Cover Mapping ([2021](https://zhiweili.net/assets/pdf/2021.12_JAG_Time%20series%20remote%20sensing%20image%20classification%20framework%20using%20combination%20of%20deep%20learning%20and%20multiple%20classifiers%20system.pdf); [2024](https://zhiweili.net/assets/pdf/2024.7_RSE_Learning%20spectral-indices-fused%20deep%20models%20for%20time-series%20land%20use%20and%20land%20cover%20mapping%20in%20cloud-prone%20areas.pdf))

- Flood Monitoring and Risk Assessment ([2024](https://zhiweili.net/assets/pdf/2024.10_ISPRS%20P&RS_Beyond%20clouds%EF%BC%9ASeamless%20flood%20mapping%20using%20Harmonized%20Landsat%20and%20Sentinel-2%20time%20series%20imagery%20and%20water%20occurrence%20data.pdf); [2024](https://www.taylorfrancis.com/chapters/edit/10.1201/9781003244561-4/urban-flooding-monitoring-management-geospatial-perspective-zhiwei-li-cheolhee-yoo-qihao-weng); [2024](https://zhiweili.net/assets/pdf/Conference%20Papers/2024_IGARSS_Can%20we%20reconstruct%20cloud-covered%20flooding%20areas%20in%20harmonized%20Landsat%20and%20Sentinel-2%20image%20time%20series.pdf))

- Geospatial Artificial Intelligence (GeoAI) ([2019](https://zhiweili.net/assets/pdf/2019.4_ISPRS%20P&RS_Deep%20learning%20based%20cloud%20detection%20for%20medium%20and%20high%20resolution%20remote%20sensing%20images%20of%20different%20sensors.pdf); [2020](https://zhiweili.net/assets/pdf/2020.5_RSE_Deep%20learning%20in%20environmental%20remote%20sensing%EF%BC%9AAchievements%20and%20challenges.pdf); [2024](https://zhiweili.net/assets/pdf/2024.7_RSE_Learning%20spectral-indices-fused%20deep%20models%20for%20time-series%20land%20use%20and%20land%20cover%20mapping%20in%20cloud-prone%20areas.pdf))


<div class="slideshow-container">
    <div class="mySlides">
        <img src="../assets/img/research_cloud.jpg" alt="Image 1">
    </div>
    <div class="mySlides">
        <img src="../assets/img/research_lulc.jpg" alt="Image 2">
    </div>
    <div class="mySlides">
        <img src="../assets/img/research_flood.jpg" alt="Image 3">
    </div>
    <div class="mySlides">
        <img src="../assets/img/research_GeoAI.jpg" alt="Image 4">
    </div>
    <!-- Add more slides as needed -->
</div>

<script>
    let slideIndex = 0;
    let slides = document.getElementsByClassName("mySlides");
    let totalSlides = slides.length;

    function showSlides() {
        for (let i = 0; i < totalSlides; i++) {
            slides[i].style.display = "none";
        }
        slideIndex++;
        if (slideIndex > totalSlides) {
            slideIndex = 1; // Restart from the first slide
        }
        slides[slideIndex - 1].style.display = "block";
        setTimeout(showSlides, 3000); // Change image every 3 seconds
    }
    
    showSlides();
</script>

<style>
    .slideshow-container * { box-sizing: border-box; }
    .slideshow-container {
        font-family: Arial, sans-serif; 
        margin: 0px auto;
        max-width: 960px; 
        position: relative; 
        background: #ffffff; /* Set background to white */
        overflow: hidden;
    }
    .slideshow-container .mySlides { 
        display: none; 
        text-align: center; /* Center the images */
    }
    .slideshow-container img {
        vertical-align: middle; /* middle */
        width: 100%;
        height: auto
        max-width: 960px;
        object-fit: cover;
    }
</style>



[//]: # "<html lang="en">"

[//]: # "<head>"

[//]: # "    <meta charset="UTF-8">"

[//]: # "    <meta name="viewport" content="width=device-width, initial-scale=1.0">"

[//]: # "    <title>Embedded Google Slides Slideshow</title>"

[//]: # "</head>"

[//]: # "<body>"

[//]: # "    <div>"

[//]: # "        <iframe src="https://docs.google.com/presentation/d/e/2PACX-1v.../embed?start=true&loop=true&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>"

[//]: # "    </div>"

[//]: # "</body>"

[//]: # "</html>"






[//]: # "- Cloud Detection &#40;[Li et al., 2017, RSE]&#40;https://zhiweili.net/assets/pdf/2017.3_RSE_Multi-feature%20combined%20cloud%20and%20cloud%20shadow%20detection%20in%20GaoFen-1%20wide%20field%20of%20view%20imagery.pdf&#41;; [Li et al., 2019, ISPRS P&RS]&#40;https://zhiweili.net/assets/pdf/2019.4_ISPRS%20P&RS_Deep%20learning%20based%20cloud%20detection%20for%20medium%20and%20high%20resolution%20remote%20sensing%20images%20of%20different%20sensors.pdf&#41;; [Li et al., 2022, ISPRS P&RS]&#40;https://zhiweili.net/assets/pdf/2022.6_ISPRS%20P&RS_Cloud%20and%20cloud%20shadow%20detection%20for%20optical%20satellite%20imagery%EF%BC%9AFeatures,%20algorithms,%20validation,%20and%20prospects.pdf&#41;&#41;"

[//]: # "- Cloud Removal &#40;[Li et al., 2019, RS]&#40;https://zhiweili.net/assets/pdf/2019.8_RS_Thick%20Cloud%20Removal%20in%20High-Resolution%20Satellite%20Images%20Using%20Stepwise%20Radiometric%20Adjustment%20and%20Residual%20Correction.pdf&#41;; [Zhang et al., 2021, ISPRS P&RS]&#40;https://zhiweili.net/assets/pdf/2021.7_ISPRS%20P&RS_Combined%20deep%20prior%20with%20low-rank%20tensor%20SVD%20for%20thick%20cloud%20removal%20in%20multitemporal%20images.pdf&#41;; [Li et al., 2024, ISPRS P&RS]&#40;https://zhiweili.net/assets/pdf/2024.10_ISPRS%20P&RS_Beyond%20clouds%EF%BC%9ASeamless%20flood%20mapping%20using%20Harmonized%20Landsat%20and%20Sentinel-2%20time%20series%20imagery%20and%20water%20occurrence%20data.pdf&#41;&#41;"

[//]: # "- Land Use & Land Cover Mapping &#40;[Li et al., 2024, RSE]&#40;https://zhiweili.net/assets/pdf/2024.7_RSE_Learning%20spectral-indices-fused%20deep%20models%20for%20time-series%20land%20use%20and%20land%20cover%20mapping%20in%20cloud-prone%20areas.pdf&#41;; [Dou et al., 2021, JAG]&#40;https://zhiweili.net/assets/pdf/2021.12_JAG_Time%20series%20remote%20sensing%20image%20classification%20framework%20using%20combination%20of%20deep%20learning%20and%20multiple%20classifiers%20system.pdf&#41;&#41;"

[//]: # "- Flood Monitoring and Risk Assessment &#40;[Li et al., 2024, ISPRS P&RS]&#40;https://zhiweili.net/assets/pdf/2024.10_ISPRS%20P&RS_Beyond%20clouds%EF%BC%9ASeamless%20flood%20mapping%20using%20Harmonized%20Landsat%20and%20Sentinel-2%20time%20series%20imagery%20and%20water%20occurrence%20data.pdf&#41;; [Li et al., 2024]&#40;https://www.taylorfrancis.com/chapters/edit/10.1201/9781003244561-4/urban-flooding-monitoring-management-geospatial-perspective-zhiwei-li-cheolhee-yoo-qihao-weng&#41;; [Li et al., 2024, IGARSS]&#40;https://zhiweili.net/assets/pdf/Conference%20Papers/2024_IGARSS_Can%20we%20reconstruct%20cloud-covered%20flooding%20areas%20in%20harmonized%20Landsat%20and%20Sentinel-2%20image%20time%20series.pdf&#41;&#41;"

[//]: # "- Geospatial Artificial Intelligence &#40;GeoAI&#41; &#40;[Li et al., 2019, ISPRS P&RS]&#40;https://zhiweili.net/assets/pdf/2019.4_ISPRS%20P&RS_Deep%20learning%20based%20cloud%20detection%20for%20medium%20and%20high%20resolution%20remote%20sensing%20images%20of%20different%20sensors.pdf&#41;; [Yuan et al., 2020, RSE]&#40;https://zhiweili.net/assets/pdf/2020.5_RSE_Deep%20learning%20in%20environmental%20remote%20sensing%EF%BC%9AAchievements%20and%20challenges.pdf&#41;; [Li et al., 2024, RSE]&#40;https://zhiweili.net/assets/pdf/2024.7_RSE_Learning%20spectral-indices-fused%20deep%20models%20for%20time-series%20land%20use%20and%20land%20cover%20mapping%20in%20cloud-prone%20areas.pdf&#41;&#41;"
