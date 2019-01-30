# Gerryscore

## Summary
This code ranks states based on how much gerrymandering is going on inside its Congressional districts. 

## Methodology
A mean-median difference test is utilized to quantify the extend that gerrymandering is happening within a state. This compares a party's statewide votes to the number of Congressional seats that it wins. A z-score is calculated by dividing the mean-median difference by the standard error. Finally, a min-max scaler is applied to the z-scores to make them into a more interpretable format.

### Data
Data was obtained from Princenton University Library's Election and Voting Data Guide
https://libguides.princeton.edu/elections 

### Results
![alt text](https://github.com/nbucklin/gerryscore/Bar Chart.png)

