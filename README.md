# Beyond the Pantry
- NYC Food Coverage Predictor (Neighborhood Tabulation Area (NTA)-level)
- Identifying where Emergency Food Assistance Program (EFAP) supply does not scale with structural vulnerability across NYC neighborhoods.

## Key Takeaway
- In 2024, EFAP site coverage is not evenly aligned with structural vulnerability across NYC Neighborhood Tabulation Areas (NTAs). Among high-priority NTAs (top 25% by structural vulnerability), **56%** fall below the city median coverage, and **16%** have zero EFAP sites. Statistical testing also shows that coverage differs meaningfully between high-priority and other NTAs (p = 0.001167), supporting the conclusion that misalignment is real, not noise.


## Critical Research Question
- To what extent does Emergency Food Assistance Program (EFAP) site distribution align with structural vulnerability across NYC Neighborhood Tabulation Areas (NTAs), and can neighborhood structural and service characteristics predict low coverage areas to support targeted resource planning?


### Why this matters
- Food insecurity is not just about hunger. It is shaped by structural conditions like unemployment, household vulnerability, and where families are already under pressure. EFAP is one of NYC’s emergency food supports, so if EFAP supply does not scale with vulnerability, the neighborhoods with the highest need can be systematically under-served.

### Data sources (2024 focus)
- This project integrates multiple NYC civic datasets at the NTA level.
  - NYC Neighborhood Prioritization / vulnerability indicators (structural vulnerability inputs)
  - EFAP site locations and service attributes (food supply)
  - Shelter context indicators (used as added context and in the model as an “extended feature”)
  - NTA geography (for mapping and joins)
- DHS Shelter Census & community district shelter datasets – provide shelter population trends and geographic concentration.
- Emergency Food Assistance Program (EFAP) – provides locations and characteristics of emergency food sites.
- Neighborhood Food Insecurity Prioritization dataset – measures neighborhood-level food insecurity and vulnerability.

### Key Terminology

- **Neighborhood Tabulation Area (NTA):** NYC-defined neighborhood geography used for planning and reporting. Each record represents one NTA.
- **Structural Vulnerability:** Underlying socioeconomic conditions that increase a neighborhood’s risk of hardship, including food insecurity.
  - In this project, measured using the **Weighted Score**.
  - Higher structural vulnerability indicates deeper, systemic barriers to stable food access.
- **Weighted Score (Structural Vulnerability):** Composite measure combining food insecurity and related socioeconomic risk factors (see data dictionary).
  - Higher _Weighted Score_ = higher structural vulnerability.
- **High-Priority NTA:** Top 25% of neighborhoods ranked by Weighted Score.
  - Ranking-based definition, not manually assigned.
- **Coverage Ratio:** “Supply relative to pressure” metric.
  - Coverage Ratio = Total EFAP Sites ÷ Food Insecurity Percentage
  - Not a perfect measure of service capacity, but a consistent way to compare whether supply scales with need.
- **Why we use medians (quadrant logic):**
  - Median thresholds divide NTAs into clear, comparable zones.
  - Prevents extreme values from distorting interpretation.
  - Supports the alignment scatterplot and under-served “action” view in the dashboard.

### Analytical approach
- We answer the CRQ in two parts:
  - _Alignment analysis_ (dashboard): Compare structural vulnerability (Weighted Score) vs EFAP coverage (Coverage Ratio) and identify mismatch zones.
  - _Predictive modeling_ (Model): Predict whether an NTA is likely to be a low coverage area using structural + service context features.

#### Methodology
- Data Engineering & Integration
  - This project integrates multiple datasets operating at different geographic levels and grains. EFAP program-level data (561 sites) were aggregated to the Neighborhood Tabulation Area (NTA) level using ZIP-to-NTA mapping. Neighborhood Prioritization data (197 NTAs) served as the primary need indicator through its composite Weighted_score, which captures food insecurity, unemployment, and supply gap. Shelter population and infrastructure datasets, reported at the community district (CDTA) level, were mapped to NTAs using the CDTA2020 crosswalk to provide contextual shelter concentration.
  - All datasets were aligned to the NTA level to ensure consistent neighborhood-level comparison.

 ---
 
## Exploratory Data Analysis (EDA)
- Before formal testing or modeling, we conducted structured exploratory analysis at the neighborhood level. Key steps:
  - Aggregated 561 EFAP sites to 197 NTAs
  - Created a coverage_ratio (sites relative to neighborhood need)
  - Classified NTAs into High vs. Lower priority using the top quartile of Weighted_score
