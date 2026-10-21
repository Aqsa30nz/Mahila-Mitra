# Mahila-Mitra: Questionnaire Dataset Processing Pipeline

## 1. Objective

The objective of this task is to inspect, document, and prepare the PCOS symptom questionnaire dataset for further analysis in the Mahila-Mitra project. This work focuses only on the questionnaire dataset and does not include ultrasound-image processing or merging with a clinical dataset.

## 2. Dataset Source and File

- **Dataset file:** `CLEAN- PCOS SURVEY SPREADSHEET.csv`
- **Original file location:** `data/raw/questionnaire/`
- **Processed file location:** `data/processed/questionnaire_cleaned.csv`
- **Format:** CSV
- **Original dimensions:** 465 rows and 16 columns
- **Processed dimensions:** 464 rows and 16 columns

The original CSV is retained unchanged. The processed dataset is saved separately so that the original data remains available for comparison and reproducibility.

## 3. Variables Observed

The dataset contains demographic information, menstrual-health responses, lifestyle-related responses, symptoms, and a self-reported PCOS/PCOD diagnosis field.

The observed variables include:

- Age
- Weight
- Height
- Blood-group response code
- Menstrual interval response
- Recent weight gain
- Excessive body or facial hair growth
- Recent skin darkening
- Hair loss, hair thinning, or baldness
- Pimples or acne
- Regular fast-food consumption
- Regular exercise
- Self-reported PCOS/PCOD diagnosis
- Mood swings
- Menstrual regularity
- Period duration

The meanings of numeric response codes must be confirmed against the original questionnaire or its documentation before interpreting them as specific answers.

## 4. Initial Data Inspection

The dataset was inspected using Python and pandas. The following checks were performed:

- Dataset dimensions and column names
- Data types
- First five records
- Missing values in each column
- Exact duplicate rows
- Unique-value counts and response frequencies
- Potentially unusual values in age, height, and period duration

The initial dataset contained 465 rows and 16 columns. No missing values were detected by pandas. One exact duplicate pair was identified, involving two identical records.

## 5. Cleaning and Standardization

### 5.1 Column headers

Carriage-return and newline characters were removed from column headers, and surrounding whitespace was trimmed. This standardizes header formatting without changing the underlying response values.

### 5.2 Duplicate records

One copy of the exact duplicate record was removed from the processed dataset. The number of rows decreased from 465 to 464.

After this operation, the processed dataset contained zero exact duplicate rows.

### 5.3 Missing values

No missing values were detected in the original dataset. Therefore, no missing-value imputation or deletion was performed.

### 5.4 Unusual values and response coding

Some values require further verification:

- The observed ages range from 13 to 58, which does not match the reported age range of 18–45 associated with the dataset description.
- Four height entries are below 100, and the column header mentions centimetres or feet. Their units and intended interpretation are unclear.
- Four period-duration entries are coded as 0, 14, or 15 days. These values were flagged for review rather than automatically changed or removed.
- Blood-group responses are represented by numeric codes, but their mapping to blood groups has not been confirmed.
- Several symptom, lifestyle, and diagnosis variables contain 0/1 values. Their exact meanings should be verified before assigning labels such as Yes and No.

These values have been preserved in the processed dataset because there is not yet sufficient verified evidence to correct them safely.

## 6. Exploratory Data Analysis

The Jupyter notebook `notebooks/questionnaire_eda.ipynb` contains the initial inspection and exploratory analysis.

The notebook includes:

- Dataset dimensions and data types
- Missing-value and duplicate checks
- Unique-value counts and response frequencies
- Inspection of potentially unusual age, height, and period-duration entries
- A bar chart of recorded hair-loss response codes
- A missing-values chart
- A bar chart of recorded PCOS/PCOD diagnosis response codes

The diagnosis field contains 363 records coded 0 and 102 records coded 1. These are recorded numeric codes; their interpretation should be confirmed using the dataset's original coding documentation.

The charts are saved under `outputs/questionnaire/`.

## 7. Processing Decisions

The following decisions were applied:

1. Preserve the original CSV unchanged.
2. Standardize column-header formatting.
3. Remove one copy of the exact duplicate record.
4. Retain all other response values.
5. Avoid unverified conversions of numeric response codes.
6. Avoid deleting unusual values without a confirmed rule.
7. Save the processed CSV separately from the raw dataset.

The processed file is intended for further inspection and analysis. It should not be treated as fully validated until the dataset's coding scheme and eligibility criteria have been confirmed.

## 8. Relationship to the Research Paper

The selected research paper is:

*Predicting polycystic ovary syndrome using statistical data integration and machine learning with low-cost information* (2026).

The paper and its dataset description must be checked against the original publication and dataset documentation before claiming exact reproduction of its preprocessing pipeline.

The work documented here establishes an initial inspection and conservative duplicate-removal procedure. It does not claim to reproduce every paper-specific preprocessing, statistical matching, feature-selection, or machine-learning step. The questionnaire dataset has not been merged with any clinical dataset in this task.

## 9. Limitations and Pending Verification

- Confirm the exact source and version of the downloaded CSV.
- Verify the discrepancy between the reported and observed age ranges.
- Confirm height units and blood-group coding.
- Verify the meanings of binary response codes.
- Investigate unusual period-duration entries using the original questionnaire or source documentation.
- Compare the paper's stated preprocessing steps with the actual dataset before claiming full reproduction.
- Do not use the self-reported diagnosis field as a clinically validated diagnosis.
- Do not use the current dataset to make medical decisions.

## 10. Output Files

| File | Purpose |
|---|---|
| `data/raw/questionnaire/CLEAN- PCOS SURVEY SPREADSHEET.csv` | Preserved original dataset |
| `data/processed/questionnaire_cleaned.csv` | Dataset after column-header standardization and exact-duplicate removal |
| `notebooks/questionnaire_eda.ipynb` | Initial inspection and exploratory analysis |
| `reports/questionnaire_data_dictionary.csv` | Variable definitions, observed values, types, and coding uncertainties |
| `outputs/questionnaire/` | Generated exploratory charts |

## 11. Conclusion

The questionnaire dataset has been loaded, inspected, and prepared through a conservative initial cleaning process. One exact duplicate record was removed, resulting in 464 rows and 16 columns, with no missing values or remaining exact duplicate rows. Uncertain response coding and unusual values have been preserved for verification rather than silently modified. Further validation against the original questionnaire and research publication is required before advanced analysis or claims of exact reproduction.
