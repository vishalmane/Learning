Types of Data
    Quantitative Data (Numerical)
        Discrete
            Countable numbers.
                Example:
                Number of patients
                Number of claims
        Continuous
            Measured values.
                Example:
                    Blood pressure
                    Weight
                    Revenue
                Architect Relevance:
                    Used in ML models
                    Needs normalization
    Qualitative Data (Categorical)
        Nominal
            No order.
            Example:
                Gender
                City
                Diagnosis code
        Ordinal
            Has order.
            Example:
                Severity level (Low, Medium, High)
                Rating (1–5)
            Architect Relevance:
                Needs encoding for ML
                Impacts feature engineering

Data Distribution
    How values of a variable are spread across a range.
    It tells you:
        Where most values lie
        How spread out they are
        Whether extreme values exist
        Whether data is symmetric or skewed
    Why Distribution Matters for AI Architects
        Model selection
        Feature engineering
        Normalization strategy
        Outlier handling
        Bias detection
        Drift detection in production
    Normal Distribution - Also called Bell Curve.
        Symmetric
        Mean = Median = Mode
        Most values near center
        Tails decrease evenly
        If your data is not normal → model performance degrades.

    Skewed Distribution
        Right Skew (Positive Skew)
            Long tail on right
            Few very large values
            Mean > Median
            Outliers pull average up
            Needs log transformation
        Left Skew (Negative Skew)
            Long tail on left
            Few very small values

    Uniform Distribution- 
            All values equally likely.
            Rare in real-world business data.
            Used in:
            Simulations
            Random generators
    Bimodal / Multimodal Distribution
        Two or more peaks.
        Example:
        Mixed population (children + adults height)
        Two types of customers
        Architect Insight:
        This might mean:
            Hidden segmentation
            You should split dataset
            Multiple models required

    Exponential Distribution
        Heavily right-skewed.
    Poisson Distribution
        Used for count data.
        Example:
            Number of claims per day
            Number of patient visits
            Number of fraud incidents
        Used in:
        Event modeling
        Risk prediction

    Power Law Distribution (Very Important in Real Systems)
        Few very large values, many small ones.
        Example:
            20% customers generate 80% revenue
            Few providers generate most claims
            Social network connections
        Architect Insight:
            Heavy-tail systems need special scaling
            Fraud often hides in tails
    How to Check Distribution Practically
        Histogram
        Boxplot
        KDE plot
        Q-Q plot

Feature Engineering
    Models don’t create intelligence.
    Features do.
    Feature Engineering is about shaping data for learning.
    The process of transforming raw data into meaningful inputs (features) that improve model performance.

    Why Feature Engineering Matters (Architect View)
        Determines model accuracy more than algorithm choice
        Reduces bias
        Improves interpretability
        Reduces overfitting
        Impacts latency & cost
        Enables model explainability (important for healthcare)

    Feature Creation
    Feature Transformation
    Encoding Categorical Variables
    Handling Missing Values
    Feature Selection
    Time-Based Features
    Text Feature Engineering (Important for LLM future)

    Feature Engineering Pipeline (Enterprise Architecture)
        Raw Data
        ↓
        Validation
        ↓
        Cleaning
        ↓
        Transformation
        ↓
        Feature Store
        ↓
        Model

