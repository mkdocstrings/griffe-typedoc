# Griffe TypeDoc

[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://mkdocstrings.github.io/griffe-typedoc/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#griffe-typedoc:gitter.im)

Signatures for entire TypeScript programs using [TypeDoc](https://typedoc.org/).

WARNING: **Still in prototyping phase!**
Feedback is welcome.

## Installation

This project is available to sponsors only, through my Insiders program. See Insiders [explanation](https://mkdocstrings.github.io/griffe-typedoc/insiders/) and [installation instructions](https://mkdocstrings.github.io/griffe-typedoc/insiders/installation/).

## Usage

Add these [TypeDoc](https://typedoc.org/) configuration files to your repository:

```tree hl_lines="4 5"
./
    src/
        package1/
    typedoc.base.json
    typedoc.json
```

```json title="typedoc.base.json"
{
  "$schema": "https://typedoc.org/schema.json",
  "includeVersion": true
}
```

```json title="typedoc.json"
{
  "extends": ["./typedoc.base.json"],
  "entryPointStrategy": "packages",
  "entryPoints": ["./src/*"]
}
```

Update the entrypoints to match your file layout so that TypeDoc can find your packages. See [TypeDoc's configuration documentation](https://typedoc.org/options/configuration/).

Then in each of your package, add this TypeDoc configuration file:

```tree hl_lines="4"
./
    src/
        package1/
            typedoc.json
    typedoc.base.json
    typedoc.json
```

```json title="typedoc.json"
{
  "extends": ["../../typedoc.base.json"],
  "entryPointStrategy": "expand",
  "entryPoints": ["src/index.d.ts"]
}
```

Again, update entrypoints to match your file and package layout. See [TypeDoc's configuration documentation](https://typedoc.org/options/configuration/).

**Your packages must be built for TypeDoc to work.**

Finally, load your TypeScript API data with Griffe TypeDoc:

```python
from griffe_typedoc.loader import load

data = load(
    "typedoc",  # name or path of the typedoc executable
    working_directory=".",  # point at your monorepo
)
```

See our [API reference](https://mkdocstrings.github.io/griffe-typedoc/reference/griffe_typedoc/).

