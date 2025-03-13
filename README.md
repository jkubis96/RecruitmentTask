# RecruitmentTask


## Machine Learning Classifier for Cell Line Identification  

### Overview  
This project focuses on developing a machine learning (ML) classifier to distinguish between three selected cell lines representing different organs. The classifier is trained on gene expression profiles from **Archs4** and validated against **DepMap** data.  

### Selected Cell Lines  
- **Brain** – IMR32  
- **Breast** – SKBR3  
- **Skin** – A431  

### Data Sources  
- **Archs4**: Expression profiles (limited to protein-coding genes).  
- **RefGen annotation file**: [Homo_sapiens.GRCh38.107] (corresponding to Archs4 data).  
- **DepMap**: Used for testing and validation.  

### Implementation  

##### 1. Data Acquisition  
- Downloaded Archs4 data for selected cell lines.  
- Retrieved the corresponding RefGen annotation file.  
- Collected DepMap expression profiles for testing.  

##### 2. Preprocessing & Feature Engineering  
- Cleaned and normalized **Archs4 data** (TPM-aligned with DepMap normalization).  
- Developed scripts for **feature selection** to identify key gene markers.  

##### 3. Model Development  
- Implemented an ML classifier with:  
  - **Imputation, scaling, and preprocessing** for prediction.  
  - **Train-test split, imputer creation, data scaling, and feature selection.**  
  - **Confusion matrix analysis and cross-validation** for performance evaluation.  

##### 4. Validation & Reporting  
- Performed **predictions on DepMap** data.  
- Generated reports summarizing classification results.  


### Full reports available [here](https://jkubis96.github.io/RecruitmentTask/)