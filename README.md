# Compatibility Website

## Tech stack

- Python (3.10 encouraged)
- React/TypeScript/Styled Components

## Setup

- Install Python dependencies:
```sh
pip3 install -r requirements.txt
```

- Install `pre-commit` hooks:
```sh
pre-commit install
```

- Install npm dependencies:
```sh
npm i
```

- Run tests:
```sh
npm test
```

- Start the dev server:
```
npm start
```

## Style checks

We use ESLint and Ruff to check style for TypeScript and Python respectively. If `eslint` isn't available on the terminal, use `npm i -g eslint` to install it. Then, check for style issues:

```sh
npm run lint  # Or eslint . --fix
ruff check . --fix
```

## Documentation

### Setup

You will need to set up Vertex AI. To do this, first install the `gcloud` CLI tool, and run
```
gcloud auth login
gcloud auth application-default login
```

On Google VMs such as GCE, this shouldn't be necessary and will "just work". Set up a `.env` file:
```
PROJECT_ID=<your-project-id>
REGION=us-central1 <or any other>
EMBEDDING_MODEL=textembedding-gecko@003 <recommended>
```

### For users

If you want to create your own questionnaire, you need to create a `schema.json` file. The structure is explained below.

```json
{
    "version": "1.0.0",
    "questions": [
        ...questions
    ]
}
```

Each of the `...questions` must be a JSON object, with `display`, `key`, `type`, and `match` keys.

* `display`: The question that is displayed.
* `key`: The key that in the resulting JSON.
* `type`: The type of answer expected. Must be one of: `string`, `int`, `float`, or `enum`. If it is either `int` or `float`, a `range` key must also be present in the JSON object, with a JSON object as value. This object must have `min` and `max` keys. If `type` is `enum`, an `enum` key must be present that maps to valid `enum` values.
* `match`: The match operator. This is the brains of the system. This may be `null`, in which case the answer is ignored. The general structure of this is below:

```json
{
    "type": "comparator",
    "comparator": {
        ...options
    },
    "postprocess": {
        "type": "operator",
        "operator": {
            ...options
        }
    },
    "merge": {
        "type": "merger",
        "merger": {
            ...options
        }
    }
}
```

The `type` key specifies the type of comparator to use. Currently, the following are supported:
* `in_range`: Returns 1 if the value is in the range, and 0 otherwise. Can only be used with `int` and `float` answers. It takes `min` and `max` as options.
* `fuzzy_match`: Embeds the answer and references using an autoencoding model, and computes the maximum distance. It takes an array called `reference` as options.
* `llm_proximity`: Queries an LLM on the distance to a reference point. This by definition does not return a stable value, and should be used sparingly. It takes a string called `query`, which should be a question posed to an LLM, as options. You can use the answer from the survey by using `$value` in this query.
* `center_repel`: Defined only for `int` and `float` answers. Repels the answer away from the center to give a more extreme value. Takes a `factor` key in options. Note that if the absolute value of the factor is less than 1, it acts as a center attractor rather than a repeller. Values between 0.8 and 1.2 are recommended.
* `enum_pref`: Defined only for `enum` answers. Takes a `mapping` option that defines a mapping from the enum values to a real number. The result is the value of the mapping for the answer.

Whatever comparator you choose, you must have the name of that comparator as a key, to which you will pass the options. This idea is also used in the postprocessors.

The `postprocess` key specifies what you want to do with the result of the comparator above. Again, it takes a `type` that specifies the operator to use, and that operator is passed options. This may be null if you do not wish to postprocess the result. The following operators are currently supported:
* `center_repel_01`: Acts the same as `center_repel` between 0 and 1.

The `merge` key specifies how to merge the results to the total score. It takes a `type` key that specifies the merger to use, and that merger is passed options. The following mergers are currently supported:
* `multiply`: Multiplies by a constant real number. Takes a float `factor` as options.
* `add_if_higher`: Adds a constant value if the result is higher than a threshold. Takes `threshold` and `add` as options.

The final result will be clipped between 0 and 1.
