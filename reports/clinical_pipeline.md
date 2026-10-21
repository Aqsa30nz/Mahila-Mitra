# Mahila-Mitra: Clinical Dataset EDA Report

## 1. Objective
This report documents exploratory data analysis of the clinical/tabular
PCOS dataset for the proposed Mahila-Mitra platform. The analysis is
exploratory and does not establish clinical diagnostic performance.

## 2. Dataset Overview
- Source file: PCOS_data_without_infertility.xlsx
- Worksheet: Full_new
- Number of records: 541
- Columns after removing identifiers and an irrelevant mostly empty column: 42
- Target: PCOS (Y/N)
- Target value 0: 364 records (67.3%)
- Target value 1: 177 records (32.7%)

Patient identifiers and the serial-number field were excluded from the
cleaned dataset. The original dataset and processed CSV should remain local
and should not be committed to the public repository.

## 3. Data Cleaning
The AMH(ng/mL) column was converted to numeric values. Invalid entries
were coerced to missing values. The target column was checked to ensure
that its values are binary (0 and 1).

After cleaning, three missing cells remained:
- Marraige Status (Yrs): 1
- AMH(ng/mL): 1
- Fast food (Y/N): 1

These missing values should be handled within a training pipeline where
imputation parameters are learned from training data only.

## 4. Exploratory Analysis
The notebook generates the following visualizations:
- PCOS class distribution
- Missing-value analysis
- Age distribution
- BMI distribution
- Age and BMI comparisons by PCOS status
- Categorical feature comparisons
- Numerical correlation heatmap

The plots describe the available sample. Any apparent differences or
correlations should be interpreted cautiously and are not evidence of
causation or proof of clinical usefulness.

## 5. Class Balance
The dataset contains more PCOS-negative than PCOS-positive records:
67.3% versus 32.7%. Model evaluation should therefore report metrics
beyond accuracy, including precision, recall/sensitivity and F1-score.
Any split should preserve class proportions where appropriate.

## 6. Limitations
- The dataset contains 541 records and may not represent all populations.
- Missing values and data quality issues require transparent handling.
- Correlations do not establish causation.
- Performance on this dataset alone would not establish clinical validity.
- Any future evaluation must prevent data leakage and fit preprocessing
  steps only on training data.

## 7. Next Steps
1. Review feature names, types and category encodings.
2. Confirm which columns are appropriate predictors and exclude identifiers.
3. Create a reproducible train/test split.
4. Fit imputation, encoding and scaling within a training-only pipeline.
5. Compare baseline models using multiple evaluation metrics.
6. Document limitations and avoid presenting the model as a medical diagnosis.

## 8. Figures
Figures are saved locally under outputs/clinical/. They are generated
by the clinical_eda.ipynb notebook and should be checked before being
referenced in a final report.

## Permutation Feature Importance

Permutation importance was evaluated on the held-out test set using ROC-AUC as the scoring metric. Each feature was shuffled 10 times to estimate its effect on model performance.

The right ovarian follicle count (Follicle No. (R)) had the highest mean permutation importance (0.0830, standard deviation 0.0226). Other features with positive mean importance included LH (mIU/mL), weight gain, hair growth, and left ovarian follicle count.

The results suggest that the model's predictions rely particularly strongly on right ovarian follicle count. However, the importance values are model-specific and do not establish causal relationships or independent diagnostic value. Several features showed variability across permutations, and correlated predictors may affect their individual importance rankings.

These findings are exploratory because the dataset is relatively small and the evaluation uses a single held-out test set. External validation on independent data would be required before drawing conclusions about real-world clinical performance.
