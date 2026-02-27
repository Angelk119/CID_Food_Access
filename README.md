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

### Key terminology 
- **Neighborhood Tabulation Area (NTA):** A NYC-defined neighborhood geography used for reporting and planning. Each record in our analysis represents one NTA.
- **Structural vulnerability:** refers to the underlying socioeconomic conditions that make a neighborhood more likely to experience hardship, including food insecurity. In this project, it is measured by the Weighted Score, which combines food insecurity rates with broader risk factors like unemployment and family-related pressures to reflect overall systemic disadvantage.
  - Higher structural vulnerability means a neighborhood faces deeper, more persistent barriers to stable food access.
- **Weighted Score (Structural Vulnerability):** Weighted Score is a composite measure of structural vulnerability, combining food insecurity and broader socioeconomic risk factors (as defined in our project data dictionary).
  - Higher _Weighted Score_ means the neighborhood ranks as more structurally vulnerable.
- **High-Priority NTA:** the top 25% of neighborhoods ranked by Weighted Score.
  - This is a ranking-based definition, not a label we assign manually.
- **Coverage Ratio**: our “supply relative to pressure” metric:
  - Coverage Ratio = Total EFAP Sites ÷ Food Insecurity Percentage
  - It is not a perfect measure of service capacity, but it is a consistent way to compare whether EFAP site presence scales with food insecurity pressure.
- Why we use medians (and quadrant logic)
  - We use median thresholds to divide neighborhoods into clear visual zones without letting a few extreme values dominate the story. Medians allow a clean “above typical vs below typical” comparison across NTAs, which is why we use them in the alignment scatterplot and in the under-served “action” view (Referring to the Dashboard)


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
- Before statistical testing or modeling, we conducted structured exploratory analysis at both the neighborhood and program levels. At the neighborhood level, we:
  - Aggregated 561 EFAP sites to 197 NTAs
  - Calculated `coverage_ratio` = `number_of_food_sites ÷ neighborhood_need_proxy`
  - Binned neighborhoods into High vs Lower structural vulnerability using the top quartile of Weighted_score
### EDA Takeaway
- Neighborhoods in the top quartile of structural vulnerability had, on average, lower coverage ratios than lower-priority neighborhoods, despite representing higher measured need. Additionally:
  - A disproportionate share of high-priority NTAs fell into the low-coverage category
  - Site counts were highly skewed, with several high-priority NTAs having 0–2 sites
  - Kitchen-equipped sites were unevenly distributed, meaning equal site counts did not imply equal service capacity
    - This early finding suggested a measurable misalignment between structural vulnerability and emergency food site distribution, which motivated formal statistical testing and classification modeling.

---

### Statistical analysis (what we tested and what we found)
- **Hypothesis**:
  - H0 (null): EFAP coverage is the same for high-priority and non-high-priority NTAs.
  - H1 (alternative): EFAP coverage differs between high-priority and non-high-priority NTAs.
- **Variables**
  - Grouping: High Priority vs Not High Priority
  - Outcome: Coverage Ratio

##### Why we used Welch’s t-test**
- We checked assumptions and found: Coverage Ratio is not normally distributed and roup variances are not equal. So we used Welch’s t-test, which is designed for unequal variances. The Welch’s t-test p-value = `0.001167`
  - This is statistically significant, meaning the observed difference is unlikely to be random.
  - Effect size: Cohen’s d = `0.3526`
    - This suggests a small-to-moderate practical difference. The effect is not just “statistically significant”, it is meaningful enough to care about in planning decisions.
- **Interpretation:** Coverage gaps are not evenly spread. High-priority neighborhoods are more likely to have worse coverage patterns, supporting the dashboard story that supply does not reliably scale with vulnerability.



---

