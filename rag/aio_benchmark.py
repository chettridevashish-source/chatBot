import asyncio
import aiohttp
import time
import argparse
import statistics

async def fetch_chat(session, url, question):
    start_time = time.perf_counter()
    try:
        async with session.post(url, json={"question": question}, timeout=120.0) as response:
            status = response.status
            # read the stream to the end
            content_length = 0
            first_token_time = None
            async for chunk in response.content.iter_chunked(1024):
                if not first_token_time and chunk:
                    first_token_time = time.perf_counter() - start_time
                content_length += len(chunk)
            
            total_time = time.perf_counter() - start_time
            if first_token_time is None:
                first_token_time = total_time
                
            return status, total_time, first_token_time, content_length
    except Exception as e:
        return 500, time.perf_counter() - start_time, 0, 0

async def run_benchmark(concurrent_users):
    url = "http://127.0.0.1:8000/chat"
    question = "What are the documents required for an ST certificate?"
    
    print(f"\n🚀 Starting benchmark with {concurrent_users} concurrent users...")
    
    start_time = time.perf_counter()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_chat(session, url, question) for _ in range(concurrent_users)]
        results = await asyncio.gather(*tasks)
        
    total_time = time.perf_counter() - start_time
    
    statuses = [r[0] for r in results]
    latencies = [r[1] for r in results if r[0] == 200]
    ttfts = [r[2] for r in results if r[0] == 200]
    
    success_count = statuses.count(200)
    rate_limit_count = statuses.count(429)
    timeout_count = statuses.count(504)
    error_count = len(statuses) - success_count - rate_limit_count - timeout_count
    
    print("-" * 50)
    print(f"Total Requests: {concurrent_users}")
    print(f"Success (200) : {success_count}")
    print(f"Queue Full (429): {rate_limit_count}")
    print(f"Timeouts (504): {timeout_count}")
    print(f"Errors (500)  : {error_count}")
    print(f"Throughput    : {success_count / total_time:.2f} req/sec")
    
    if latencies:
        print(f"Avg Latency   : {statistics.mean(latencies):.2f}s")
        if len(latencies) >= 2:
            print(f"P95 Latency   : {statistics.quantiles(latencies, n=100)[94]:.2f}s")
        else:
            print(f"P95 Latency   : {latencies[0]:.2f}s")
        print(f"Avg TTFT      : {statistics.mean(ttfts):.2f}s")
    print("-" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=10, help="Number of concurrent users")
    args = parser.parse_args()
    asyncio.run(run_benchmark(args.users))
