import numpy as np
import pandas as pd

def output_for_sankey(output, availablechildflows, availablechildstocks, allflownumbersmatrix):
    """
    Function which creates a spreadsheet showing results of flows to use as a base for Sankey diagrams.
    """

    # Initialize an empty list to store rows
    output_flownav_list = []

    for i in range(len(availablechildflows)):
        relevantrow = np.where(allflownumbersmatrix[:, 0] == str(availablechildflows[i]))
        relevantrow = relevantrow[0][0]
        flownumberfrom = allflownumbersmatrix[relevantrow, 1]
        flownumberto = allflownumbersmatrix[relevantrow, 2]

        # Append the values directly to the list
        output_flownav_list = output_flownav_list.append({
            'flownumberfrom': flownumberfrom,
            'flownumberto': flownumberto,
            'parentflownumberfrom': np.nan,
            'parentflownumberto': np.nan,
            'navigation': np.nan
        })

    # Create a DataFrame using the list of dictionaries
    output_flownav = pd.DataFrame.from_records(output_flownav_list)

    # Save the result to a CSV file
    output_flownav.to_csv('output.csv', index=False)

    # Save the result to an Excel file
    output_flownav.to_excel('output.xlsx', sheet_name='output', index=False)

# Example usage:
# output_for_sankey(output, availablechildflows, availablechildstocks, allflownumbersmatrix)