- **EDA Findings**
  - High-priority NTAs had lower average coverage ratios despite higher measured need
  - Structural vulnerability outpaces food site distribution across NYC, especially in Queens and Brooklyn.
    - <img width="400" alt="Screenshot" src="https://github.com/user-attachments/assets/d7b1063a-1719-4497-882e-230150ef6677" />
  - Site counts were highly skewed, with several high-priority NTAs having 0–2 sites
  - Kitchen-equipped sites were unevenly distributed
    - <img width="400" alt="EDA Screenshot" src="https://github.com/user-attachments/assets/c39942d7-28da-4cb0-949a-962d7ec68d65" />

These patterns indicated a measurable misalignment between structural vulnerability and food site distribution, motivating formal statistical testing and predictive modeling.

---

### Statistical Analysis (What We Tested and Found)
- **Hypothesis**
  - H0 (null): EFAP coverage is the same for high-priority and non-high-priority NTAs.
  - H1 (alternative): EFAP coverage differs between high-priority and non-high-priority NTAs.
- **Variables**
  - Grouping: High Priority vs. Not High Priority
  - Outcome: Coverage Ratio
- **Test Used: Welch’s t-test**
  - Coverage Ratio was not normally distributed and group variances were unequal.
  - Welch’s t-test accounts for unequal variances.
  - p-value = 0.001167 → statistically significant difference.
- **Effect Size**
  - Cohen’s d = 0.3526
  - Indicates a small-to-moderate practical difference.
- **Interpretation**
  - High-priority neighborhoods are more likely to have lower coverage.
  - Coverage gaps are systematic, supporting the finding that supply does not reliably scale with vulnerability.


---

## Dashboard (Tableau) story
🔗 Tableau Public Dashboard (CID Food Access – Dashboard): https://public.tableau.com/views/CID-foodaccess/Dashboard2
- The dashboard is designed as a narrative:
  - Need (Structural Vulnerability): Map visualizes food insecurity pressure across NTAs.
  - Supply (EFAP Distribution): Bar chart shows where EFAP sites are concentrated.
  - Alignment vs. Misalignment (4-Zone View): Scatterplot splits NTAs by
    - X-axis: Structural Vulnerability
    - Y-axis: Coverage Ratio
    - Zones identify:
      - Aligned (high need + high coverage)
      - Under-Served (high need + low coverage)
      - Over-Served (low need + high coverage)
      - Lower Priority (low need + low coverage)
  - Action View: Ranked list of high-priority NTAs by lowest coverage to support targeted intervention.

### KPI Definitions
- **KPI 1: % of High-Priority NTAs Under-Served**
  - Measures how many structurally vulnerable neighborhoods fall below the city median coverage.
  - Result: 56% of high-priority NTAs are below median coverage.
- **KPI 2: Average Coverage in High-Priority NTAs**
  - Measures overall average coverage within the high-priority group.
  - Averages may appear stable even if many NTAs fall below the median, indicating uneven distribution within the group.
- **KPI 3: % of High-Priority NTAs with Zero EFAP Sites**
  - Measures how many vulnerable neighborhoods have no EFAP presence.
  - Result: 16% of high-priority NTAs have zero sites.
- **Why Use the Median**
  - The median represents a “typical neighborhood” benchmark.
  - It prevents outliers from distorting results and supports a clear under-served classification.


## Predictive Model: Identifying Low Food Coverage Neighborhoods
To move beyond descriptive analysis, we built a logistic regression model to predict whether an NTA has low EFAP coverage.
- **Predictors (5):** food insecurity rate, unemployment rate, high shelter population flag, soup kitchen presence, weekend availability  
- **Regularization:** L2 applied for stability and interpretability  
- **Data:** 197 NTAs (50 held out for testing)
### Performance
- Accuracy: 86%  
- F1 Score: ~0.86  
- Recall (low coverage): 92%  
  - The model correctly identified 92% of under-served neighborhoods.
  - 43 of 50 test NTAs were classified correctly.
### Key Findings
- Higher food insecurity increases the likelihood of low coverage.
- Operational infrastructure (soup kitchens, weekend access) strongly predicts higher coverage.
- Coverage gaps are not random; they are systematically associated with structural and service factors.

The model reinforces the dashboard findings: structural vulnerability alone does not guarantee adequate food site distribution.

