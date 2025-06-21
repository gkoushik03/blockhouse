import csv

def is_valid(row):
    """
    Validate a single row from the L2 order book CSV.
    Checks:
    - bid price < ask price
    - bid size > 0 and ask size > 0
    - all necessary fields can be converted to float
    """
    try:
        bid_px = float(row['bid_px_00'])
        ask_px = float(row['ask_px_00'])
        bid_sz = float(row['bid_sz_00'])
        ask_sz = float(row['ask_sz_00'])
    except (ValueError, KeyError):
        return False

    if bid_px >= ask_px:
        return False
    if bid_sz <= 0 or ask_sz <= 0:
        return False
    return True

def preprocess_csv(input_csv_path, output_csv_path):
    """
    Reads input CSV, filters valid rows, writes them to output CSV.
    """
    with open(input_csv_path, 'r', newline='') as infile, \
         open(output_csv_path, 'w', newline='') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()
        valid_rows = 0
        total_rows = 0

        for row in reader:
            total_rows += 1
            if is_valid(row):
                writer.writerow(row)
                valid_rows += 1
            # else: # optionally log invalid rows here

        print(f"Processed {total_rows} rows, wrote {valid_rows} valid rows to {output_csv_path}")

if __name__ == '__main__':
    input_csv = 'l1_day.csv'    # Replace with your input CSV filename
    output_csv = 'cleaned_l2_orderbook.csv'  # Cleaned data output

    preprocess_csv(input_csv, output_csv)
