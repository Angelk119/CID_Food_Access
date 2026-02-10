
---

# Beyond the Pantry

## Where Need Meets Supply: Emergency Food Access in NYC Neighborhoods

---

## Overview

This project examines food insecurity among children living in New York City family homeless shelters by comparing neighborhood food insecurity prioritization, shelter population concentration, and the availability of emergency food assistance sites.
The goal is to identify whether neighborhoods with the highest shelter-related need are adequately supported with emergency food resources and to provide data-informed recommendations for equitable food access planning.

---

## Critical Research Question

How does the availability of emergency food assistance sites across Neighborhood Tabulation Areas (NTAs) compare for neighborhoods located within community districts with higher shelter population concentrations and higher food insecurity prioritization?

---

## Actionable Recommendations

### Policy

Coordinate planning between the NYC Department of Homeless Services and the Mayor’s Office of Food Policy so emergency food resources expand proportionally in neighborhoods with the highest shelter-related food insecurity.

### Resource Allocation

Increase sustained funding and operational support for nonprofit emergency food providers in neighborhoods with high shelter populations but limited food site density.

### Data & Technology

Develop a neighborhood-level integrated data system linking shelter populations, food insecurity metrics, and food site capacity to guide equitable long-term planning.

---

## Stakeholders

NYC Department of Homeless Services
Mayor’s Office of Food Policy
Children and families living in NYC shelters

---

## Data Sources

DHS Shelter Census & community district shelter datasets – provide shelter population trends and geographic concentration.
Emergency Food Assistance Program (EFAP) – provides locations and characteristics of emergency food sites.
Neighborhood Food Insecurity Prioritization dataset – measures neighborhood-level food insecurity and vulnerability.

---

## Methodology

### Geographic aggregation at the Neighborhood Tabulation Area (NTA) level

All spatial analyses are conducted at the NTA level to ensure consistency across datasets and to enable neighborhood-level comparisons of food access and shelter-related needs.

### Construction of a coverage ratio to quantify food access relative to need

A coverage ratio is calculated using counts of individuals in shelter systems as a proxy for food insecurity needs, allowing food assistance availability to be evaluated relative to population demand.

### Statistical testing of differences across priority and non-priority areas

Mean difference tests and proportional comparisons are used to assess whether food coverage differs significantly between high-need and lower-need neighborhoods before modeling.

### Logistic regression for neighborhood-level classification

Coverage ratio is binned into categorical outcomes (for example, high vs low coverage), and logistic regression is used to identify neighborhood characteristics associated with inadequate food access.

### Exploratory time-series analysis using ARIMAX

ARIMAX models are explored to examine trends in shelter population demand over time, with results interpreted cautiously and model assumptions explicitly tested and documented.

---

## Tech Stack

Python: Pandas, Scikit-learn, Streamlit
SQL: SQLite
Visualization: Tableau

---

## Key Findings

Food assistance resources are unevenly distributed relative to neighborhoods with the highest concentration of family shelters.

Children in shelter-dense neighborhoods face compounded barriers such as distance, limited hours, and transportation challenges when accessing food.

Data integration and predictive analysis reveal priority zones where targeted investment would most effectively reduce food insecurity risk.

---

## Ethics & Equity

This project centers children and families experiencing homelessness, recognizing that institutional datasets often reflect system-level perspectives rather than lived experience.
Findings are framed to avoid harm, prevent misinterpretation, and support equitable policy decisions rather than surveillance or deficit narratives.
Shelter data are not available at the individual shelter-site or exact neighborhood location level, we cannot make causal claims about how specific food programs affect shelter residents.

---

## Links to Final Deliverables

Interactive Tableau Dashboard: [WIP]

Local Streamlit Application: [WIP]

Technical Report (PDF):
[Link to deliverables/Deliverable_Report.pdf]

---

## Repository Navigation

sql/data_processing.sql — Star Schema construction and ETL

python/notebooks/eda.ipynb — Visual EDA and statistical analysis

python/src/model_training.py — Final model code and evaluation

ai_process.md — Documentation on ethical AI usage

---

## Data Source Attribution

We acknowledge and appreciate the work of the New York City Open Data program and associated municipal agencies in making these datasets publicly available for civic research and analysis.

---

## Contributors and Roles

- **Angel Bautista — Project Manager** | [LinkedIn](https://www.linkedin.com/in/angelgbautista/)
- **Ayema Qureshi — Analytics Engineer / Data Modeler** | [LinkedIn](https://www.linkedin.com/in/ayemaqureshi/)
- **Ibrahima Diallo — Data Engineer / ETL Lead** | [LinkedIn](https://www.linkedin.com/in/ibranova/)

---

## APA References

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

If you'd like, I can next **add badges, a table of contents, or GitHub preview styling** to make it look more professional.