---


### Streamlit app (model demo)
- The Streamlit app is a simple “neighborhood profile” to show model output in a decision-friendly way: Users input neighborhood indicators (food insecurity rate, unemployment, shelter context, service availability).
- The app returns a predicted coverage risk label (example: “LOW COVERAGE”) and a confidence score.
- This turns analysis into a usable tool for discussion.

## Actionable Recommendations
- **Prioritize zero-coverage high-priority NTAs**
  - High-vulnerability neighborhoods with 0 EFAP sites signal the most urgent gaps.
- **Target expansion in the under-served zone**
  - Focus on NTAs with high vulnerability + low coverage for new partnerships and site placement.
- **Expand weekend availability**
  - Weekend access is a meaningful predictor of coverage and can improve access without adding new sites.
- **Align planning with shelter pressure areas**
  - Monitor EFAP coverage closely where shelter concentration is high.
- **Strengthen coverage measurement**
  - Move beyond site counts to include capacity, hours, eligibility, and accessibility where possible.
- **Monitor alignment over time**
  - Use `coverage_ratio` and `weighted_score` to track whether infrastructure scales with vulnerability.



### Limitations
- **Coverage Ratio measures site count, not service capacity.**
  - Calculated as EFAP sites relative to neighborhood-level need proxies.
  - Does not account for site capacity, daily volume, staffing, or demand intensity.
  - Equal site counts may reflect very different operational realities.
- **EFAP data reflects registered sites, not real-time availability.**
  - Captures listed locations and characteristics.
  - Does not guarantee daily operation, inventory sufficiency, or absence of temporary closures.
- **Need is measured using composite structural indicators.**
  - Represented by `weighted_score`, combining food insecurity, unemployment, and supply gap metrics.
  - Useful for comparison, but remains a proxy for individual hardship.
- **Shelter data is aggregated at the community district level.**
  - Mapped to NTAs via CDTA2020 crosswalk.
  - Shelter concentration is contextual, not precise neighborhood-level exposure.
- **Findings reflect correlation, not causation.**
  - Statistical tests and modeling identify relationships between vulnerability and coverage.
  - Cross-sectional design does not establish causal effects.

---

### Tech Stack
- Python: Pandas, Scikit-learn, Streamlit
- SQL: SQLite
- Visualization: Tableau


## Ethics & Equity

This analysis examines neighborhood-level patterns, not individual families. Shelter and food access data are aggregated and mapped to NTAs using geographic crosswalks. Because we rely on proxies and do not observe individual outcomes, findings are descriptive and correlational, not causal.

Structural vulnerability and food insecurity scores are used as contextual indicators of need, not direct measures of lived experience. The presence of a food site does not guarantee adequate access.

Our goal is to evaluate whether resource placement aligns with measured need, not to rank or assign blame to communities. Transparency about data limitations ensures the analysis supports informed policy discussion without overstating conclusions.

---

