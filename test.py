import pandas as pd
import openpyxl
import ollama

#Key helper functions---------------------------------------------------------------------
def KPI_prompt_text(current_KPI,prior_KPI,KPI_name):
    if current_KPI > prior_KPI:
        text = f'{KPI_name} has increased from {str(prior_KPI)} to {str(current_KPI)}'
    elif current_KPI < prior_KPI:
        text = f'{KPI_name} has decreased from {str(prior_KPI)} to {str(current_KPI)}'
    else:
        text = f'{KPI_name} has remained the same'
    
    return text

def amount_prompt_text(variance,percentage_change):
    if variance ==0:
        variance_descriptor = "Amount has remained the same"
    elif variance >0:
        variance_descriptor = f'Amount has increased by £{abs(variance):,.2f} ({percentage_change:,.1f}%)'
    else:
        variance_descriptor = f'Amount has decreased by £{abs(variance):,.2f} ({percentage_change:,.1f}%)'
    
    return variance_descriptor

#Key program parameters----------------------------------------------
llm_system_prompt = 'You are an expert financial analyst, and as part of your month-end pack to the board you are providing a \
short but meaningful and insightful explanation of the month-on-month movements for this financial cost line item \
providing any derived KPIs where appropriate.Keep commentary brief but insightful, this will only be shown as one excel line item'

file_path = r"C:\Users\craig\OneDrive\Desktop\Example_Financials.xlsx"

kpi_links = {
    "Salaries": "Headcount",
    "Software Licences": "Number of Licences",
    "Consulting Fees": "Active Projects"
}#

commentaries=[]

#Start of main program
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
period_prompt_text = f'\nCurrent Period: {current_period}\nPrior period: {prior_period}\n'
comp_periods_amt = current_period + " vs. " + prior_period + " (£)"
comp_periods_perc = current_period + " vs. " + prior_period + " (%)"

kpi_dict = df_kpis.set_index("KPI")[[current_period,prior_period]].to_dict(orient="index")

for _,row in df_financials.iterrows():
    amount_variance = row[comp_periods_amt]
    percent_variance = row[comp_periods_perc]
    line_item_name = row["Line Item"]

    if line_item_name in kpi_links:
        kpi_name = kpi_links[line_item_name]
        kpi_text = KPI_prompt_text(kpi_dict[kpi_name][current_period],
                                   kpi_dict[kpi_name][prior_period],
                                   kpi_name)
    else:
        kpi_text ="No relevant KPI available"

    prompt = f'Line item: {line_item_name}{period_prompt_text}\
{amount_prompt_text(amount_variance,percent_variance)}\n{kpi_text}\n\n{llm_system_prompt}'

    #interact with the LLM to generate a response for this given prompt
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
)           
    commentaries.append(response.message.content)

df_financials["Commentary"] = commentaries
df_financials.to_excel('output.xlsx', sheet_name='Sheet1', index=False)