Probability & Statistics for ML
    Random Variables
        A random variable is a numerical representation of an uncertain event.

            Example:
            X = number of claims per day
            Y = patient risk score
            Z = next predicted token

            Two types:
            🔹 Discrete Random Variable
                Takes countable values.
                Example: number of fraud cases.

            🔹 Continuous Random Variable
                Takes values in a range.
                Example: blood pressure.

    Probability Distributions
        A distribution tells us: How likely each value of a random variable is.
        Bernoulli Distribution
        Gaussian (Normal) Distribution
        Categorical Distribution
        Multinomial Distribution

        Loss functions depend on assumed distribution.

    Conditional Probability
        Conditional probability means: P(A∣B)
        Probability of A given B happened.
        Probability of A happening given that B has already happened
            In LLMs: P(next word∣previous words)
            Language models are fully based on conditional probability.
            Example:
                P(Rain ∣ Cloudy)
                Given that the sky is cloudy, what’s the probability it rains?
                P("insurance" | "healthcare claim")
            Every predictive model is estimating: P(Y∣X)
    
    Bayes Theorem
        Bayes’ Theorem is used for updating probabilities when new evidence appears
        “Given that I observed B, what is the probability that A is true?”
            P(A | B) = (P(B | A) * P(A)) / P(B)
        Reverse conditional probability using known information.
        I already know B happened. What fraction of those cases have A?
        If it is raining, how likely is it cloudy?

        Why It Matters in AI
            Spam detection
            Risk modeling
            Uncertainty estimation
            Bayesian neural networks
            Model confidence calibration


Training a model = Finding parameter values that minimize prediction error.
We want to find weights θ that minimize: Loss(θ)

Loss Functions: A loss function measures how wrong the model is.

MSE (Mean Squared Error)  
            MSE=n1​∑(ytrue​−ypred​)2
    What it does:
        Penalizes large errors more.
        Assumes Gaussian noise.
        Smooth and differentiable.

        Example:
            Predict hospital bill:
            True = 10000
            Predicted = 9000

            Error = 1000
            Squared error = 1,000,000

            Large mistakes hurt more.

Cross-Entropy Loss:  Used for classification and LLMs.
    For classification: 
                    Loss=−∑ylog(p)
    For GPT:            
                    Loss=−logP(correct token)
        What it does:

        Penalizes confident wrong predictions heavily.
        Derived from Maximum Likelihood Estimation.

        Example (LLM):
                Model predicts:
                P("insurance") = 0.9
                True word = "insurance"
                Loss = -log(0.9) = small

                If wrong:
                P("insurance") = 0.01
                Loss = -log(0.01) = huge

                This forces model to adjust strongly.

Gradient Descent: To minimize loss. Move in the direction of steepest decrease.

        Gradient tells:
            "If you move weights slightly this way, loss decreases fastest."
            So we repeatedly:
                Compute loss
                Compute gradient
                Update weights
                This is training.

Stochastic Gradient Descent (SGD)
    Full Gradient Descent:
        Uses entire dataset to compute gradient.
        Very slow for large data.
    SGD:
        Uses ONE sample at a time.
        Faster.
        Noisy updates
        Noise prevents getting stuck in shallow local minima.

Mini-Batch Training
    Compromise between full batch and SGD.
    Use small batch (e.g., 32, 128 samples).
    Advantages:
        Faster than full batch
        More stable than SGD
        Parallelizable on GPU
        This is standard in deep learning.

Learning Rate (α)
    Learning rate controls step size.
    Too small:
        Very slow training.
    Too large:
        Overshoots minimum.
        Diverges.
        Training unstable.

    Fine-tuning requires small learning rate because:
        Large pretrained models already near good minimum.
    Large learning rate:
        → destroys pretrained knowledge
        → catastrophic forgetting

Vanishing / Exploding Gradients
    This is critical in deep networks.

    Vanishing Gradient
        Gradients become extremely small.
        Weights barely update.
        Training stalls.
        
        Common in:
            Deep networks
            Sigmoid/tanh activations

    Exploding Gradient
        Gradients become huge.
        Weights jump wildly.
        Loss becomes NaN.

Adam Optimizer (Conceptual)
    Adam = Adaptive Moment Estimation
    Instead of using same learning rate for all parameters:
    Adam:
        Tracks moving average of gradients
        Tracks squared gradients
        Adjusts learning rate per parameter
    Benefits:
        Faster convergence
        Stable training
        Default in most deep learning frameworks
    Used in GPT training.

Why Training Becomes Unstable
    1️⃣ Learning rate too high
    2️⃣ Poor initialization
    3️⃣ Exploding gradients
    4️⃣ Data distribution shift
    5️⃣ Batch size too small
    6️⃣ Bad loss scaling
    7️⃣ Mixed precision errors

