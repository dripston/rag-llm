from medical_rag import MedicalRAG

# Test the Medical RAG system
rag = MedicalRAG()
matches = rag.search_similar_documents('patient usr001 medical history', top_k=3)
print('Found matches:', len(matches))

for i, match in enumerate(matches):
    print(f'Match {i+1}: ID={match["id"]}, Score={match["score"]:.4f}')
    if 'metadata' in match and match['metadata']:
        print(f'  Content preview: {str(match["metadata"].get("content", ""))[:100]}...')
    print()