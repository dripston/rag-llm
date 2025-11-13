import json

# Check if HOSP004 is in the chunked data
with open('chunked_prisma_data.json', 'r') as f:
    data = json.load(f)
    
hosp004_count = 0
for item in data:
    if 'HOSP004' in item.get('content', ''):
        hosp004_count += 1
        print("Found HOSP004 in chunk:")
        print(item['content'][:200] + "...")
        
print(f"HOSP004 found in {hosp004_count} chunks")

# Also check the total number of chunks
print(f"Total chunks: {len(data)}")

# Check for all hospital IDs
hospital_ids = set()
for item in data:
    content = item.get('content', '')
    if 'Hospital Information:' in content:
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('ID: HOSP'):
                hospital_ids.add(line.strip())

print(f"All hospital IDs found: {sorted(hospital_ids)}")

# Check for all doctor-hospital relationships
doctor_hospitals = set()
for item in data:
    content = item.get('content', '')
    if 'Doctor Information:' in content:
        lines = content.split('\n')
        doctor_id = None
        hospital_id = None
        for line in lines:
            if line.strip().startswith('ID: DOC'):
                doctor_id = line.strip()
            elif line.strip().startswith('Hospital ID: HOSP'):
                hospital_id = line.strip()
        if doctor_id and hospital_id:
            doctor_hospitals.add(f"{doctor_id} -> {hospital_id}")

print(f"Doctor-Hospital relationships: {sorted(doctor_hospitals)}")

# Check for all user-hospital relationships
user_hospitals = set()
for item in data:
    content = item.get('content', '')
    if 'Patient Information:' in content:
        lines = content.split('\n')
        user_id = None
        hospital_id = None
        for line in lines:
            if line.strip().startswith('ID: USR'):
                user_id = line.strip()
            elif line.strip().startswith('Hospital ID: HOSP'):
                hospital_id = line.strip()
        if user_id and hospital_id:
            user_hospitals.add(f"{user_id} -> {hospital_id}")

print(f"User-Hospital relationships: {sorted(user_hospitals)}")