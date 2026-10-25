# Project Notebook

[Open the RF and ANN notebook](Kodagu_RF_ANN_Landslide_Susceptibility.ipynb).

## Run instructions

1. Use ArcGIS Pro's Python environment with scikit-learn, NumPy, pandas, Matplotlib and joblib. The original notebook recorded scikit-learn 1.8.0.
2. Set `PROJECT_ROOT` to your local project directory.
3. Confirm the source geodatabase is `arcgis_files/Landslide/Landslide.gdb` beneath that directory, with `Kodagu_ML_TrainingData` and the listed predictor fields.
4. Restart the kernel and run cells from the beginning.
5. Initially keep `RUN_RASTER_MAPPING` and `RUN_EXISTING_MAP_ANALYSIS` false. Set them true and rerun from the beginning when their prerequisites are available. Spatial Analyst is required for these optional sections.

Outputs go to `Notebook_Repaired_Outputs`. Raw inputs are not included in this repository.

## Scope and verification

The uploaded working notebook had 13 saved error outputs. The first error used `reference_raster` before assignment; the absent `aligned_paths` setup then caused cascading failures. A replacement alignment block now defines `aligned_paths` and `final_paths`, prepares all 12 factors and checks their grids.

The original RF/ANN parameters and stratified split (70:30, seed 42) are retained. Output counts and errors were cleared, and the historical evaluation metrics were recorded separately in Markdown. The uploaded notebook directly documents **360 samples (181 landslide, 179 background), 252 training and 108 test records**.

Python cells compile. The restored setup, grid checks and NoData handling were exercised with small test doubles; real ArcPy geoprocessing and end-to-end execution on the original datasets have **not** been performed here.

The original deleted cell cannot be recovered exactly. The replacement is labelled accordingly, so regenerated raster results are not guaranteed to match the historical maps.

## Inputs requiring attention

- Mapping uses a raster named `kodaguannual_Rainfall`. Confirm it represents the same rainfall variable used for the training samples and reconcile its identity with the documented August–October 2018 period.
- The original low/moderate/high classification thresholds are absent. Existing three-class RF/ANN rasters and the corrected Combine raster are prerequisites for map-statistics/agreement sections.
- AHP construction and its ROC evaluation are not present in the uploaded code.
- Raster CRS must already match the DEM; the notebook stops on mismatches rather than choosing an unverified coordinate transformation.
