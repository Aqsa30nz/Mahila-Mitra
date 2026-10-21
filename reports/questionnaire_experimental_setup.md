# Questionnaire Dataset: Experimental Setup and Current Implementation

## 1. Objective

The objective of this implementation stage is to prepare and understand the symptom-questionnaire data that will serve as one of the input modalities of the proposed Mahila-Mitra platform for PCOS/PCOD support.

This stage focuses on dataset inspection, benchmarking, data-quality assessment, conservative preprocessing, and validation of the processed dataset. It does not claim to provide a clinical diagnosis or a complete PCOS prediction system.

## 2. Dataset Description

- **Dataset name:** PCOS 2023 Dataset
- **Source:** Kaggle
- **Source URL:** https://www.kaggle.com/datasets/sahilkoli04/pcos2023
- **Original local dataset dimensions:** 465 rows × 16 columns
- **Processed dataset dimensions:** 464 rows × 16 columns
- **Number of exact duplicate rows removed:** 1
- **Missing values in the processed dataset:** 0

The dataset contains questionnaire responses relating to age, weight, height, menstrual patterns, reported symptoms, lifestyle habits, and self-reported PCOS/PCOD diagnosis.

The diagnosis field is treated as a questionnaire response. Its coded values are not independently interpreted as clinically confirmed diagnoses.

## 3. Experimental Environment and Tools

The current questionnaire-processing workflow uses:

- **Python:** Data-processing and analysis language.
- **Pandas:** Dataset loading, inspection, duplicate detection, preprocessing, and validation.
- **Jupyter Notebook:** Execution and documentation of the analysis workflow.
- **Matplotlib:** Exploratory data visualisations, where used in the notebook.
- **CSV files:** Storage of the original and processed questionnaire datasets.

The original dataset is retained separately from the processed output to preserve the source data.

## 4. Experimental Workflow

The implemented workflow consists of the following stages:

1. Load the original questionnaire CSV file.
2. Inspect dataset dimensions, column names, data types, and response distributions.
3. Examine missing values and exact duplicate records.
4. Review unusual values and potentially inconsistent response codes.
5. Standardise column headers by removing embedded line breaks and surrounding whitespace.
6. Remove one exact duplicate record.
7. Save the processed dataset as a separate CSV file.
8. Reload the saved file and validate its dimensions, duplicate count, and missing-value count.
9. Document benchmark results, data-quality observations, and unresolved limitations.

## 5. Benchmark Results

After the implemented preprocessing:

| Measurement | Observed result |
|---|---:|
| Original rows | 465 |
| Processed rows | 464 |
| Columns | 16 |
| Exact duplicate rows remaining | 0 |
| Missing values remaining | 0 |
| Records outside the paper's stated 18–45 age range | 41 |
| Height values below 100 | 4 |
| Period-duration entries coded as 0, 14, or 15 | 4 |

The processed dataset's self-reported diagnosis field contains 363 responses coded as 0 and 101 responses coded as 1.

Unusual values have been retained rather than automatically deleted or recoded because their intended meaning has not yet been verified against authoritative dataset documentation.

## 6. Preprocessing Decisions

The preprocessing stage applies conservative data-cleaning decisions:

- Exact duplicate removal.
- Column-header standardisation.
- Missing-value assessment.
- Identification and documentation of unusual values.
- Preservation of the original CSV.
- Separate storage and validation of the processed CSV.

No missing-value imputation or unsupported response-code conversion has been performed. Potentially unusual age, height, and period-duration values have not been removed solely because they appear atypical.

## 7. Alignment with the Project Synopsis

This implementation contributes to the data-preparation component of the Mahila-Mitra methodology, particularly the preparation of manually reported symptoms and lifestyle information and the identification of inconsistent or unusual questionnaire records.

The questionnaire dataset represents one input modality of the proposed platform. The current work establishes a preliminary data-processing pipeline that can support subsequent investigation of structured symptom data.

## 8. Limitations and Pending Verification

The research paper reports 465 entries and 15 variables for the questionnaire dataset, whereas the Kaggle file and the local CSV currently show 16 columns. The reason for this discrepancy has not been established. No column has been removed based on an assumption.

The meanings of all numeric response codes, the height-unit conventions, and the unusual period-duration values also require verification. The observed age range extends beyond the range stated in the paper; those records have been retained pending confirmation of the relevant inclusion criteria.

The current implementation covers questionnaire data only. It does not yet demonstrate ultrasound-image classification, medical-report NLP/NER processing, multimodal fusion, a retrieval-augmented generation (RAG) assistant, or a complete end-to-end platform.

## 9. Next Steps

1. Resolve dataset provenance and schema differences where authoritative documentation is available.
2. Verify response-code meanings and data-quality rules.
3. Evaluate and prepare an appropriate ultrasound dataset as a separate modality.
4. Develop and evaluate the additional components described in the project synopsis.
5. Integrate the components only when the required data, implementation, and evaluation are available.

## 10. Current Implementation Status

The questionnaire dataset has been inspected, benchmarked, conservatively preprocessed, and validated after saving. The current implementation represents an initial data-preparation milestone within the broader Mahila-Mitra research project; it does not imply that the complete proposed platform has been implemented.

## Alignment with the Mahila-Mitra Synopsis

This experiment supports the structured symptom-processing component described in Sections 5.2, 5.3 and 5.4 of the Mahila-Mitra methodology.

**Objective alignment**
- Objective 1: The broader literature and requirement analysis provides the research context for the platform.
- Objectives 2 and 3: The questionnaire preprocessing workflow prepares structured symptom-related data for subsequent analysis within the proposed platform.
- Objective 6: This milestone records data-quality checks and preprocessing validation. It does not constitute a complete evaluation of the proposed platform.

Objectives concerning multimodal integration, personalised guidance, RAG-based conversational assistance, privacy and safety mechanisms remain broader project objectives and are not claimed as completed by this experiment.

**Experimental setup**
1. Load the original questionnaire CSV.
2. Inspect dataset dimensions, column names, data types, missing values, duplicates, response frequencies and unusual values.
3. Standardise column headers without changing the original CSV.
4. Remove the one exact duplicate record.
5. Preserve undocumented response codes and unusual values instead of making unsupported assumptions.
6. Save the processed dataset separately.
7. Reload the saved CSV and verify its dimensions, missing-value count and duplicate count.

**Current outcome**
- Original dataset: 465 rows × 16 columns.
- Processed dataset: 464 rows × 16 columns.
- Missing values after preprocessing: 0.
- Exact duplicate records after preprocessing: 0.

**Scope and limitations**

This experiment covers questionnaire data only. Ultrasound-image processing, medical-report NLP/NER, multimodal fusion, RAG, personalised support, and complete system-level or user-oriented evaluation have not been demonstrated by this workflow. Further modelling and evaluation require appropriate validation of the dataset's labels, response coding, feature suitability and research limitations. The workflow does not establish clinical diagnostic performance.