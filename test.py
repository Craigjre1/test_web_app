import pandas as pd
import openpyxl

file_path = r"C:\Users\craig\OneDrive\Desktop\Example_Financials.xlsx"

df_dict = pd.read_excel(file_path,sheet_name=None)
df_financials = df_dict["Financials"]
df_kpis = df_dict["KPIs"]

df_cols = df_financials.columns
period_cols = [col for col in df_financials.columns if col.endswith(" (£)")]

for i in range(1,len(period_cols)):
    current_period = period_cols[i]
    prior_period = period_cols[i-1]
    period_label = (current_period + "vs. " + prior_period).replace("(£)","")
    df_financials[period_label + "(£)"] = df_financials[current_period] - df_financials[prior_period]
    df_financials[period_label + "(%)"] = df_financials.apply(
        lambda row:((row[current_period]/row[prior_period]-1)*100) if row[prior_period] !=0 else None, axis = 1
        )

current_period = current_period.replace("(£)","").strip()
prior_period = prior_period.replace("(£)","").strip()
comp_periods_amt = current_period + " vs. " + prior_period + " (£)"
comp_periods_perc = current_period + " vs. " + prior_period + " (%)"

kpi_dict = df_kpis.set_index("KPI")[[current_period,prior_period]].to_dict(orient="index")
current_headcount = kpi_dict["Headcount"][current_period]
prior_headcount = kpi_dict["Headcount"][prior_period]

if current_headcount > prior_headcount:
    adjective = "increased"
elif current_headcount < prior_headcount:
    adjective = "decreased"
else:
    adjective = "N/A"

for index,row in df_financials.iterrows():
    if row['Line Item'] == "Salaries":
        prompt = f'Line item: Salaries \nCurrent Period: {current_period}\nPrior period: {prior_period}\n\
{"Amount has remained the same" if row[comp_periods_amt] ==0 else ("Amount has increased by £" if row[comp_periods_amt] > 0 else\
"Amount has decreased by £")}{abs(row[comp_periods_amt]):,.2f} ({row[comp_periods_perc]:,.1f}%)\n\
{"Headcount has remained the same" if adjective == 'N/A' else \
"Headcount has " + adjective + " from " + str(prior_headcount) + " to " + str(current_headcount)}\n\n\
You are an expert financial analyst, and as part of your month-end pack to the board you are providing a\
short but meaningful and insightful explanation of the month-on-month movements for this financial line item.'
        print(prompt)

# Write a short explanation of this change for a financial commentary.

#print(df_financials.head(3))

#df_financials.to_excel('output.xlsx', sheet_name='Sheet1', index=False)