# Questionnaire Dataset Benchmark

## Dataset overview

- Source: PCOS 2023 Dataset (Kaggle)
- Original shape: 465 rows x 16 columns
- Cleaned shape: 464 rows x 16 columns
- Exact duplicate rows removed: 1
- Missing values in cleaned dataset: 0

## Diagnosis distribution

Have you been diagnosed with PCOS/PCOD?
0    363
1    101

## Data quality observations

- Observed age range: 13–58 years
- Records outside the paper's stated 18–45 age range: 41
- Height values below 100: 4
- Period-duration values coded 0, 14, or 15:
  4

## Outstanding issue

The original questionnaire CSV contains 465 records and 16 columns. The processed dataset contains 464 records and 16 columns after removal of one exact duplicate record. The diagnosis-response column is retained as the target candidate, leaving 15 other columns that may serve as input features, subject to further validation.

The research paper's reported count of 15 variables may refer to the input features rather than all CSV columns, but this interpretation has not been independently confirmed.

The dataset contains undocumented response codes and unusual values, including ambiguous height entries and period-duration values. These values have been retained rather than interpreted, converted, or removed without an authoritative codebook. The dataset's self-reported diagnosis responses must not be treated as independently clinically verified diagnoses.

No machine-learning model has been trained or evaluated as part of this preprocessing milestone. Results reported by third-party notebooks are not results of the Mahila-Mitra implementation.
