# Annual changes Bachelor's degree in Saudi Arabia
### EDA prpoject

## Project Discribtion:
The project is based on Exploratory Data Analysis (EDA), where i used (إحصائيات عامة - التعليم الجامعي,https://moe.gov.sa/ar/knowledgecenter/dataandstats/edustatdata/Pages/HigherEduStat.aspx ) dataseet from the minestry of Education.
The data includes 552,671 students distributed across 13 administrative regions, 24 educational institutions, and 11 fields of study.

## Dataset Sample
| السنة الدراسية | المرحلة الدراسية | المستوى الدراسي | نوع المؤسسة التعليمية | المنطقة الإدارية | نوع الجهة | الجهة التعليمية | المجال الواسع | المجال الضيق | المجال التفصيلي | نظام الدراسة | الجنس | الجنسية | العدد | حالة_الطالب |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2021 | بكالوريوس | بكالوريوس | الجامعات الحكومية | المنطقة الشرقية | جامعة | الجامعة السعودية الإلكترونية | الأعمال والإدارة والقانون | الأعمال والإدارة | التسويق والإعلان | انتظام | أنثى | سعودي | 181 | مستجد |
| 2021 | بكالوريوس | بكالوريوس | الجامعات الحكومية | المنطقة الشرقية | جامعة | الجامعة السعودية الإلكترونية | الأعمال والإدارة والقانون | الأعمال والإدارة | التسويق والإعلان | انتظام | أنثى | غير سعودي | 8 | مستجد |
| 2021 | بكالوريوس | بكالوريوس | الجامعات الحكومية | المنطقة الشرقية | جامعة | الجامعة السعودية الإلكترونية | الأعمال والإدارة والقانون | الأعمال والإدارة | التسويق والإعلان | انتظام | ذكر | سعودي | 131 | مستجد |

## Project Objective

Does the number of students change over the years?
To answer this question, several visualization figures were created to explore the data and reveal insights about key trends and patterns.

## Project Structure
```bash
project/
├── EDA/
│   └── EDA.ipynb                        # Exploratory Data Analysis notebook
├── csvfiles/
│   ├── sepCSVfiles/                     # Separated individual CSV files
│   ├── final_dataset_withEnrolled.csv   # Final dataset including enrolled students
│   ├── hes2021-2023.xlsx                # Raw HES data (2021–2023) 
│   └── main_dataset.csv                # Main combined dataset
├── dataCombination/
│   └── concatCSVs.py                   # Script to concatenate CSV files
├── webStyle/
│   ├── __pycache__/                    # Python cache (auto-generated)
│   └── style.py                        # Styling utilities for web output
└── main.py                             # Main entry point of the streamlit application
```
## Run the program

### Install the required libraries:

```bash
pip install -r requirements.txt
```
### Run the Streamlit program
```bash
streamlit run main.py
```

### Streamlit link
You can checkout the data analysis in this streamlit link: https://annualchangesbachelorstudents.streamlit.app/