Why Model Convergence Fails

Convergence fails when:
    Loss oscillates wildly
    Loss increases instead of decreases
    Gets stuck in saddle point
    Gradient becomes zero

Large LLMs use:
    Learning rate warmup
    Gradient clipping
    Layer normalization
    Weight decay
    AdamW optimizer

Loss function → defines objective
Gradient → tells direction
Learning rate → controls speed
Optimizer → controls stability
Batch size → controls noise

Training = Controlled descent in high-dimensional space.


What is Bias–Variance Tradeoff?

When a model makes predictions, the total prediction error comes from three sources:

Error=Bias^2 + Variance + Irreducible Noise

Bias: Error due to wrong assumptions in the model.
Variance: Error due to model sensitivity to training data.
Noise: Random error in the data (cannot be removed).

Bias:
Bias measures how far the model’s predictions are from the true relationship.

High bias means:
    Model is too simple
    Cannot capture real patterns

Example:
    Predicting house price using only:
        Price = constant average price
        The model ignores features like:
            size
            location
            age
        This creates systematic error.

Variance: 
Variance measures how much the model changes when training data changes.

High variance means:
    Model memorizes training data
    Small data changes → large prediction changes
Example:
    Imagine training a model on 10 patients.
    If one patient is removed:
        predictions change drastically
        That means high variance.

Underfitting vs Overfitting
Underfitting
    Model too simple.
    Symptoms:
        High training error
        High test error
    Example:
        Linear model trying to fit nonlinear data.
    High bias.

Overfitting
    Model too complex.
    Symptoms:
        Very low training error
        High test error
    Example:
        Model memorizes training dataset.
    High variance.

Model Capacity
    Capacity = model’s ability to learn complex patterns.
    Examples:
        Low capacity:
            Linear regression
        Medium capacity:
            Random forest
        Very high capacity:
            Deep neural networks
            Transformers


Regularization
    Regularization prevents models from becoming too complex.
    It penalizes large weights.

L2 Regularization (Ridge)
    Adds penalty:
        Loss=original loss+λ∑w^2
    Effect:
        discourages large weights
        smooths model
    Used widely in neural networks.

L1 Regularization (Lasso)
    Penalty:
        Loss=original loss+λ∑∣w∣
    Effect:
        pushes some weights to zero
        performs feature selection
    Useful for sparse models.

Dropout
    Dropout randomly disables neurons during training.
    Example:
        Network with 100 neurons
        Each iteration → randomly deactivate ~50 neurons.
    Effect:
        prevents co-adaptation
        forces network to learn robust features
        You can think of dropout as training many smaller networks simultaneously.
    This reduces variance.

Early Stopping
    Training too long can cause overfitting.
    Early stopping monitors validation loss.
    When validation error starts increasing → stop training.
    Effect:
        prevents model from memorizing noise.

Model Capacity vs Dataset Size
This is an important architectural concept.

    Small dataset + big model→ Overfitting risk.
    Large dataset + big model→ Works well.
    Example:
        Training GPT-like model on:
            1 million sentences → overfit
            1 trillion tokens → generalize

Neural Network Architecture
    Input Layer → Hidden Layers → Output Layer
    Patient Age, Income, Claim Amount
        ↓
     Hidden Layer
        ↓
     Hidden Layer
        ↓
    Fraud Probability

    Each neuron performs: y=activation(w⋅x+b)
        Where:
            x = input
            w = weight            
            b = bias
            activation = nonlinear function

Activation Functions
    Activation functions introduce non-linearity into neural networks.
    Without them, the network would behave like simple linear regression.

Common Activation Functions

ReLU (Most Common)
    ReLU(x)=max(0,x)
    Graph:
        negative values → 0
        positive values → unchanged
    Why used:
        simple
        avoids vanishing gradients
        computationally efficient

Sigmoid
        $$
        \sigma(x) = \frac{1}{1 + e^{-x}}
        $$
        Range: 0 to 1
        Used for:
            binary classification
        Problem:
            causes vanishing gradients.

