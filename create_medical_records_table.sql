-- Create the medical_records table with the specified columns
CREATE TABLE medical_records (
  user_id TEXT PRIMARY KEY,              -- your custom-generated user ID
  user_name TEXT NOT NULL,               -- user's name
  transcripted_data TEXT,                -- text from transcription
  audio_url TEXT,                        -- audio file URL (from Supabase Storage)
  treated_by TEXT,                       -- doctor name
  hospital_id TEXT,                      -- optional hospital identifier
  user_mobile VARCHAR(15),               -- user's mobile number
  address TEXT,                          -- user's address
  created_at TIMESTAMP DEFAULT NOW()     -- record creation time
);

-- Add SOAP notes table
CREATE TABLE soap_notes (
  id SERIAL PRIMARY KEY,                 -- auto-incrementing ID
  medical_record_id TEXT REFERENCES medical_records(user_id), -- foreign key to medical_records
  subjective TEXT,                       -- subjective notes
  objective TEXT,                        -- objective observations
  assessment TEXT,                       -- assessment details
  plan TEXT,                             -- treatment plan
  created_at TIMESTAMP DEFAULT NOW()     -- note creation time
);

-- Insert dummy data into medical_records table
INSERT INTO medical_records (user_id, user_name, transcripted_data, audio_url, treated_by, hospital_id, user_mobile, address) VALUES
('USR001', 'John Doe', 'Patient complains of headaches and dizziness for the past 3 days.', 'https://bubvzeylnvznjlzcalgx.supabase.co/storage/v1/object/public/audio/consultation_001.mp3', 'Dr. Smith', 'HOSP001', '1234567890', '123 Main St, Cityville'),
('USR002', 'Jane Smith', 'Routine checkup, patient reports feeling healthy.', 'https://bubvzeylnvznjlzcalgx.supabase.co/storage/v1/object/public/audio/consultation_002.mp3', 'Dr. Johnson', 'HOSP002', '0987654321', '456 Oak Ave, Townsville'),
('USR003', 'Robert Johnson', 'Patient has been experiencing chest pain after exercise.', 'https://bubvzeylnvznjlzcalgx.supabase.co/storage/v1/object/public/audio/consultation_003.mp3', 'Dr. Williams', 'HOSP001', '5551234567', '789 Pine Rd, Villagetown'),
('USR004', 'Emily Davis', 'Follow-up visit for diabetes management.', 'https://bubvzeylnvznjlzcalgx.supabase.co/storage/v1/object/public/audio/consultation_004.mp3', 'Dr. Brown', 'HOSP003', '4445556666', '321 Elm Blvd, Hamlet'),
('USR005', 'Michael Wilson', 'Patient reports difficulty sleeping and anxiety.', 'https://bubvzeylnvznjlzcalgx.supabase.co/storage/v1/object/public/audio/consultation_005.mp3', 'Dr. Miller', 'HOSP002', '7778889999', '654 Maple Dr, Borough');

-- Insert dummy data into soap_notes table
INSERT INTO soap_notes (medical_record_id, subjective, objective, assessment, plan) VALUES
('USR001', 'Patient reports headaches occurring 2-3 times daily, lasting 30-45 minutes. No visual disturbances. Associated with mild dizziness.', 'Blood pressure: 130/85. Heart rate: 72 bpm. Neurological exam: grossly normal.', 'Tension-type headaches, possibly stress-related. Rule out other causes.', 'Prescribe relaxation techniques. Schedule follow-up in 2 weeks. Consider physical therapy.'),
('USR002', 'Patient feels generally well. No specific complaints at this time.', 'Blood pressure: 118/76. Heart rate: 68 bpm. Weight: 150 lbs. All vitals within normal limits.', 'Overall good health. Normal routine checkup.', 'Continue current healthy habits. Schedule annual checkup next year.'),
('USR003', 'Chest pain described as pressure-like, occurring during or after physical activity. Lasts 5-10 minutes. No radiation. Associated with shortness of breath.', 'Blood pressure: 142/90. Heart rate: 78 bpm. EKG shows nonspecific ST changes.', 'Suspect stable angina. Possible hypertension.', 'Order stress test. Start patient on low-dose aspirin. Refer to cardiologist.'),
('USR004', 'Patient reports blood glucose levels have been well-controlled. No episodes of hypoglycemia. Minor concerns about diet adherence.', 'Blood glucose: 110 mg/dL (fasting). HbA1c: 6.2%. Weight: 175 lbs.', 'Good diabetes control. Patient is managing condition well.', 'Continue current medication regimen. Provide dietary counseling. Schedule 3-month follow-up.'),
('USR005', 'Patient describes racing thoughts at night, difficulty falling asleep. Reports feeling on edge and irritable during the day.', 'Appears anxious during visit. Pulse: 88 bpm. Blood pressure: 125/80.', 'Generalized anxiety disorder with associated insomnia.', 'Refer to mental health counselor. Consider short-term anxiolytic. Provide sleep hygiene education.');