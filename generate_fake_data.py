import json
import random
import numpy as np

from faker import Faker

fake = Faker()

all_names = set()
has_spouse = set()

def generate_company():
    return {
        "name": fake.company(),
        "mission": fake.bs(),
        "catch_phrase": fake.catch_phrase()
    }

# Generate a limited set of companies
companies = [generate_company() for _ in range(20)]
company_names = [company["name"] for company in companies]

# Define role hierarchies for different job types
role_hierarchies = {
    "Data Scientist": ["Junior Data Scientist", "Data Scientist", "Senior Data Scientist", "Lead Data Scientist", "Data Science Manager"],
    "Data Engineer": ["Junior Data Engineer", "Data Engineer", "Senior Data Engineer", "Lead Data Engineer", "Data Engineering Manager"],
    "Admin": ["Admin Assistant", "Admin Coordinator", "Admin Manager", "Admin Director"]
} 

def generate_person():
    
    employment_status = np.random.choice([True, False], p=[0.8, 0.2])
    work_data = None
    if employment_status:
        job_type = random.choice(list(role_hierarchies.keys()))
        work_data = {
            "company": random.choice(company_names),
            "role": random.choice(role_hierarchies[job_type]),
            "job_type": job_type
        }

    name = fake.name()
    while name in all_names:
        name = fake.name()


    all_names.add(name)
    person = {
        "name": name,
        "work": work_data
    }
    return person



def generate_family_tree(depth, avg_num_children=2):

    if depth == 0:
        return None, None
    elif depth == 1:
        return generate_person(), None
    else:
        partner1, partner2 = generate_person(), generate_person()

        # If this same name has already been used as someone's spouse, generate a new person
        while partner1["name"] in has_spouse:
            partner1 = generate_person()
        while partner2["name"] in has_spouse:
            partner2 = generate_person()
        
        # Add them to the has_spouse set
        has_spouse.add(partner1["name"])
        has_spouse.add(partner2["name"])
        
        partner1["spouse"] = partner2["name"]
        partner2["spouse"] = partner1["name"]
        
        for _ in range(random.randint(0, avg_num_children)):
            child, _ = generate_family_tree(depth-1, random.randint(0, avg_num_children))
            if child:
                partner1["children"] = partner1.get("children", [])
                partner2["children"] = partner2.get("children", [])

                partner1["children"].append(child)
                partner2["children"].append(child)
        
        return partner1, partner2

def generate_families(num_families, avg_family_depth):
    families = []

    for _ in range(num_families):
        family_depth = int(np.random.exponential(avg_family_depth))
        partner1, partner2 = generate_family_tree(family_depth)

        if partner1 and partner2:
            families.append({"Partner 1": partner1, "Partner 2": partner2})

    return families

if __name__ == '__main__':

    num_families = 500
    avg_family_depth = 10
    families = generate_families(num_families, avg_family_depth)

    data = {
        "companies": companies,  # Include company details here
        "families": families
    }
    
    with open('companies_and_families.json', 'w') as f:
        json.dump(data, f, indent=4)

