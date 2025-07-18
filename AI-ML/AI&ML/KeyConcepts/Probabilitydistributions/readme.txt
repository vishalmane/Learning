Probability distributions describe how the values of a random variable are distributed. 
They are fundamental to statistics and are used to model uncertainty and randomness. 
Probability distributions can be discrete or continuous, and each type has its own set of properties and applications.

### Discrete Probability Distributions

1. **Bernoulli Distribution**:
   - Models a single experiment with two possible outcomes: success (1) or failure (0).
   - Parameter: \( p \) (probability of success).
   - Example: Coin flip (success: heads, failure: tails).

   \[
   P(X = x) = p^x (1 - p)^{1 - x} \quad \text{for } x \in \{0, 1\}
   \]

2. **Binomial Distribution**:
   - Models the number of successes in a fixed number of independent Bernoulli trials.
   - Parameters: \( n \) (number of trials), \( p \) (probability of success in each trial).
   - Example: Number of heads in 10 coin flips.

   \[
   P(X = k) = \binom{n}{k} p^k (1 - p)^{n - k} \quad \text{for } k = 0, 1, \ldots, n
   \]

3. **Poisson Distribution**:
   - Models the number of events occurring in a fixed interval of time or space, given the events occur with a known constant rate and independently of the time since the last event.
   - Parameter: \( \lambda \) (average rate of occurrence).
   - Example: Number of emails received in an hour.

   \[
   P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!} \quad \text{for } k = 0, 1, 2, \ldots
   \]

### Continuous Probability Distributions

1. **Uniform Distribution**:
   - Models a random variable that has equal probability in any interval of the same length within its range.
   - Parameters: \( a \) (minimum value), \( b \) (maximum value).
   - Example: Random number between 0 and 1.

   \[
   f(x) = \frac{1}{b - a} \quad \text{for } a \leq x \leq b
   \]

2. **Normal (Gaussian) Distribution**:
   - Models a continuous random variable with a symmetric, bell-shaped curve.
   - Parameters: \( \mu \) (mean), \( \sigma \) (standard deviation).
   - Example: Heights of people.

   \[
   f(x) = \frac{1}{\sigma \sqrt{2 \pi}} e^{-\frac{(x - \mu)^2}{2 \sigma^2}}
   \]

3. **Exponential Distribution**:
   - Models the time between events in a Poisson process.
   - Parameter: \( \lambda \) (rate parameter, inverse of the mean).
   - Example: Time between arrivals of customers at a store.

   \[
   f(x) = \lambda e^{-\lambda x} \quad \text{for } x \geq 0
   \]

4. **Gamma Distribution**:
   - Generalizes the exponential distribution and models the sum of multiple exponentially distributed random variables.
   - Parameters: \( \alpha \) (shape parameter), \( \beta \) (rate parameter).
   - Example: Waiting time for multiple events to occur.

   \[
   f(x) = \frac{\beta^\alpha x^{\alpha - 1} e^{-\beta x}}{\Gamma(\alpha)} \quad \text{for } x \geq 0
   \]

5. **Beta Distribution**:
   - Models random variables limited to intervals of finite length, typically [0, 1].
   - Parameters: \( \alpha \) (shape parameter), \( \beta \) (shape parameter).
   - Example: Proportion of success in a series of experiments.

   \[
   f(x) = \frac{x^{\alpha - 1} (1 - x)^{\beta - 1}}{B(\alpha, \beta)} \quad \text{for } 0 \leq x \leq 1
   \]

### Visualizing Probability Distributions

Visualizing probability distributions can help understand their properties. Below is an example of Python code to visualize some common distributions using Matplotlib and SciPy:

```python
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Plot settings
plt.figure(figsize=(14, 10))

# Uniform Distribution
x = np.linspace(-1, 2, 1000)
plt.subplot(2, 2, 1)
plt.plot(x, stats.uniform.pdf(x, 0, 1), 'b-', label='Uniform')
plt.title('Uniform Distribution')
plt.legend()

# Normal Distribution
x = np.linspace(-5, 5, 1000)
plt.subplot(2, 2, 2)
plt.plot(x, stats.norm.pdf(x, 0, 1), 'r-', label='Normal')
plt.title('Normal Distribution')
plt.legend()

# Exponential Distribution
x = np.linspace(0, 5, 1000)
plt.subplot(2, 2, 3)
plt.plot(x, stats.expon.pdf(x, 1), 'g-', label='Exponential')
plt.title('Exponential Distribution')
plt.legend()

# Poisson Distribution
x = np.arange(0, 20, 1)
plt.subplot(2, 2, 4)
plt.plot(x, stats.poisson.pmf(x, 5), 'k-', label='Poisson')
plt.title('Poisson Distribution')
plt.legend()

plt.tight_layout()
plt.show()
```

This code visualizes the Uniform, Normal, Exponential, and Poisson distributions, illustrating their shapes and characteristics. Understanding these distributions helps in selecting the appropriate models for different types of data and real-world phenomena.