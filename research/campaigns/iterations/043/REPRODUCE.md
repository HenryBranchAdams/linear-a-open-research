# Reproduce C043's admission summary

From the extracted current project root:

```bash
python3 iterations/043/analysis/check_join.py
```

Compare the printed JSON with `iterations/043/analysis/result.json`. The inputs are the preserved exact five-carrier join, including original catalogue field captures and missingness. The calculation selects readable rows and reports which physical classes they represent; it does not assess the truth of the source's physical reconstruction or translate SI-KA.

The analysis rule and physical selection were frozen before the current exact-sign joins. They were not frozen before all historical source/object exposure. Original CMS/GORILA target pages remain an access limit. Reproducing an eligibility failure is not a negative semantic test.
