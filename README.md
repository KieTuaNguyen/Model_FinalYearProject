# Vietnamese E-commerce Feedback Analysis Model

## Contact
For technical questions or support, please contact:
- Kiet Nguyen
- [WhatsApp](https://wa.me/84914852966)

## Introduction
This repository contains an advanced Aspect-Based Sentiment Analysis (ABSA) model specifically designed for Vietnamese e-commerce feedback analysis. The model employs state-of-the-art natural language processing techniques to extract meaningful insights from customer reviews, enabling granular understanding of product and service sentiment.

## Model Architecture

### Processing Pipeline

```mermaid
graph LR
    A[Import Feedback Data] --> B[Pre-Processing]
    B --> C[ABSA Modeling]

    subgraph "Pre-Processing"
    direction TB
    B1[Extract Columns] --> B2[Tokenize]
    B2 --> B3[Clean Data]
    B3 --> B4[Export JSON]
    end

    subgraph "ABSA Modeling"
    direction TB
    C1[Manual Labeling] --> C2[Train Model]
    C2 --> C3[Model Application]
    C3 --> C4[Extract Aspects]
    C4 --> C5[Determine Polarity]
    end

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef process fill:#d4e6f1,stroke:#2874a6,stroke-width:2px;
    
    class A,B,C default;
    class B1,B2,B3,B4,C1,C2,C3,C4,C5 process;
```

### Sentiment Analysis Flow

```mermaid
graph TD
    A[Input Text] --> B[Aspect Extraction]
    B --> C[Context Window]
    C --> D[Sentiment Analysis]
    D --> E[Polarity Score]
    
    subgraph "Aspect Categories"
    F[Về Sản Phẩm]
    G[Về Dịch Vụ]
    end
    
    subgraph "Sentiment Classes"
    H[POS]
    I[NEU]
    J[NEG]
    end

    classDef categories fill:#d5f5e3,stroke:#196f3d,stroke-width:2px;
    classDef sentiment fill:#f5cba7,stroke:#a04000,stroke-width:2px;
    
    class F,G categories;
    class H,I,J sentiment;
```

## Implementation Details

### 1. Data Processing
Our model implements sophisticated text processing:
- Vietnamese-specific tokenization
- Context window extraction
- Noise removal and normalization
- Special character handling

### 2. Aspect Extraction
The system uses a two-stage approach:

```mermaid
graph TD
    A[Input Text] --> B[Category Detection]
    B --> C[Term Extraction]
    C --> D[Context Analysis]
    D --> E[Polarity Assessment]
    
    subgraph "Training Process"
    F[Manual Labeling]
    G[Model Training]
    H[Validation]
    end
    
    F --> G --> H

    classDef process fill:#d4e6f1,stroke:#2874a6,stroke-width:2px;
    class A,B,C,D,E process;
```

### 3. Model Components

#### Dataset Characteristics
- Total size: 22,000 records
- Development set: 4,400 records (20%)
- Training set: 1,100 records manually labeled

#### Training Approach
- Initial manual labeling of seed dataset
- Model training on labeled data
- Iterative refinement process
- Performance validation

## Repository Structure
```
MODEL_FLEXIBOARD/
├── document/              # Technical documentation
├── vincorenpl/            # Core NLP components
│   ├── checkpoint-30800/  # Model checkpoints
│   └── sample_data/       # Training samples
├── warehouse/             # Processed data
└── inference.py           # Model inference
```

## Example Output

```json
{
  "Content": "Màn hình rất tốt, loa rất hay nhưng giao hàng chậm",
  "Aspects": [
    {
      "Category": "Về Sản Phẩm",
      "Term": "màn hình",
      "Polarity": "POS",
      "Confidence": 0.95
    },
    {
      "Category": "Về Dịch Vụ",
      "Term": "giao hàng",
      "Polarity": "NEG",
      "Confidence": 0.78
    }
  ]
}
```

## Important Note
This model has been developed and trained by Kiet Nguyen for educational purposes. The training data and pre-trained models are intended for academic use only and should not be used for commercial purposes without proper authorization.

## License
This project is licensed under the MIT License - see the LICENSE file for details.