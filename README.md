# Warhammer 40,000 Faction Classification — Exploratory Analysis and Data Preparation

Project Assignments 1 (Exploratory Data Analysis) and 2 (Data Preparation and Feature Engineering) · Machine Learning elective · Universidad de Carabobo, Faculty of Experimental Sciences and Technology (FACYT), Department of Computing.
Authors: Gustavo Herrera, Jeanmarco Alarcón.

## Problem

> *Given the characteristics of a Warhammer 40K unit, predict which faction it belongs to.*

| Item | Definition |
|---|---|
| Unit of observation | One **datasheet** (one row of `Datasheets`, key `datasheet_id`): a playable unit with its model profiles, weapon profiles, costs, keywords and abilities |
| Target | `faction_id` (25 classes). `faction_name` is only its display label; neither is ever a feature |
| Learning problem | Multiclass, single-label classification with strongly imbalanced classes (269 to 4 datasheets) |
| Features | Numeric and mechanical values only (model and weapon statistics, cost, unit size, shared rule keywords, core abilities, role, base). Names and text are never used to predict |
| Deliverables | [`notebooks/01_eda_warhammer.ipynb`](notebooks/01_eda_warhammer.ipynb) (Assignment 1) and [`notebooks/02_data_preparation.ipynb`](notebooks/02_data_preparation.ipynb) (Assignment 2), each executed in order with all outputs visible |

## Data source

