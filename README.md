# cse4153_pa3

A study on Backoff Protocols

2.1 Linear Backoff
You will start by implementing a backoff protocol named linear backoff. In this protocol, the initial
window size is 2 slots. Each subsequent window increases by 1 slot.

For example, |W1| = 2, |W2| = 3, |W3|=4, etc.

2.2 Binary Exponential Backoff
The next backoff protocol to be implemented is the familiar binary exponential backoff protocol. The
initial window size is 2 slots. Each subsequent window increases by a multiplicative factor of 2.

For example |W1| = 2, |W2| = 4, |W3|=8, etc.

2.3 LogLog Backoff
The final backoff protocol is called loglog backoff. Here, the initial window size is 4 slots. Each
subsequent window is defined as follows. For a current window Wj which has just ended, the next
window Wj+1 has (1 + 1/log2log2(|Wj|))*|Wj| slots; when this value is not an integer, you should take the
floor of the value. Note that the logarithm is base 2.

For example, |W1| = 4, |W2| = (1 + 1/log2log2(4))*4 = 8, |W3| = (1 + 1/log2log2(8))*8 = 13 , etc. 