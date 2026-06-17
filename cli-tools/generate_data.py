import click

@click.group()
@click.argument('output_filepath')
def generate_and_save_data(output_filepath):
    """Generates fake data and saves it to a CSV file."""
    import csv
    import random

    from faker import Faker


    fake = Faker()
    num_records = 1000
    data = []
    positions = ["Admin", "Manager", "Department Head", "Engineer", "Analyst"]

    print(f"Generating {num_records} fake employee records...")
    for _ in range(num_records):
        data.append(
            {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "position": random.choice(positions),
                "salary": round(random.uniform(40000, 180000), 2),
                "sex": random.choice(["Male", "Female"]),
            }
        )

    output_filepath = output_filepath
    print(f"Saving data to {output_filepath}")

    with open(output_filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print("Data generation complete.")



if __name__  == "__main__":
   generate_and_save_data() 