- **Dataset:** [*Warhammer 40k* by theredmage on Kaggle](https://www.kaggle.com/datasets/theredmage/warhammer-40k), **version 5**.
- **Origin:** 19 CSV files exported from [Wahapedia](https://wahapedia.ru/wh40k10ed/) on **2025-10-03 20:47:58** (`Last_Update.csv`).
- **In this repository:** the 19 files are included **unchanged** in [`data/raw/`](data/raw/), exactly as unzipped from the Kaggle download. They are the canonical input and are never modified. [`.gitattributes`](.gitattributes) stores them byte for byte, so their checksums are the same on every operating system.
- **Licence and use:** the game content belongs to Games Workshop and the export is published by Wahapedia. The data are used here for academic purposes only.

The notebook verifies every file before using it (SHA-256, exact header, number of rows) and **stops if anything differs**. The expected checksums are:

| File (`Wahapedia Data Export - <name>.csv`) | SHA-256 |
|---|---|
| Abilities | `cc82bdfd06aa0174e58e4052f3110c865fecfa7fce7fc6b34bbc251fbd71916d` |
| Datasheets | `c029e088ac3ea699f18e1820309e2af421380d8b527c1dda0c40fbcd8fdc67b4` |
| Detachment_Abilities | `32355f9d0d7657e32fbc37e22d5729196ffd32a7b57cd34978d958a37521d014` |
| DS_Abilities | `3844304cdab463292b9a6f10d816697ccb54a5cccfe12dec6a60f58b340d4cc4` |
| DS_Detachment Abilities | `9e8bcff7847319b06197ccddf4c91dd99ce257ccf638078245a8a4c05ee3442c` |
| DS_enhancements | `018b767e4de616e80c34ed8a0d1ef4f312a5922765db3ccc3d8a4af673a4d379` |
| DS_Keywords | `fab6567a3d4390c562c41ea286051b0c7d5fbfb8c04ca34d5a74f21cb60c2c5b` |
| DS_Leader | `97d79c860c128eb615455619f23f97e7f0020e6278aed3ba4a32f32ebaa99fbc` |
| DS_Model Costs | `6bf975f20c912e6f08cc3489f7e113bf355e792a88613d65ff2012c17b8d355d` |
| DS_Models | `a63228898859243f88112a89b1d7bb6ba4447d2961e6d1c2bef3620288f96ee8` |
| DS_Options | `4d80019626096975d97792c799e55b33033c3101f59d701dec33dcc1807477f7` |
| DS_Stratagems | `7aa7b482d57d1062758a04c2249152c5a2e302878d77dc930a6b0b41279dcbf9` |
| DS_Unit Comp | `cef285ffd61c73fe963ba41abefb937850bbd8469b7c2ce2694f1955eddbbcb7` |
| DS_Wargear | `07a24bc5b59da7ac8ef821ce4ef7e36e65cdb6c576e4855e545b9cdcad7a4472` |
| Enhacements | `925bb98feab054190816f97bdff94c73fac7a9934e72e7024ac26e4645813cdf` |
| Factions | `178f535e8bb871f3f76b4fdfdd2df4d22ce3afd8e60e0452be41a7025d0d1a39` |
| Last_Update | `0bd9408d6616a8c03a5226440a1f4e0a5734ba0be84722792a6ddf01c9148778` |
| Sources | `c105d64b1ac3a75d649f8ddf7b579de24555e54f35f4d9b9ec01499235732985` |
| Stratagems | `f11be03e14c074ff24642bf39858c3264d365ab35240b78d768f84065b7f0a41` |

## Requirements

- **Python 3.14** (tested with 3.14.6).
- The packages pinned in [`requirements.txt`](requirements.txt): pandas, numpy, matplotlib, seaborn, scipy, scikit-learn, and ipykernel, nbformat and nbconvert to execute the notebook.

```bash
git clone https://github.com/JeanJedsonn/EDA_V2.git
cd EDA_V2
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

From the repository root:

```bash
cd notebooks
python -m nbconvert --to notebook --execute --inplace 01_eda_warhammer.ipynb
python -m nbconvert --to notebook --execute --inplace 02_data_preparation.ipynb
```

Alternatively, open a notebook in Jupyter or VS Code and use **Restart Kernel → Run All**. Paths are resolved relative to the notebook folder, so the data are found without any configuration. **The two notebooks are independent:** each one reads `data/raw/` itself, neither uses variables or files produced by the other, and they can be run in any order.

| Notebook | Each run | Time on the test machine |
|---|---|---|
| `01_eda_warhammer.ipynb` | verifies the 19 CSV files; rebuilds `artifacts/warhammer_raw.db` and `artifacts/warhammer_clean.db` from scratch (the folder is created if it does not exist); executes the whole analysis | about 45 s |
| `02_data_preparation.ipynb` | verifies the 9 CSV files it reads; rebuilds the table of 1,350 datasheets and checks it against the exploratory analysis; splits train and test; fits the preparation pipeline on the training rows only. **It writes nothing to disk** | about 10 s |

The executed notebooks in the repository already contain every output, so they can be read without running them.

## Repository structure

```text
EDA_V2/
├── data/
│   └── raw/                      # input: the 19 CSV files of the Kaggle export (canonical, immutable, versioned)
├── notebooks/
│   ├── 01_eda_warhammer.ipynb    # Assignment 1: builds the databases and runs the whole EDA
│   └── 02_data_preparation.ipynb # Assignment 2: validation, train/test split, features and preprocessing pipeline
├── artifacts/                    # generated on every run (not versioned)
│   ├── warhammer_raw.db
│   └── warhammer_clean.db
├── requirements.txt              # pinned dependencies
├── .gitattributes                # keeps data/raw byte for byte
└── README.md
```

| File | Kind | Produced by | Versioned |
|---|---|---|---|
| `data/raw/*.csv` | input (canonical source) | Kaggle download, unchanged | yes |
| `artifacts/warhammer_raw.db` | generated | notebook, §4.1 | no (rebuilt on every run) |
| `artifacts/warhammer_clean.db` | generated | notebook, §4.6, built only from the raw database | no (rebuilt on every run) |
| `notebooks/01_eda_warhammer.ipynb` | code and results | — | yes (with outputs) |
| `notebooks/02_data_preparation.ipynb` | code and results | — | yes (with outputs) |

## Pipeline and lineage

```text
data/raw/  (19 CSV, SHA-256 verified)
   └─ §4.1  warhammer_raw.db     one table per file, every value as text, exactly as in the CSV; load_manifest table
        │                        (attached read-only to the clean database: the analysis cannot modify it)
        ├─ §4.2  one documented decision for each of the 110 raw columns (kept, renamed or removed)
        ├─ §4.3  referential integrity: orphan rows counted (134 weapons, 124 stratagem links)
        ├─ §4.4  reading check: values that a type-guessing reader would alter (N/A, +N, None)
        ├─ §4.5  parsers with a status (dice expressions, thresholds, movement, bases, costs)
        └─ §4.6  warhammer_clean.db  8 tables with their original names, abbreviations renamed to full names,
                                     9 derived columns, foreign keys enforced
              └─ TEMP working tables of the session (parsed characteristics, never written to a file)
                    └─ §4.7  datasheet_features: 1,350 rows, one per datasheet (unique index)
```

**Contents of `warhammer_clean.db`:**
- **Tables:** `Factions` (25 rows), `Datasheets` (1,351), `DS_Models` (1,425), `DS_Wargear` (6,652), `DS_Model_Costs` (1,706), `DS_Keywords` (5,727), `Abilities` (11) and `DS_Abilities` (1,675).
- **Added columns:**
  - `DS_Models`: `base_area`, `is_flying_base` and `kw_FLY`;
  - `DS_Wargear`: `attacks_mean`, `strength_mean` and `damage_mean`, the expected value of each dice expression, n·(k+1)/2 + c;
  - `DS_Model_Costs`: `total_models` and `cost_per_model`;
  - `DS_Abilities`: `parameter_mean`.
- **Rows that are not loaded:**
  - the 134 orphan weapons;
  - 285 empty duplicate datasheets (copies of shared units whose weapons are stored on another copy), with all their child rows;
  - abilities other than Core;
  - keywords present in a single faction (the universality filter).

**What makes the build fail** (an exception, never a warning):
- a missing file, a wrong checksum, header or row count;
- a raw column without a decision, or a stored table or column that differs from the decisions;
- an orphan count that differs from the expected one;
- a foreign-key violation;
- an unparsed characteristic;
- a duplicated `datasheet_id`;
- an identifier or target alias in `X`.

## Data preparation (notebook 02)

```text
data/raw/ (9 of the 19 CSV, SHA-256 verified, read as text)
   └─ §5  row filters without the target (134 orphan weapons, 285 empty duplicates, 1 internal page)
          parsers with a status; one row per datasheet (1,350), checked against the exploratory analysis
          GroupId: related datasheets (same name or identical profiles), 1,207 groups
   └─ §6  grouped and stratified hold-out on GroupId (StratifiedGroupKFold, 4 folds, seed 42): 1,012 train / 338 test
   └─ §7–10  Pipeline, fitted on the training rows only:
          add_mechanical_features (FunctionTransformer): logs, points per Wound, melee share, spreads, indicators, can fly
          ColumnTransformer: numeric → median imputation + scaling · binary → most frequent · role → one-hot
                             keywords → KeywordEncoder (vocabulary learned in fit: keywords in ≥ 2 training factions,
                             without allegiance or unit-name keywords)
          RedundancyFilter: drops binary columns that repeat an earlier one, learned in each fit
   └─ §11  structural checks: 118 numeric columns, no missing or infinite values, input unchanged, reproducible fit
```

Columns that would reveal the faction are excluded before the pipeline: identifiers, names, faction and allegiance keywords, faction abilities and the price context of a cost row (its text names the Imperial Agents). No model is trained and no hyperparameter is tuned; the test set is not transformed. Section 12 of the notebook lists the hypotheses and the objects for the modelling notebook.

## Reproducibility

- **Random seed:** `RANDOM_STATE = 42` for every stochastic step (bootstrap intervals, train/test split, validation folds).
- **Clean runs:** each notebook is executed top to bottom; its execution counts are sequential and there are no errors or warnings. No warning filter is used: in notebook 02 the number of folds is set by the smallest faction (4 datasheets: 4 hold-out folds, 3 inner folds), so every class fits in every fold.
- **Automated checks:** there is no separate test suite. The checks listed above run inside the notebooks on every execution, so the `nbconvert --execute` command doubles as the automated build-and-validate test: it exits with an error if any check fails.
