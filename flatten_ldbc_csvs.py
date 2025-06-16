import os
import shutil

def flatten_ldbc_csvs(input_root, output_dir):
    """
    Flattens LDBC SNB csv output by copying all .csv files from nested subdirs of `input_root`
    into `output_dir`, renaming them as e.g., dynamic__Person.csv
    """
    if not os.path.isdir(input_root):
        raise ValueError(f"Input path does not exist: {input_root}")

    os.makedirs(output_dir, exist_ok=True)

    for subdir in ['dynamic', 'static']:
        subdir_path = os.path.join(input_root, subdir)
        if not os.path.isdir(subdir_path):
            print(f"Warning: Missing expected subdir {subdir_path}")
            continue

        for entity_name in os.listdir(subdir_path):
            entity_path = os.path.join(subdir_path, entity_name)
            if not os.path.isdir(entity_path):
                continue

            for file in os.listdir(entity_path):
                if not file.endswith(".csv") or file.startswith('_') or file.startswith('.'):
                    continue

                full_input_path = os.path.join(entity_path, file)
                flat_filename = f"{subdir}__{entity_name}.csv"
                full_output_path = os.path.join(output_dir, flat_filename)

                print(f"Copying {full_input_path} → {full_output_path}")
                shutil.copyfile(full_input_path, full_output_path)

    print(f"\nDone. Flattened CSVs are in: {output_dir}")


if __name__ == "__main__":
    # Change these paths as needed
    INPUT_DIR = "out/graphs/csv/raw/composite-merged-fk"
    OUTPUT_DIR = "flat_csv"

    flatten_ldbc_csvs(INPUT_DIR, OUTPUT_DIR)
