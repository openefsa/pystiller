# Introduction to pystiller

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

## Working with API keys and environment variables

The *pystiller* package requires your personal API key provided by DistillerSR.
You can provide your API key in one of two ways:

1.  By setting it in the `.env` file.\
2.  By including it manually in the authentication request.

### Setting the API key via `.env`

A `.env` file is used to define environment variables that Python can load at
runtime. This approach is particularly convenient for sensitive information
like API keys, as it allows you to use them in any Python script or function
without hardcoding them.

Place the `.env` file in the root directory of you project (for example,
`C:/Users/username/Documents/myProject/.env` on Windows or
`~/Documents/myProject/.env` on Unix-like systems). You can create or edit this
file with any plain text editor.

Add your DistillerSR API key in the following format:

`DISTILLER_API_KEY=<your_distiller_api_key>`

Once the file is saved, the variable will be correctly set for the library to
use during execution.

### Setting the API key manually for the authentication request

Alternatively, you can provide the API key directly in the `distiller_key`
argument of the `Client()` constructor. This is useful if you  refer not to
store the API key globally. For example:

```python
from pystiller import Client

client = Client(distiller_key="<your_distiller_api_key>")
```

Note that if an API key is explicitly provided, the API key set through the
`.env` file will be ignored, if any.

### Setting the DistillerSR instance URL

The *pystiller* package needs to know the instance URL on which DistillerSR is
running to function properly. You can provide the instance URL in one of two
ways:

1.  By setting it in the `.env` file.\
2.  By including it manually in each API request.

If you prefer to store the URL in the `.env` file, add your DistillerSR
instance URL in the following format:

`DISTILLER_INSTANCE_URL=<your_distiller_instance_url>`

After saving the file, R will automatically read the API key on startup.

Alternatively, you can provide the instance URL directly in the
`distiller_instance_url` argument of the `Client()` constructor. This is useful
if you refer not to store the instance URL globally. For example:

```python
from pystiller import Client

client = Client(distiller_instance_url="<your_distiller_instance_url>")
```

## Basic usage

The main purpose of *pystiller* is to query the DistillerSR APIs for specific
project or report codes and retrieve relevant information across various
endpoints.

Below are examples demonstrating how to use the functions in this package.
First, load the *pystiller* package:

```python
from pystiller import *
```

Then, initialize the client by specifying the API key and/or the instance URL
you want to use:

```python
# Use the API key and the instance URL defined in .env file.
client = Client()
# Manually define the API key and the instance URL.
client = Client(
    distiller_key="<your_distiller_api_key>",
    distiller_instance_url="<your_distiller_instance_url>"
)
```

To explore the arguments and usage of a specific function, you can run:

```python
help(function_name)
```

This will show the full documentation for the function, including its
arguments, return values, and usage examples.

For example, if you are working with the `Client.get_report()` function,
you can check its documentation with:

```python
help(Client.get_report)
```

## Getting an authentication token

Before using functions of this package, you must obtain an authentication token
derived from the API key provided by DistillerSR. The client automatically
requests the token upon creation using the specified API key.

By default, Distiller tokens expire after 60 minutes (1 hour). Automatic
refreshes of the token can be enabled by setting the `automatic_token_refresh`
parameter to `True` during client initialisation. For example:

```python
client = Client(automatic_token_refresh=True)
```

The obtained token can be used to perform API calls using the
`Client.get_projects()`, `Client.get_reports()`, and `Client.get_report()`
functions.

## Getting the list of projects associated with the user

If you want to retrieve the list of all the available projects associated with
your DistillerSR account, you can browse them with the `Client.get_projects()`
function, as follows:

```python
client = Client()

projects = client.get_projects()

print(projects)
```

## Getting the list of reports associated with a project

Each individual project has its own associated set of projects. You can
retrieve the list of associated reports with the `Client.get_reports()`
function, as follows:

```python
client = Client()

reports = client.get_reports(project_id=123)

print(reports)
```

## Getting a specific report

You can retrieve a specific report with the `Client.get_report()` function by
specifying a project ID and a report ID, as follows:

```python
client = Client()

project_id_ = 123
report_id_ = 456

report = client.get_report(
  projectId=project_id_,
  reportId=report_id_,
  format=ReportFormat.CSV
)

print(report.head())
```

Note that for very large reports, CSV files are generally a better choice.
Exporting to Excel may cause issues when tables exceed one million rows,
whereas CSV handles large datasets more reliably.
