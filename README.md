# Possible Algorithms
## Leaky Bucket Algorithm (LBA)
This algorithm revolves around queuing requests and processing them at a fixed rate. I decided not to go for this algorithm. My reasoning is that, in the context of HFT, either a request is processed immediately or not at all. Receiving a response late is of little use. Additionally, if the queue begins to fill up, a significant response time delay is incurred on all new requests as previous ones need to first be processed.

## Token Bucket Algorithm (TBA)
Instead of processing requests at a fixed rate, TBA generates tokens at a fixed rate and each request consumes a token. This algorithm handles sporadic requests better than LBA. As an example, if the user is allowed to make 60 requests per minute, the LBA would force the requests to be spread out over a full minute. TBA, on the other hand, allows the user to make all 60 requests within one second if the user hasn't made any request in the last 59 seconds. TBA is the most common rate limiting algorithm for APIs.

## Fixed Window Algorithm (FWA)
FWA would be my second pick for a rate limiter algorithm. The algorithm divides time into fixed windows. Within each window, a certain amount of requests are allowed, if that amount is exceeded, the user will have to wait till the next window. A notable downside is that requests can temporarily reach up to twice the allowed limit right at the edge between two windows. I have decided not to go with this algorithm. Even though the average rate will not exceed the limit, there is a risk of requests temporarily doubling the allowed rate which could result in server overload and lead to a bad user experience for all users.

# Instructions
If you want to run the rate limiter tests, you need to first install pytest. This can easily be done by running "pip install pytest" in your terminal. You can run the suite of tests using the following command "python -m pytest -v .\test_rate_limiter.py".

# Implementation Decisions
- I decided to lazily update the tokens in a bucket. A user's buckets is filled to its theoretical level based on the timestamp of the last refill only when the user attempts to make a request.
- Bucket information is stored by using a 2d array. The first value represents the number of tokens and the second value represents the timestamp of the last refill. I initially implemented this with a tuple. The downside is that tuples are immutable, so changing a value means creating a new tuple in memory and then storing a reference to it. As such, I switched to a 2d.
- I initially implemented my rate limiter with time(). I then found out that time() has the potential to go backwards under numerous circumstances whereas monotonic() doesn't. As such, I opted to use monotonic() instead.

# Sources
- https://youtu.be/MIJFyUPG4Z4?si=ak6OIvquhMLsU7I9
- https://www.youtube.com/watch?v=mQCJJqUfn9Y
- https://www.youtube.com/watch?v=YXkOdWBwqaA
- https://www.w3schools.com/python/ref_module_time.asp 