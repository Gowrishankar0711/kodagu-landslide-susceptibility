# Landslide Susceptibility Mapping Using GIS and Machine Learning
## Kodagu District, Karnataka, India

A geospatial project integrating **Analytical Hierarchy Process (AHP), Random Forest (RF), and Artificial Neural Network (ANN)** to map landslide susceptibility in Kodagu district. The study combines 12 conditioning factors, inventory-based evaluation, and spatial agreement analysis to compare the three approaches.

**Key results:** RF test ROC–AUC of **0.9702**, ANN test ROC–AUC of **0.9012**, and approximately **122 km²** classified as high susceptibility by all three models.

## Project Objectives

- Prepare and integrate terrain, hydrological, geological, land-use, and infrastructure-related conditioning factors.
- Develop an AHP-based susceptibility model and machine learning models.
- Evaluate model discrimination using ROC–AUC.
- Produce low, moderate, and high susceptibility maps.
- Compare spatial agreement and identify areas consistently classified as highly susceptible.

## Study Area

The study covers **Kodagu district in Karnataka, India**, within the Western Ghats. 

Susceptibility represents the relative spatial tendency for landslides to occur. It does not provide a forecast of when a landslide will happen.

## Conditioning Factors

| No. | Factor | Representation |
| --- | --- | --- |
| 1 | Elevation | Digital Elevation Model (DEM) |
| 2 | Slope | DEM-derived slope |
| 3 | Aspect | DEM-derived slope orientation |
| 4 | Curvature | DEM-derived terrain curvature |
| 5 | Rainfall | CHIRPS rainfall data |
| 6 | Distance to roads | Euclidean distance raster |
| 7 | Distance to rivers | Euclidean distance raster |
| 8 | Topographic Wetness Index (TWI) | Terrain-based wetness index |
| 9 | Lithology | Geological classes |
| 10 | Distance to lineaments | Euclidean distance raster |
| 11 | Geomorphology | Geomorphological classes |
| 12 | Land Use/Land Cover (LULC) | Land-cover classes |

NDVI, NDWI, and NDBI were explored during preliminary analysis and excluded from the final factor set following multicollinearity assessment.

## Methodology

### 1. Data Preparation

- Prepared and clipped input layers to the study area.
- Derived terrain factors from the DEM.
- Calculated distances to roads, rivers, and lineaments.
- Resampled and aligned raster layers using the processed DEM as the reference grid.
- Prepared lithology, geomorphology, and LULC layers for raster analysis.
- Reclassified the 12 factors for AHP-based modelling.

Resampling rainfall to the analysis grid aligns the inputs; it does not increase the spatial detail of the original rainfall data.

### 2. Multicollinearity Assessment

Variance Inflation Factor (VIF) analysis was performed in Python using **473 sampled records**.

Preliminary VIF values were high for NDVI (**137.270**), NDWI (**75.555**), and NDBI (**20.354**). After removing these indices, the eight continuous predictors evaluated in the subsequent analysis had VIF values of approximately **1.02–2.04**.

This VIF result applies to those eight continuous predictors, rather than constituting a VIF assessment of all 12 final factors.

### 3. AHP-Based Susceptibility Mapping

- Used pairwise comparisons to assign relative weights to conditioning factors.
- Integrated reclassified factors through an AHP-weighted overlay.
- Prepared a continuous Landslide Susceptibility Index (LSI) for ROC evaluation.
- Presented the susceptibility output as low, moderate, and high classes.

### 4. Machine Learning Sample Preparation

- Used the 2018 landslide inventory as positive samples.
- Prepared background samples outside a **500 m buffer** around known landslide points.
- Extracted conditioning-factor values to sample points.
- Checked the extracted dataset for unexpected missing and NoData values.
- Used a **70:30 training–testing split** for RF and ANN modelling.

Background samples represent locations treated as non-landslide samples for modelling; they are not confirmed permanently stable locations.

### 5. Random Forest and ANN Modelling

Trained Random Forest and ANN models in Python, evaluated their discrimination on the test data using ROC–AUC, and generated susceptibility maps with low, moderate, and high classes.

### 6. Spatial Agreement Analysis

Compared the classified AHP, RF, and ANN maps cell by cell to identify:

- Cells where all three models assigned the same class.
- Cells where exactly two models agreed.
- Cells where all three assigned different classes.
- Cells classified as high susceptibility by all three models.

## Results

### ROC–AUC

| Method | ROC–AUC | Evaluation basis |
| --- | --- | --- |
| AHP | 0.8514 | Continuous LSI evaluated using 181 landslide and 179 background points |
| Random Forest | 0.9702 | Test subset from the 70:30 split |
| ANN | 0.9012 | Test subset from the 70:30 split |

RF achieved the higher test ROC–AUC of the two machine learning models in this experiment. The AHP score uses a different evaluation setup and should not be interpreted as a strictly equivalent held-out comparison.

ROC–AUC measures discrimination between the sampled landslide and background locations; **it is not classification accuracy**.

### Agreement Between Classified Maps

| Agreement category | Cell count | Percentage |
| --- | ---: | ---: |
| All three models agree | 1,282,509 | 29.44% |
| Exactly two models agree | 2,923,045 | 67.11% |
| All three models disagree | 150,127 | 3.45% |

The intersection of the three high-susceptibility classes contains **130,022 cells**, covering approximately **122 km²**, or **2.99% of the analysed area**.

Agreement indicates consistency between models; it does not independently establish ground-truth accuracy.

## Tools and Technologies

- **ArcGIS Pro and Spatial Analyst:** raster and vector processing, terrain analysis, distance analysis, reclassification, overlay, and map layouts.
- **Python and ArcPy:** GIS automation and extraction of sample attributes.
- **NumPy and pandas:** tabular data preparation and analysis.
- **scikit-learn:** machine learning and evaluation.
- **Matplotlib:** evaluation plots.
- **joblib:** model persistence.

## Detailed Results and Comparison Charts

See the [results report](Results/README.md) for model metrics, confusion matrices, susceptibility class tables, four comparison charts, map interpretations and high-susceptibility consensus analysis. Machine-readable CSV tables and the chart-generation script are included in [Results/](Results/).