## Dashboard (Tableau) story
🔗 Tableau Public Dashboard (CID Food Access – Dashboard): https://public.tableau.com/views/CID-foodaccess/Dashboard2
- The dashboard is designed as a narrative:
  1. Pressure (structural vulnerability context)
     - Map shows how food insecurity pressure varies across NTAs.
  2. Supply distribution (EFAP presence)
     - Bar chart shows how EFAP sites are distributed across NTAs.
     - With a borough filter, it shows where EFAP supply is concentrated within that borough.
  3. Alignment vs misalignment (4-zone view)
     - We split the city into four zones using medians of:
       - `X-axis`: structural vulnerability (Weighted Score or priority score used for need)
       - `Y-axis`: Coverage Ratio
       - Zones:
         - **Aligned**: higher vulnerability + higher coverage
         - **Under-Served**: higher vulnerability + lower coverage
         - **Over-Served**: lower vulnerability + higher coverage
         - **Lower Priority**: lower vulnerability + lower coverage
  4. Action view (zoom into the under-served zone)
     - A ranked list of high-priority NTAs ordered by Coverage Ratio from lowest upward.
     - This is meant to answer: “Where should decision makers act first?”
     - _Why there are 0s in the action chart_: A 0% coverage value means an NTA has zero EFAP sites in the EFAP dataset, so the Coverage Ratio becomes zero. Those NTAs represent the most severe supply gaps because there is no EFAP presence at all.

### KPI definitions 
- **KPI 1: “% of high-priority NTAs under-served”**
  - This tells us: Out of the neighborhoods that are most structurally vulnerable, how many have below-typical EFAP coverage?
  - In our results, 56% of high-priority NTAs are below the city median coverage.
 
- **KPI 2: “Average coverage in high-priority NTAs”**
  - This tells us: On average, what does coverage look like across high-priority NTAs?
  - This can feel like it “contradicts” KPI 1 because averages can be pulled up by a smaller number of better-covered neighborhoods, while KPI 1 is counting how many fall below a typical benchmark (the median). Both can be true at once:
    - The average might look OK, while most high-priority areas are still below the median, meaning coverage is unevenly distributed inside the high-priority group.

- **KPI 3: “% of high-priority NTAs with zero EFAP sites”**
  - This tells us: How many of the most vulnerable neighborhoods have no EFAP sites at all?
  - In our results, 16% of high-priority NTAs have zero EFAP sites.
  - City median coverage matters in this context because the median is the “middle neighborhood” benchmark. Half of NTAs are above it and half are below it. We use it to avoid extreme outliers and to make the “under-served vs not under-served” classification clear and defensible.




## Predictive Model: Identifying Low Food Coverage Neighborhoods
- To move beyond descriptive analysis, we built a logistic regression model to predict whether a Neighborhood Tabulation Area (NTA) has low or high Emergency Food Assistance Program (EFAP) coverage. The final model (Version 2.0) uses **five predictors**: food insecurity rate, unemployment rate, high shelter population flag, soup kitchen presence, and weekend availability
  - L2 regularization was applied to stabilize coefficients while preserving interpretability, making the model suitable for policy-facing decision contexts.
- The model was trained on 197 NYC NTAs, with 50 held out for testing. On the test set, it achieved 86% accuracy and an F1 score of approximately 0.86. Most importantly for equity planning, the model correctly identified 92% of low coverage neighborhoods (`recall_low` = 0.92) 
  - This high recall minimizes the risk of overlooking under-served areas. The confusion matrix shows that out of 50 test NTAs, 43 were classified correctly, with only 7 total misclassifications 
- Feature effects align with our alignment analysis. Higher food insecurity increases the likelihood of low coverage, reinforcing the core finding that structural vulnerability does not automatically translate into adequate food site distribution. In contrast, unemployment, shelter concentration, soup kitchen presence, and weekend availability are associated with higher coverage. Notably, operational characteristics such as soup kitchens and weekend hours emerge as the strongest positive predictors of coverage, suggesting that program infrastructure plays a critical role in mitigating vulnerability.
- Overall, the model demonstrates that structural and service characteristics meaningfully predict coverage outcomes. While some targeting mechanisms appear to exist, persistent misalignment remains, particularly in neighborhoods where food insecurity is high but site infrastructure is limited. The model strengthens the dashboard findings by showing that coverage gaps are not random; they are systematically associated with measurable structural factors.

---


### Streamlit app (model demo)
- The Streamlit app is a simple “neighborhood profile” to show model output in a decision-friendly way: Users input neighborhood indicators (food insecurity rate, unemployment, shelter context, service availability).
- The app returns a predicted coverage risk label (example: “LOW COVERAGE”) and a confidence score.
- This turns analysis into a usable tool for discussion.


