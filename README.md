# Crypto Price Tracker
### Author: Virendrasinh Chavda

<p align="justify">
This repository contains the code for a real-time cryptocurrency tracking web app developed using Dash and Plotly. The app displays live candlestick charts, technical indicators like RSI and MACD, and a heatmap for visualizing price changes across various cryptocurrency pairs. Users can select the desired cryptocurrency, time frame, data span, and technical indicator to analyze market trends and make informed trading decisions. The app deployed on GCP can be viewed here (https://crypto-tracker-live.nw.r.appspot.com/).
</p>

## Table of Contents
1. [Overview](#Overview)
2. [Data](#Data)
3. [Methodology](#Methodology)
4. [Results](#Results)
5. [Future Work](#Future-Work)
6. [Contributing](#Contributing)
7. [License](#License)

## Overview
<p align="justify">
Money laundering is a sophisticated financial crime where illicit funds are disguised as legitimate. Traditional rule-based detection methods struggle with evolving and complex laundering schemes. In this project, we use **network analysis** techniques to detect money laundering by identifying central and suspicious nodes (accounts) in transaction networks. Centrality measures like **degree**, **closeness**, and **betweenness centrality** help uncover significant nodes. Additionally, community detection algorithms such as the **Girvan-Newman algorithm** are employed to isolate suspicious clusters of accounts.
</p>

<p align="justify">
Marketing campaigns are integral to driving customer engagement and conversions. In this project, we analyze A/B testing data to determine if different campaign strategies; Ad vs. PSA, significantly impact conversion rates. Using statistical tests, we assess if campaign type and ad frequency correlate with higher conversions and measure the practical impact of these factors on conversion likelihood. 
</p>

## Data:
<p align="justify">
The dataset used for this project includes anonymized user data on ad exposure and conversion outcomes, with the following key attributes:
</p>

* **test group**: Indicates the campaign type (`ad` or `psa`)
* **converted**: Binary variable indicating conversion (True/False)
* **total ads**: Number of ads shown to each user
* **most ads day**: Day of the week with the highest ad exposure
* **most ads hour**: Hour of the day with the highest ad exposure

<p align="justify">
For the purposes of this project, a subset of 2000 transactions was sampled and used for analysis due to computational constraints. Columns related to transaction type, timestamp, and fraud labels were excluded, focusing on **network properties**.
</p>

## Methodology:
### 1. Preprocessing
<p align="justify">
The dataset was cleaned by removing irrelevant columns and focusing on metrics essential for A/B testing, such as `test group`, `converted`, `total ads`, `most ads day`, and `most ads hour`.
</p>

### 2. Statistical Testing
<p align="justify">
The following statistical tests were conducted: 

* **Chi-Square Test**: To compare conversion rates between `ad` and `psa` groups.
* **Point-Biserial Correlation**: To measure the association between `total ads` and conversion.
* **Linear Regression**: To estimate the effect of `total ads` on conversion probability.
* **Effect Size Calculation (Cohen’s d)**: To determine the practical significance of ad exposure differences between groups.
</p>

### 3. Visualization
<p align="justify">
Visualizations included: 

* **Conversion Rate by Day and Hour**: Stacked bar plots for weekly and hourly conversion trends.
* **Conversion vs. Total Ads**: Scatter and box plots to visualize ad exposure differences by conversion status.
</p>

## Results:
<p align="justify">
* **Conversion Differences**: The Chi-Square test indicated significant conversion differences between the `ad` and `psa` groups. 
* **Ad Frequency Impact**: A positive correlation between `total ads` and conversion probability was found, with regression results showing a small but significant increase in conversion with ad frequency.
* **Effect Size**: Cohen’s d showed an extremely small practical effect, indicating that while statistically significant, the difference in ad exposure is practically minimal. 
</p>

## Future Work:
<p align="justify">
* **Incorporate Additional Features**: Adding data on user demographics and behavior could refine insights.
* **Longitudinal Analysis**: Analyzing conversion trends over time may reveal seasonality or time-sensitive patterns.
* **Machine Learning Integration**: Building predictive models using these results could enhance campaign targeting and optimization. 
</p>

## Contributing
<p align="justify">
Contributions are welcome! If you would like to suggest improvements, report issues, or contribute to the project, feel free to open a pull request or submit an issue.
</p>

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For more details, please refer to the [project report](https://github.com/VirendraChavda/Marketing-Effectivenes/blob/main/A_B%20Testing.ipynb).