Tanh

        Range:
        -1 to 1

        Better than sigmoid but still suffers gradient problems.

Backpropagation
    Backpropagation is the algorithm used to train neural networks.
    It calculates how much each weight contributed to the error.
    Then adjusts weights to reduce the error.
    
    How it works (conceptually)
    Step 1: Forward pass
        Input → prediction
    Step 2: Compute loss
    Step 3: Backward pass
        Compute gradient of loss with respect to each weight.
    Step 4: Update weights using gradient descent
        
$$
        w = w - \alpha \frac{\partial Loss}{\partial w}
$$

What is a Transformer
    A Transformer is a neural network architecture designed to process sequences of data (like text).
    Goal: Predict next token given previous tokens
    Example:
        Input:  "The doctor prescribed"
        Output: "medicine"
    Unlike older models (RNN/LSTM), Transformers process all words in parallel using attention.

How a Transformer Processes a Sentence
    "The patient has diabetes"
    Text
    ↓
    Tokenization
    ↓
    Embeddings
    ↓
    Positional Encoding
    ↓
    Transformer Layers
        • Self-Attention
        • Feed Forward
        • Residual + LayerNorm
    ↓
    Output probabilities
    ↓
    Next token prediction

    Tokenization : Tokenization converts text into tokens (numerical IDs).
        "The patient has diabetes"
        ↓
        ["The", "patient", "has", "diabetes"]
        ↓
        [512, 8231, 67, 19284]
    
    Embeddings: Embeddings convert token IDs into dense vectors.
        An embedding is a numerical vector that represents the meaning of text, image, or other data.
        token = "doctor"\
        ↓
        Embedding vector:[0.21, -0.77, 0.12, 0.98, ...]
        ↓
        Typical dimension: 768
                        1024
                        4096
        Embeddings capture semantic meaning.
        doctor – hospital ≈ teacher – school
        So similar words appear close in vector space.
        This allows models to understand meaning.

    Positional Encoding: 
        Transformers process tokens in parallel.
        But language requires word order.
        Example:
            "dog bites man"
            "man bites dog"
        Same words → different meaning.
        So transformers add position information.
        Example:
            Embedding(word) + Position Encoding
            Positional encoding injects information like:
                token1 → position 1
                token2 → position 2
    
    Self-Attention (Core Idea)
        This is the heart of transformers.
        Self-attention lets each word look at other words in the sentence.
        
        Example sentence:
            "The patient took medicine because he was sick"
            When processing "he", the model should attend to "patient".
        Self-attention learns this relationship.

        How It Works
        Each token creates three vectors:
            Query (Q): Query → what I am looking for
            Key (K): Key → what I contain
            Value (V): Value → information to pass

            Words with high similarity → stronger attention.
            "The cat sat on the mat"
                | Word | Attention Weight |
                | ---- | ---------------- |
                | The  | 0.05             |
                | cat  | 0.40             |
                | sat  | 0.15             |
                | on   | 0.15             |
                | the  | 0.05             |
                | mat  | 0.20             |

            Because “cat sat” has strong meaning.

    Multi-Head Attention
        Instead of one attention calculation, the model uses multiple attention heads.
        Example:
            Head 1 → grammatical relation
            Head 2 → semantic meaning
            Head 3 → long-range dependency
            Head 4 → subject-object relation
        Different heads capture different relationships.
        "The cat sat on the mat"
            | Head   | Focus                   |
            | ------ | ----------------------- |
            | Head 1 | cat ↔ sat               |
            | Head 2 | sat ↔ mat               |
            | Head 3 | sat ↔ on                |
            | Head 4 | global sentence meaning |

    
    Feed-Forward Layers
        After attention, each token passes through a small neural network.
            Linear
            ↓
            ReLU / GELU activation
            ↓
            Linear
        Adds nonlinear transformation.
        Allows model to learn complex patterns.

    Residual Connections
        Deep networks suffer from training problems.
        Residual connections fix this.