### Actionable recommendations (based on findings)
- These are practical moves aligned with the dashboard “under-served zone” logic:
  - Prioritize zero-coverage high-priority NTAs first.
    - Any high-priority neighborhood with 0 EFAP sites represents the strongest signal of a supply gap.
  - Target expansion using the under-served zone
    - Use the “high vulnerability + low coverage” quadrant as the shortlist for new EFAP partnerships and site placement.
  - Improve weekend availability where risk is high
    - The model includes weekend service as a meaningful factor. Expanding weekend hours can increase real access even when adding new sites is slow.
  - Coordinate EFAP planning with shelter pressure areas
    - Shelter concentration is contextual but important. Where shelter pressure is high, EFAP access should be monitored more closely to prevent compounding vulnerability.
  - Strengthen measurement beyond site counts
    - Site count is a starting point. If data becomes available, expand coverage measurement to include capacity, hours, eligibility, language access, and distance to sites.
  - Implement a real-time dashboard using coverage_ratio and weighted_score to monitor whether emergency food infrastructure is proportionally meeting neighborhood vulnerability.




### Limitations
- **Coverage Ratio measures site count, not service capacity**.
  - The coverage_ratio is calculated using the number of EFAP sites relative to neighborhood-level need proxies. It does not account for site capacity, daily volume served, staffing levels, or demand intensity. Two neighborhoods with the same number of sites may have very different operational realities.

- **EFAP data reflects registered sites, not real-time availability.**
  - The EFAP dataset captures listed program locations and service characteristics but does not guarantee consistent daily operation, inventory sufficiency, or absence of temporary closures.

- **Need is measured using composite structural indicators.**
  - Structural vulnerability is represented through the `weighted_score`, which combines food insecurity, unemployment, and supply gap metrics. While useful for neighborhood comparison, it remains a proxy and does not directly measure individual-level food hardship.

- **Shelter population data is aggregated at the community district level.**
  - Shelter counts are mapped to NTAs using CDTA2020. Because shelter data is not available at the exact neighborhood or site level, shelter concentration is treated as contextual rather than precise neighborhood-level exposure.

- **The analysis supports correlation, not causation.**
  - While statistical tests and logistic regression identify meaningful relationships between structural vulnerability and coverage outcomes, the cross-sectional design does not establish causal effects between food site placement and food insecurity.


---

### Tech Stack
- Python: Pandas, Scikit-learn, Streamlit
- SQL: SQLite
- Visualization: Tableau


## Ethics & Equity

This analysis focuses on neighborhood-level patterns, not individual families. All shelter data are aggregated at the community district level and mapped to Neighborhood Tabulation Areas (NTAs) using a geographic crosswalk. Because we do not observe individual shelter locations or individual-level food access outcomes, this project does not make causal claims about how specific emergency food programs affect shelter residents. Shelter concentration and food insecurity prioritization scores are used as contextual indicators, not direct measures of individual need.

Power shows up in how data are structured and reported. City agencies and institutions determine what gets measured and published, while families living in shelters are represented only through aggregated counts. As a result, this analysis reflects system-level patterns rather than lived experience. We explicitly acknowledge that the presence of a food site in a neighborhood does not guarantee consistent or sufficient access.

To reduce the risk of misinterpretation, findings are framed around alignment between structural vulnerability and emergency food site distribution. High-priority labels describe composite indicators of food insecurity, unemployment, and supply gap, not the performance or behavior of a neighborhood. The goal is to evaluate whether resource placement aligns with measured need, not to assign blame or rank communities.

Because the data operate at different geographic levels and rely on proxies, conclusions are limited to descriptive and correlational insights. This transparency ensures the analysis supports informed policy discussion without overstating what the data can prove.

---

## Links to Final Deliverables
- Interactive Tableau Dashboard: [https://public.tableau.com/app/profile/ayema.qureshi/viz/CID-foodaccess/Dashboard2?publish=yes] 
- Local Streamlit Application: [WIP]
- Technical Report (PDF):[Link to deliverables/Deliverable_Report.pdf]
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


