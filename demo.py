import pandas as pd

def detect_header_rows(df, threshold_ratio=0.5):
    """
    Detects the number of top rows that are misstructured headers.
    A row is considered a header row if the number of cells that are NaN 
    or contain 'Unnamed' is greater than or equal to threshold_ratio * total columns.
    """
    header_rows = 0
    total_cols = df.shape[1]
    
    for idx, row in df.iterrows():
        # Count cells that are either NaN or a string starting with 'Unnamed'
        count_bad = sum(
            1 for cell in row 
            if pd.isna(cell) or (isinstance(cell, str) and cell.startswith("Unnamed"))
        )
        if count_bad >= threshold_ratio * total_cols:
            header_rows += 1
        else:
            break  # Stop when a row looks like data
    return header_rows if header_rows > 0 else 1

def auto_fix_headers(df):
    # Detect the number of misstructured header rows
    header_rows = detect_header_rows(df)
    
    # Fill empty cells with empty strings in the header rows
    top = df.head(header_rows).fillna('')
    
    # Combine the detected header rows for each column
    new_header = [
        " ".join(
            str(top.iloc[r, c]).strip() 
            for r in range(header_rows) 
            if str(top.iloc[r, c]).strip() and not str(top.iloc[r, c]).strip().startswith("Unnamed")
        ).strip() or f"Column_{c}"
        for c in range(df.shape[1])
    ]
    
    df.columns = new_header  # Set new header
    return df.iloc[header_rows:].reset_index(drop=True)

# Example usage on the provided CSV data:
csv_data = """Sonesta Simply Suites Midwestern & Northeastern Portfolio,Unnamed: 0,Unnamed: 1,Unnamed: 2,Unnamed: 3,Unnamed: 4,Unnamed: 5,Unnamed: 6,Unnamed: 7,Unnamed: 8,Unnamed: 9
HOTEL KEYS 2017,2018,2019,2020,2021,2022,2023,2024,CAPEX 2017 - Q3 2024,nan,CAPEX 2017 - Q3 2024/KEY
"sonesta simply suites Des Moines 98  $59,031","$160,605","$71,558","$24,890","$56,538","$22,993","$34,638","$207,609","$637,861",nan,"$6,509"
"sonesta simply suites Chicago Waukegan 122  $151,284","$170,636","$184,843","$42,535","$138,052","$66,428","$179,086","$224,468","$1,157,332",nan,"$9,486"
"sonesta simply suites Chicago libertyville 122  $78,721","$200,852","$68,787","$128,508","$316,234","$80,848","$74,167","$198,093","$1,146,211",nan,"$9,395"
"sonesta simply suites Chicago naperville 122  $100,657","$207,920","$184,735","$45,803","$331,312","$12,951","$205,338","$113,654","$1,202,370",nan,"$9,855"
"sonesta simply suites Chicago o'Hare 160  $388,168","$45,540","$266,078","$33,689","$362,921","$35,186","$488,198","$1,213,317","$2,833,098",nan,"$17,707"
"sonesta simply suites boston braintree 133  $357,805","$26,171","$197,550","$228,220","$128,699","$282,590","$901,683","$809,548","$2,932,266",nan,"$22,047"
"sonesta simply suites baltimore bWI airport 125  $247,971","$78,872","$149,856","$112,860","$159,153","$15,266","$713,389","$585,403","$2,062,770",nan,"$16,502"
"sonesta simply suites Detroit Warren 122  $35,644","$199,877","$122,664","$62,440","$49,465","$49,734","$562,771","$118,728","$1,201,323",nan,"$9,847"
"sonesta simply suites Detroit Troy 118  $222,130","$58,036","$71,787","$27,176","$72,115","$36,978","$346,802","$307,769","$1,142,793",nan,"$9,685"
"sonesta simply suites Detroit ann arbor 122  $225,294","$72,700","$73,527","$45,787","$172,123","$58,346","$183,810","$420,923","$1,252,510",nan,"$10,266"
"sonesta simply suites st. louis earth City 122  $76,687","$195,558","$143,835","$50,190","$97,021","$35,928","$69,788","$351,477","$1,020,484",nan,"$8,365"
"sonesta simply suites Parsippany Morris Plains 122  $215,525","$54,535","$53,767","$42,423","$204,026","$156,287","$186,136","$228,432","$1,141,132",nan,"$9,354"
"sonesta simply suites Cleveland north olmstead airport 125  $209,905","$87,629","$118,083","$207,742","$181,676","$22,832","$603,417","$48,748","$1,480,031",nan,"$11,840"
"sonesta simply suites Columbus airport 122  $73,358","$201,927","$146,243","$35,593","$79,965","$90,580","$527,957","$98,160","$1,253,782",nan,"$10,277"
"sonesta simply suites Pittsburgh airport 123  $108,651","$264,724","$103,527","$40,821","$164,003","$14,240","$344,523","$123,942","$1,164,431",nan,"$9,467"
"sonesta simply suites Hampton 98  $83,612","$255,099","$33,377","$112,706","$42,195","$49,519","$69,168","$252,593","$898,268",nan,"$9,166"
"Total  1,956  $2,634,443","$2,280,681","$1,990,216","$1,241,385","$2,555,497","$1,030,705","$5,490,872","$5,302,862","$22,526,662",nan,"$11,517"
"""

# Read CSV data into a DataFrame (simulate reading from file)
from io import StringIO
df = pd.read_csv(StringIO(csv_data))

# Fix headers automatically
fixed_df = auto_fix_headers(df)
print(fixed_df)
