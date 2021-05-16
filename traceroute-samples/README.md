# Traceroute samples

Individual and aggregated samples returned by participants for the
paper: `The network energy intensity of video streaming over Wi-Fi and 4G`.

## Setup

This is a Jupyter Notebook designed to run on Jupyter 5 with a Python 3.9
kernel. Dependencies are defined in `requirements.txt` and installed
automatically by the notebook.

The notebook reads the individual samples from `samples/`, runs a query against
[ipinfo.io](https://ipinfo.io) and then aggregates the output into a single
CSV ready to be read in by [the model](/model/). A pre-generated CSV
is provided in [`traceroute-samples.csv`](/traceroute-samples/traceroute-samples.csv).
