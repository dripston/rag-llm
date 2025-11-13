import asyncio
from chunk_prisma_data import fetch_prisma_data

async def test_fetch():
    print("Testing data fetch...")
    data = await fetch_prisma_data()
    print("Data fetched successfully!")
    print(f"Keys: {data.keys()}")
    for key, value in data.items():
        print(f"  {key}: {len(value) if isinstance(value, list) else type(value)} items")
    return data

if __name__ == "__main__":
    print("Running simple test...")
    data = asyncio.run(test_fetch())
    print("Test completed!")