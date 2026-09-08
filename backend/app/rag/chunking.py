def split_text(text: str, chunk_size: int = 800, chunk_overlap: int = 150) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be between zero and chunk_size - 1")

    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start
        current_length = 0
        while end < len(words):
            word_length = len(words[end])
            separator_length = 1 if end > start else 0
            if end > start and current_length + separator_length + word_length > chunk_size:
                break
            current_length += separator_length + word_length
            end += 1

        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break

        overlap_length = 0
        overlap_start = end
        while overlap_start > start:
            candidate_length = len(words[overlap_start - 1])
            separator_length = 1 if overlap_start < end else 0
            if overlap_length and overlap_length + separator_length + candidate_length > chunk_overlap:
                break
            if not overlap_length and candidate_length > chunk_overlap:
                break
            overlap_length += separator_length + candidate_length
            overlap_start -= 1
        start = min(end, overlap_start)
    return chunks
