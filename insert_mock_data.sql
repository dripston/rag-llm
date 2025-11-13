-- Insert mock data into Hospital table
INSERT INTO "Hospital" (hospital_id, hospital_name, address, phone_number, created_at) VALUES
('HOSP001', 'City General Hospital', '123 Main St, Cityville', '123-456-7890', NOW()),
('HOSP002', 'Town Medical Center', '456 Oak Ave, Townsville', '098-765-4321', NOW()),
('HOSP003', 'Regional Health Complex', '789 Pine Rd, Villagetown', '555-123-4567', NOW());

-- Insert mock data into Doctor table
INSERT INTO "Doctor" (doctor_id, doctor_name, hospital_id, phone_number, certificate_url, id_document_url, profile_image_url, created_at) VALUES
('DOC001', 'Dr. Smith', 'HOSP001', '111-222-3333', 'https://example.com/cert1.pdf', 'https://example.com/id1.pdf', 'https://example.com/doc1.jpg', NOW()),
('DOC002', 'Dr. Johnson', 'HOSP002', '444-555-6666', 'https://example.com/cert2.pdf', 'https://example.com/id2.pdf', 'https://example.com/doc2.jpg', NOW()),
('DOC003', 'Dr. Williams', 'HOSP001', '777-888-9999', 'https://example.com/cert3.pdf', 'https://example.com/id3.pdf', 'https://example.com/doc3.jpg', NOW()),
('DOC004', 'Dr. Brown', 'HOSP003', '222-333-4444', 'https://example.com/cert4.pdf', 'https://example.com/id4.pdf', 'https://example.com/doc4.jpg', NOW()),
('DOC005', 'Dr. Miller', 'HOSP002', '666-777-8888', 'https://example.com/cert5.pdf', 'https://example.com/id5.pdf', 'https://example.com/doc5.jpg', NOW());

-- Insert mock data into User table (adding more users)
INSERT INTO "User" (user_id, user_name, transcripted_data, audio_url, treated_by, hospital_id, user_mobile, address, created_at) VALUES
('USR001', 'John Doe', 'Patient complains of headaches and dizziness for the past 3 days.', 'https://example.com/audio1.mp3', 'DOC001', 'HOSP001', '1234567890', '123 Main St, Cityville', NOW()),
('USR002', 'Jane Smith', 'Routine checkup, patient reports feeling healthy.', 'https://example.com/audio2.mp3', 'DOC002', 'HOSP002', '0987654321', '456 Oak Ave, Townsville', NOW()),
('USR003', 'Robert Johnson', 'Patient has been experiencing chest pain after exercise.', 'https://example.com/audio3.mp3', 'DOC003', 'HOSP001', '5551234567', '789 Pine Rd, Villagetown', NOW()),
('USR004', 'Emily Davis', 'Follow-up visit for diabetes management.', 'https://example.com/audio4.mp3', 'DOC004', 'HOSP003', '4445556666', '321 Elm Blvd, Hamlet', NOW()),
('USR005', 'Michael Wilson', 'Patient reports difficulty sleeping and anxiety.', 'https://example.com/audio5.mp3', 'DOC005', 'HOSP002', '7778889999', '654 Maple Dr, Borough', NOW());

