# Research Paper Summary: PCOS Symptom Questionnaire Dataset

## 1. Research Paper

**Title:** Predicting polycystic ovary syndrome using statistical data integration and machine learning with low-cost information

**Publication:** *Neural Computing and Applications*, 2026.

**Link:** https://link.springer.com/article/10.1007/s00521-026-12211-y

## 2. What Is the PCOS 2023 Questionnaire Dataset?

The PCOS 2023 Dataset is a publicly available questionnaire dataset hosted on Kaggle. It contains responses collected through an online Google Forms questionnaire about PCOS-related symptoms and menstrual characteristics. The dataset provides demographic, lifestyle and symptom-related information that can be explored using statistical analysis and machine-learning methods.

## 3. Number of Entries and Variables

The research paper reports 465 entries and 15 variables for the PCOS 2023 Dataset. The CSV file inspected for this project contains 465 rows and 16 columns. This difference in the reported number of variables needs further investigation and will be documented as a dataset-version or schema discrepancy until its cause is established.

## 4. Data Collection and Recorded Information

According to the paper, the questionnaire responses were collected online from women aged 18–45. The variables primarily represent binary or ordinal responses related to menstrual patterns and symptoms associated with hyperandrogenism.

The downloaded CSV includes questions about age, weight, height, blood group, menstrual frequency, recent weight gain, excessive body or facial hair, skin darkening, hair loss, acne, fast-food consumption, physical activity, reported PCOS/PCOD diagnosis, mood swings, menstrual regularity and period duration.

## 5. Variables Shared with the Clinical Dataset

The paper describes two tabular datasets: a clinical PCOS dataset containing 541 records and the PCOS 2023 questionnaire dataset containing 465 records. The authors harmonized their schemas and selected 14 variables shared between the datasets for the data-integration experiment.

The shared information includes demographic, lifestyle, menstrual, symptom-related and PCOS-diagnosis variables. The datasets were not automatically linked patient by patient; statistical matching was used to investigate integration across the two sources.

## 6. Column Names and Response Standardization

The authors report harmonizing column names and retaining shared features to make the two datasets comparable. They state that the PCOS 2023 questionnaire dataset required no further adjustments in their preprocessing procedure.

The paper does not provide a detailed list of every original questionnaire column name and its replacement name in the preprocessing description. Therefore, the exact mapping used for the questionnaire dataset must not be invented. The present project will document its own column-name standardization and response mappings separately.

## 7. Records or Values Removed or Corrected

The paper reports removing null characters and invalid values from the clinical dataset. It also recoded the clinical dataset's Regular Menstruation variable from 2 (regular) and 4 (irregular) to 1 and 0, respectively. One record with an unexpected value of 5 for this variable was discarded, and one record with a missing value for Regular Fast Food Consumption was removed. The limited-feature subset of infertile patients was also excluded.

These corrections were reported for the clinical dataset, not the PCOS 2023 questionnaire dataset. The authors state that the questionnaire dataset required no further adjustments. The present project will independently inspect its downloaded CSV before deciding whether any additional cleaning is necessary.

## 8. Analyses and Machine-Learning Methods

The paper investigates statistical matching and machine-learning approaches for integrating the two PCOS-related datasets. Its workflow includes data preparation, exploratory analysis, statistical assessment of shared variables, data integration and classification.

The authors examine correlations between variables and PCOS labels, compare different integration configurations and evaluate classification performance using metrics such as accuracy, precision, recall and F1-score. They also investigate feature selection, hyperparameter optimization and uncertainty-based rejection of predictions.

For the questionnaire dataset, the paper reports 363 records labelled 0 and 102 labelled 1 for the PCOS diagnosis variable. These are the paper's reported results and will be kept separate from the findings generated in this project.

## 9. Limitations of Self-Reported Questionnaire Data

Questionnaire responses reflect information reported by participants and may be affected by recall errors, misunderstanding of questions, inconsistent response coding and data-entry mistakes. The dataset description and reported age range may also differ from the records in a particular downloaded version.

The presence of a self-reported PCOS/PCOD diagnosis label does not independently establish a clinically confirmed diagnosis. A questionnaire dataset of this kind should therefore be described according to its actual source and limitations. Its findings should not be treated as proof of disease or as a replacement for professional medical assessment.

## Reference

Maranhão, G. B. de A., Freitas, W. W. L., de Miranda, B. A., Lins, C. S., et al. (2026). *Predicting polycystic ovary syndrome using statistical data integration and machine learning with low-cost information*. Neural Computing and Applications.

https://doi.org/10.1007/s00521-026-12211-y
