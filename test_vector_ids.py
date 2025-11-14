import hashlib

def test_vector_id_generation():
    """Test vector ID generation with content hashing"""
    
    # Test content samples
    content1 = """
        Patient Information:
        ID: USR099
        Name: Rahul Verma
        Mobile: 9123456780
        Address: 12 Lotus Residency, Mumbai
        Treated By: DR009
        Hospital ID: HOSP004
        Transcript: Patient has mild throat pain and cough
        Audio URL: https://example.com/audio/99
        Created: 2025-11-14T12:00:00Z
        """
    
    content2 = """
        Patient Information:
        ID: USR003
        Name: Robert Johnson
        Mobile: 5551234567
        Address: 789 Pine Rd, Villagetown
        Treated By: DOC003
        Hospital ID: HOSP001
        Transcript: Patient has been experiencing chest pain after exercise.
        Audio URL: https://example.com/audio3.mp3
        Created: 2025-11-12T10:30:00Z
        """
    
    # Generate vector IDs
    hash1 = hashlib.md5(content1.encode('utf-8')).hexdigest()
    vector_id1 = f"chunk_{hash1}"
    
    hash2 = hashlib.md5(content2.encode('utf-8')).hexdigest()
    vector_id2 = f"chunk_{hash2}"
    
    print(f"Content 1 hash: {hash1}")
    print(f"Vector ID 1: {vector_id1}")
    print()
    print(f"Content 2 hash: {hash2}")
    print(f"Vector ID 2: {vector_id2}")
    print()
    print(f"IDs are different: {vector_id1 != vector_id2}")

if __name__ == "__main__":
    test_vector_id_generation()