# pystiller <img src="![media/logo.png](https://raw.githubusercontent.com/openefsa/pystiller/main/media/logo.png)" height="140" align="right">

[![Lifecycle: stable](https://img.shields.io/badge/lifecycle-stable-brightgreen.svg)](https://lifecycle.r-lib.org/articles/stages.html#stable) [![codecov](https://codecov.io/gh/openefsa/pystiller/branch/main/graph/badge.svg?token=VL7426RVCI)](https://codecov.io/gh/openefsa/pystiller)

## Overview

The **pystiller** package provides a pool of functions to query **DistillerSR**
through its APIs. It features authentication and utilities to retrieve data
from DistillerSR projects and reports.

The package is intended for researchers, analysts, and practitioners who
require convenient programmatic access to DistillerSR data.

## Installation

### From PyPi

```
pip install pystiller
```

### Development version

To install the latest development version:

```
pip install git+https://github.com/openefsa/pystiller.git
```

## Requirements

An active internet connection is required, as the package communicates with
DistillerSR online services to fetch and process data.

## Usage

Once installed, load the package as usual:

```python
from pystiller import *
```

Basic usage examples and full documentation are available in the package
[guide](docs/guide.md).

## Authors and maintainers

- **Lorenzo Copelli** (author, [ORCID](https://orcid.org/0009-0002-4305-065X)).
- **Fulvio Barizzone** (author, [ORCID](https://orcid.org/0009-0006-3035-520X)).
- **Dayana Stephanie Buzle** (author, [ORCID](https://orcid.org/0009-0003-2990-7431)).
- **Rafael Vieira** (author, [ORCID](https://orcid.org/0009-0009-0289-5438)).
- **Luca Belmonte** (author, maintainer, [ORCID](https://orcid.org/0000-0002-7977-9170)).

## Links

- **Homepage**: [GitHub](https://github.com/openefsa/pystiller).
- **Bug Tracker**: [Issues on GitHub](https://github.com/openefsa/pystiller/issues).
- **DistillerSR API Documentation**: [https://apidocs.evidencepartners.com/](https://apidocs.evidencepartners.com/).