Autoregressive Generation
    LLMs generate text token by token.

    Input: "The doctor prescribed"
    ↓
    Predict next token
    ↓
    "medicine"
    ↓
    Append to sentence
    ↓
    Predict next token again

    Sequence grows gradually.
    This is called autoregressive generation.

What a Transformer Layer Looks Like
    Input embeddings
    ↓
    Multi-head self-attention
    ↓
    Add & LayerNorm
    ↓
    Feed-forward network
    ↓
    Add & LayerNorm
    ↓
    Output

Tokenization → text → numbers
Embeddings → meaning vectors
Attention → understand relationships
Feed-forward → learn patterns
Decoder → generate text sequentially

Vector Space Representation
    In embeddings, each sentence becomes a point in a high-dimensional space.
    Imagine a simplified 2D example:
                    animal
                    ↑
        dog        cat                  car
            \      /
            \    /
            pet
    cat and dog are close
    car is far away


Semantic Similarity
    Two pieces of text with similar meaning have similar embeddings.
    "The dog is barking"
    "The dog is making noise"
    Embedding vectors will be very close.

Dimensionality
    Embeddings usually have hundreds or thousands of dimensions.
    Why so many?
        Because language meaning is complex.
        Dimensions capture different aspects: (Not exactly like this, but conceptually.)
            dimension 1 → animals
            dimension 2 → emotions
            dimension 3 → location
            dimension 4 → time
        More dimensions → richer semantic representation.

Use Case 1 - RAG (Retrieval Augmented Generation)
RAG systems use embeddings to retrieve relevant documents.
    User Question
        ↓
    Convert to embedding
        ↓
    Search vector database
        ↓
    Retrieve similar documents
        ↓
    Send context to LLM
        ↓
    Generate answer

Use Case 2 — Semantic Search
Use Case 3 — Recommendation Systems
Use Case 4 — Document Clustering

Vector Databases
Embeddings are stored in vector databases.
Popular systems:
        FAISS
        Pinecone
        Weaviate
        Chroma


How GPT Works

        Text
        ↓
        Tokenization
        ↓
        Embeddings
        ↓
        Positional Encoding
        ↓
        Transformer Layers
        ↓
        Attention
        ↓
        Logits
        ↓
        Softmax
        ↓
        Token Selection
        ↓
        Append
        ↓
        Repeat

    Text           --- "The doctor prescribed"
    → Tokenization --- ["The", "doctor", "prescribed"]
    → Embeddings   --- Each token ID is converted into a vector.
                        "The" → [0.12, -0.33, ...]
                        "doctor" → [0.91, 0.02, ...]
    → Positional Encoding
                    --- Transformers don’t know word order.
                        "The" + position 1
                        "doctor" + position 2\
                        Why it matters -> Without this: "dog bites man" = "man bites dog"
    → Transformer Layers (Attention)
                    --- This is the main computation engine.
                        Layer 1
                        Layer 2
                        ...
                        Layer N (50–100+ layers)
                    Each layer contains:
                        Self-Attention
                            "The doctor prescribed medicine because he..."
                             Word "he" attends to: → "doctor"
                        Feed Forward
                        Residual + LayerNorm
    → Logits(Raw Output)
                    --- logits = raw scores for each token
                            medicine → 5.2
                            tablet → 4.8
                            car → -2.1
                        These are NOT probabilities yet.
    → Softmax
                    --- Convert logits into probabilities:
                        medicine → 0.65
                        tablet → 0.30
                        car → 0.001
    → Next Token Prediction
                    --- Model picks next token based on probabilities.
                        "The doctor prescribed medicine"
    → Decoding
                    --- This is where behavior changes significantly.
                        Greedy Decoding: Pick highest probability.
                            Always choose: medicine
                        Sampling: Randomly sample based on probability.
                            medicine (65%)
                            tablet (30%)
                        Temperature: Controls randomness.
                        Top-k Sampling: Pick from top k tokens.
                                        top 3 tokens only
    Autoregressive Loop
        GPT repeats this process:
            Predict next token
            → append to input
            → repeat
        The doctor prescribed
            → medicine
            → for
            → the
            → patient