-- Insert mock data into Interaction table
INSERT INTO "Interaction" (id, doctor_id, patient_id, audio_url, transcripted_data, soap_notes, reports_url, created_at) VALUES
('INT001', 'DOC001', 'USR001', 'https://example.com/int1.mp3', 'Patient reports headaches occurring 2-3 times daily, lasting 30-45 minutes. No visual disturbances. Associated with mild dizziness.', 'Tension-type headaches, possibly stress-related. Rule out other causes.', 'https://example.com/report1.pdf', NOW()),
('INT002', 'DOC002', 'USR002', 'https://example.com/int2.mp3', 'Patient feels generally well. No specific complaints at this time.', 'Overall good health. Normal routine checkup.', 'https://example.com/report2.pdf', NOW()),
('INT003', 'DOC003', 'USR003', 'https://example.com/int3.mp3', 'Chest pain described as pressure-like, occurring during or after physical activity. Lasts 5-10 minutes. No radiation. Associated with shortness of breath.', 'Suspect stable angina. Possible hypertension.', 'https://example.com/report3.pdf', NOW()),
('INT004', 'DOC004', 'USR004', 'https://example.com/int4.mp3', 'Patient reports blood glucose levels have been well-controlled. No episodes of hypoglycemia. Minor concerns about diet adherence.', 'Good diabetes control. Patient is managing condition well.', 'https://example.com/report4.pdf', NOW()),
('INT005', 'DOC005', 'USR005', 'https://example.com/int5.mp3', 'Patient describes racing thoughts at night, difficulty falling asleep. Reports feeling on edge and irritable during the day.', 'Generalized anxiety disorder with associated insomnia.', 'https://example.com/report5.pdf', NOW());

-- Insert mock data into Report table
INSERT INTO "Report" (id, "userId", file_url, note, created_at) VALUES
('REP001', 'USR001', 'https://example.com/blood_test1.pdf', 'Complete blood count within normal limits', NOW()),
('REP002', 'USR002', 'https://example.com/cholesterol1.pdf', 'Cholesterol levels slightly elevated', NOW()),
('REP003', 'USR003', 'https://example.com/ecg1.pdf', 'ECG shows nonspecific ST changes', NOW()),
('REP004', 'USR004', 'https://example.com/glucose1.pdf', 'Fasting glucose: 110 mg/dL', NOW()),
('REP005', 'USR005', 'https://example.com/thyroid1.pdf', 'TSH levels normal', NOW());

-- Insert mock data into SoapNote table
INSERT INTO "SoapNote" (id, "userId", note, created_at) VALUES
('SOAP001', 'USR001', 'Subjective: Patient reports headaches occurring 2-3 times daily, lasting 30-45 minutes. No visual disturbances. Associated with mild dizziness. Objective: Blood pressure: 130/85. Heart rate: 72 bpm. Neurological exam: grossly normal. Assessment: Tension-type headaches, possibly stress-related. Rule out other causes. Plan: Prescribe relaxation techniques. Schedule follow-up in 2 weeks. Consider physical therapy.', NOW()),
('SOAP002', 'USR002', 'Subjective: Patient feels generally well. No specific complaints at this time. Objective: Blood pressure: 118/76. Heart rate: 68 bpm. Weight: 150 lbs. All vitals within normal limits. Assessment: Overall good health. Normal routine checkup. Plan: Continue current healthy habits. Schedule annual checkup next year.', NOW()),
('SOAP003', 'USR003', 'Subjective: Chest pain described as pressure-like, occurring during or after physical activity. Lasts 5-10 minutes. No radiation. Associated with shortness of breath. Objective: Blood pressure: 142/90. Heart rate: 78 bpm. EKG shows nonspecific ST changes. Assessment: Suspect stable angina. Possible hypertension. Plan: Order stress test. Start patient on low-dose aspirin. Refer to cardiologist.', NOW()),
('SOAP004', 'USR004', 'Subjective: Patient reports blood glucose levels have been well-controlled. No episodes of hypoglycemia. Minor concerns about diet adherence. Objective: Blood glucose: 110 mg/dL (fasting). HbA1c: 6.2%. Weight: 175 lbs. Assessment: Good diabetes control. Patient is managing condition well. Plan: Continue current medication regimen. Provide dietary counseling. Schedule 3-month follow-up.', NOW()),
('SOAP005', 'USR005', 'Subjective: Patient describes racing thoughts at night, difficulty falling asleep. Reports feeling on edge and irritable during the day. Objective: Appears anxious during visit. Pulse: 88 bpm. Blood pressure: 125/80. Assessment: Generalized anxiety disorder with associated insomnia. Plan: Refer to mental health counselor. Consider short-term anxiolytic. Provide sleep hygiene education.', NOW());