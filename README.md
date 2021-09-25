# The network energy intensity of video streaming over Wi-Fi and 4G

**Authors:** David Mytton, Iain Staffell, Malte Jansen.

**Institution:** Centre for Environmental Policy, Imperial College London,
London, SW7 1NE, UK.

**Correspondence:** <david@davidmytton.co.uk>.

## Summary

> Over 5 billion people have access to the internet. Video streaming is a common activity, making up 60% of all internet traffic. We quantify the energy consumption of video streaming over Wi-Fi and 4G connections for the first time using empirical data. We analyze 116 traceroutes collected from volunteers to reveal the underlying network architecture. We combine these with industry data to estimate the energy intensity of different sections of the internet, and the network energy consumption of video streaming. Using the UK as a case study, we find that 39.2±8.8 bn hours of video were streamed in 2019, generating 76.3±17.1 EB of network traffic which consumed 4.2±0.9 TWh of electricity, or 1.3% of national demand. 4G streaming is twice as energy intensive (0.211 kWh/hr) as over Wi-Fi (0.091 kWh/hr), therefore the carbon intensity of use-stage networking for video streaming over Wi-Fi is 0.023 kgCO2/hour compared to 0.054 kgCO2/hour for 4G.

## Citation

The paper has not yet been published. On publication this repo will be updated
with the correct citation.

## This repository

This repo contains the following materials:

* [**Model:**](/model/) Jupyter notebook containing the calculations and energy
  model.
* [**Traceroute collector:**](/traceroute-collector/) The code used to collect
  Scamper traceroute samples from participants.
* [**Traceroute samples:**](/traceroute-samples/) The traceroute samples in
  Scamper JSON and aggregated into a single CSV for analysis in the model.

## License

Different licenses are used throughout this repo but unless otherwise
specified, these materials are published under the
[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) license.