## Links to Final Deliverables
- Interactive Tableau Dashboard: [https://public.tableau.com/app/profile/ayema.qureshi/viz/CID-foodaccess/Dashboard2?publish=yes] 
- Local Streamlit Application: https://beyondthepantry.streamlit.app
- Schema: [https://lucid.app/lucidchart/bfb16d31-5bda-4eee-92ad-83c0d3d41102/edit?viewport_loc=-2043%2C253%2C2995%2C1708%2C0_0&invitationId=inv_5e1df819-e856-440f-b2ce-1720ed73a113] 

---

## Repository Navigation

```
CID_Food_Access/
├─ data/
│  ├─ clean/
│  │  ├─ dim_map.csv
│  │  ├─ efap_cleaned.csv
│  │  ├─ efap_nta_mapping.csv
│  │  ├─ prioritization_clean.csv
│  │  ├─ shelter_census_clean.csv
│  │  ├─ shelter_qr_TimeSeries.csv
│  │  └─ unified_dataset_for_modeling.csv
│  └─ raw/
│     ├─ Individual_Census.csv
│     ├─ Neighborhood_Prioritization_Map.csv
│     ├─ efap_raw.csv
│     ├─ nta2020_raw.csv
│     └─ .DS_Store
│
├─ deliverables/
│  ├─ Deliverable_Report.pdf
│  └─ Stakeholder_Presentation.pptx
│
├─ deployment/
│  ├─ app.py
│  ├─ coverage_model.pkl
│  ├─ model_metadata.json
│  ├─ scaler.pkl
│  └─ requirements.txt
│
├─ python/
│  └─ notebooks/
│     ├─ data_processing/
│     │  ├─ efap_clean.ipynb
│     │  ├─ nta2020_clean.ipynb
│     │  ├─ prioritization_clean.ipynb
│     │  └─ shelter_census_clean.ipynb
│     ├─ eda/
│     │  ├─ statistics.ipynb
│     │  ├─ tableau_data_prep.ipynb
│     │  └─ unified_eda.ipynb
│     └─ modeling/
│        └─ models.ipynb
│
├─ src/
│  ├─ create_schema.py
│  └─ create_schema2.py
│
├─ sql/
│  └─ data_processing.sql
│
├─ food_access.db
├─ README.md
├─ ai_process.md
└─ .gitignore
```

---

### Data Source Attribution

We acknowledge and appreciate the work of the New York City Open Data program and associated municipal agencies in making these datasets publicly available for civic research and analysis.

---

### Contributors and Roles

- **Angel Bautista — Project Manager** | [LinkedIn](https://www.linkedin.com/in/angelgbautista/)
   - Contributed to policy interpretation and executive messaging
   - Coordinated cross-functional workflow and milestone tracking
 
  
- **Ayema Qureshi — Analytics Engineer / Data Modeler** | [LinkedIn](https://www.linkedin.com/in/ayemaqureshi/)
  - Defined critical research question (CRQ), project scope, and analytical framing aligned with DHS and food policy stakeholders
  - Designed and implemented star schema architecture, including fact tables, dimension tables, and bridge logic to align EFAP, prioritization, and shelter datasets at the NTA level
  - Engineered program level features and aggregated program-level service indicators (kitchen access, weekend availability)
  - Led exploratory data analysis (EFAP + structural vulnerability indicators), identifying distributional patterns and misalignment between need and supply
  - Built Tableau dashboard to operationalize alignment framework, including KPI logic, quadrant segmentation, and stakeholder-ready visual narratives
  - Co-developed statistical methodology and modeling documentation, translating EDA findings into formal testable hypotheses
  - Translated technical outputs into executive-facing insights, framing results around system alignment rather than neighborhood deficit
 
  
- **Ibrahima Diallo — Data Engineer / ETL Lead** | [LinkedIn](https://www.linkedin.com/in/ibranova/)
  - Built ETL pipelines and data processing scripts, including feature engineering for modeling datasets and alignment of neighborhood-level inputs
  - Led statistical modeling implementation, developing and comparing Logistic Regression models (Model 1 vs Model 2), applying L2 regularization, and selecting the final extended feature model
  - Implemented statistical tests (independent t-tests, Spearman correlation) to validate group differences prior to modeling
  - Engineered preprocessing pipeline, including feature scaling and model serialization (scaler.pkl, coverage_model.pkl, model_metadata.json) for reproducible deployment
  - Conducted model evaluation and validation, reporting Accuracy, Precision, Recall, F1 Score, and confusion matrix performance with threshold tuning
  - Developed and deployed Streamlit prediction application, integrating model artifacts and building interactive performance and feature impact views
  - Co-developed technical documentation and presentation materials, translating modeling insights into stakeholder-facing explanations 

--- 

### APA References

Coalition for the Homeless. (n.d.). Why are so many people homeless?
Davis, A. Y. (2003). Are prisons obsolete? Seven Stories Press.
Feeding America. (n.d.). What is food insecurity?
Gundersen, C., & Ziliak, J. P. (2018). Food insecurity research in the United States: Where we have been and where we need to go. *Applied Economic Perspectives and Policy, 40*(1), 119–135.
Institute for Children, Poverty, and Homelessness. (n.d.-a). Federal SNAP changes threaten stability for NYC families in shelters.
Institute for Children, Poverty, and Homelessness. (n.d.-b). Family homelessness 101: New York City – Impact on children.
Mayor’s Office of Food Policy. (n.d.-a). About the Mayor’s Office of Food Policy.
Mayor’s Office of Food Policy. (n.d.-b). Food Forward NYC.
New York State Office of the Comptroller. (2023). Federal actions threaten to exacerbate rising food insecurity.
NY1. (2024, May 29). Child hunger rates continue to rise in New York City.
U.S. Department of Agriculture Economic Research Service. (n.d.). Definitions of food security.

---


