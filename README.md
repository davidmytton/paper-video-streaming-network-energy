# The network energy intensity of video streaming over Wi-Fi and 4G

**Authors:** David Mytton, Iain Staffell, Malte Jansen.

**Institution:** Centre for Environmental Policy, Imperial College London,
London, SW7 1NE, UK.

**Correspondence:** <david@davidmytton.co.uk>.

## Summary

> By 2023 5.3 billion people are expected to be able to access the internet, up
> from 3.9 billion in 2015. Frequent internet usage involves video streaming,
> which makes up 60% of all internet traffic, 65% on mobile. In this paper we
> calculate the energy consumption of video streaming over Wi-Fi and 4G
> connections. We analyze traceroute data collected from volunteers to reveal
> the underlying network architecture. We use this data to provide updated
> figures for the energy intensity of the different sections of the internet,
> then use industry data to derive the network energy consumption of video
> streaming. We estimate 39bn hours of video were streamed in the UK in 2019
> generating 76 EB of data and consuming a total of 4.2 TWh of electricity, or
> 1.3% of total electricity generation. Video streaming over 4G is twice as
> energy intensive per streaming hour (0.211 kWh/hr) compared to Wi-Fi (0.091
> kWh/hr).

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
