
# 🧠 Models

Source code for generating models to predict data features in a standardized way.

---

## 📋 Table of Contents
- [🧠 Models](#-models)
  - [📋 Table of Contents](#-table-of-contents)
  - [📖 Introduction](#-introduction)
  - [🛠️ How to Create a Model](#️-how-to-create-a-model)
    - [1. Directory Setup](#1-directory-setup)
    - [2. Recommended Structure](#2-recommended-structure)
    - [3. Data Access](#3-data-access)
    - [4. Artifact Management](#4-artifact-management)
    - [5. Standardized Inference](#5-standardized-inference)
  - [🚀 Workflow](#-workflow)

---

## 📖 Introduction
This directory serves as the central hub for all predictive modeling within the project. By following a standardized approach, we ensure that models are reproducible, easy to integrate, and well-documented.

---

## 🛠️ How to Create a Model
To maintain consistency, follow these steps when developing a new model:

### 1. Directory Setup
Each model should have its own subdirectory within `models/`. Use a descriptive name (e.g., lowercase, underscores).

```bash
mkdir models/my_new_model
```

### 2. Recommended Structure
A standardized model directory should ideally contain:
- **`train.py`** (or `.ipynb`): Logic to train the model using datasets from the `data/` directory.
- **`predict.py`**: Module to run inference on new data.
- **`README.md`**: Model-specific documentation (purpose, hyperparameters, performance).
- **`weights/`**: Directory for model artifacts (see [Artifact Management](#4-artifact-management)).

### 3. Data Access
Always reference data using relative paths or the `datpy` utility. Avoid hardcoding absolute paths.

```python
import pandas as pd
# Load data relative to the project structure
data = pd.read_csv("../../data/raw/my_dataset.csv")
```

### 4. Artifact Management
Trained model files (e.g., `.pkl`, `.h5`, `.pt`) require careful handling:
- **Small files**: Can be stored in `models/my_new_model/weights/`.
- **Large files**: Should be tracked via **DVC** or stored in a shared filesystem. Document the external location in the model's local `README.md`.

### 5. Standardized Inference
Ideally, every model should output results to a standardized location like `metadata/` or `results/` to facilitate downstream analysis.

---

## 🚀 Workflow
1.  **Prototype**: Develop and experiment in the [sandbox/](../sandbox/) directory.
2.  **Standardize**: Once a model architecture is finalized, move the logic to a dedicated folder in `models/`.
3.  **Document**: Update the local `README.md` with performance metrics and specific usage instructions.


