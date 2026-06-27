import time
import random

def call_gemini_with_retry(client, model: str, contents, config, max_retries: int = 4, initial_delay: float = 4.0):
    """
    Executes a Gemini API call with exponential backoff and jitter when encountering 
    rate limits (429) or transient server overloads (503).
    """
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
        except Exception as e:
            err_msg = str(e)
            # Identify rate limit (429) or temporary server errors (503/Quota)
            is_transient_error = (
                "429" in err_msg 
                or "RESOURCE_EXHAUSTED" in err_msg 
                or "503" in err_msg
                or "quota" in err_msg.lower()
                or "rate limit" in err_msg.lower()
            )
            
            if is_transient_error and attempt < max_retries - 1:
                # Add jitter to prevent coordinated thundering herd issues
                sleep_time = delay + random.uniform(0.5, 1.5)
                print(f"Gemini API rate limit or transient error encountered: {err_msg[:120]}...")
                print(f"Retrying in {sleep_time:.2f}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(sleep_time)
                delay *= 2  # Double the backoff duration for the next retry
            else:
                # If we've exhausted all retries or it's a non-retryable error (e.g. 400 Bad Request), raise it
                raise e
