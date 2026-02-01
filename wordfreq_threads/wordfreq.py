import sys
import re
from collections import Counter
from threading import Thread


def find_segment_bounds(text: str, start: int, end: int) -> tuple[int, int]:
    """
    Adjust segment boundaries so we don't split words.
    Moves start forward to next whitespace if inside a word.
    Moves end backward to previous whitespace if inside a word.
    """
    n = len(text)
    start = max(0, min(start, n))
    end = max(0, min(end, n))

    # Adjust start forward if it's in the middle of a word
    if start > 0 and start < n and text[start-1].isalnum() and text[start].isalnum():
        while start < n and not text[start].isspace():
            start += 1

    # Adjust end backward if it's in the middle of a word
    if end > 0 and end < n and text[end-1].isalnum() and text[end].isalnum():
        while end > 0 and not text[end-1].isspace():
            end -= 1

    if start > end:
        start = end
    return start, end


def tokenize(segment: str) -> list[str]:
    # Lowercase and extract word-like tokens (keeps apostrophes in contractions)
    return re.findall(r"[a-zA-Z0-9']+", segment.lower())


def worker(thread_id: int, segment_text: str, results: list):
    words = tokenize(segment_text)
    counts = Counter(words)
    results[thread_id] = counts

    # Intermediate output (show top 10 to keep output readable)
    top10 = counts.most_common(10)
    print(
        f"[Thread {thread_id}] segment words={len(words)} unique={len(counts)} top10={top10}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 wordfreq.py <input_file> <N_segments>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        N = int(sys.argv[2])
        if N <= 0:
            raise ValueError
    except ValueError:
        print("N_segments must be a positive integer.")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    if len(text) == 0:
        print("Input file is empty.")
        sys.exit(0)

    # If N is bigger than text length, cap it to avoid too many empty segments
    N = min(N, len(text))

    chunk_size = len(text) // N
    segments = []

    for i in range(N):
        raw_start = i * chunk_size
        raw_end = (i + 1) * chunk_size if i < N - 1 else len(text)
        start, end = find_segment_bounds(text, raw_start, raw_end)
        segments.append(text[start:end])

    results = [None] * N
    threads = []

    for i in range(N):
        t = Thread(target=worker, args=(i, segments[i], results))
        threads.append(t)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # Consolidate results
    final_counts = Counter()
    for c in results:
        if c is not None:
            final_counts.update(c)

    print("\n=== Final Consolidated Word Frequency (Top 20) ===")
    for word, freq in final_counts.most_common(20):
        print(f"{word}: {freq}")


if __name__ == "__main__":
    main()
