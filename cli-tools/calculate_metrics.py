import click

@click.command()
@click.argument("input_filepath")
@click.argument("output_filepath")
def calculate_salary_metrics_duckdb(input_filepath, output_filepath):
    """Calculates salary metrics by position and sex."""
    import duckdb
    print(f"Reading data from {input_filepath}")
    try:
        avg_salary_by_position_sex = duckdb.sql(
            f"SELECT position, sex, AVG(salary) as average_salary "
            f"FROM '{input_filepath}' "
            'GROUP BY position, sex '
            "ORDER BY position, sex"
        )
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        raise
    print(f"Saving metrics to {output_filepath}")
    avg_salary_by_position_sex.write_csv(output_filepath)
    print("Metrics calculation complete.")

if __name__ == "__main__":
    calculate_salary_metrics_duckdb()
