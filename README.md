# Traceroute Collector

This code packages the methodology for my [Environmental Technology MSc](https://www.imperial.ac.uk/environmental-policy/msc/) thesis at Imperial College London so that the required traceroute data can be collected from volunteers as easily as possible.

The code used in this project can be [found on GitHub](https://github.com/davidmytton/traceroute-collector).

## Study

### Goal

The goal of this study is to estimate the energy intensity of internet data transfer and discover how it differs when connecting over Wi-Fi and 4G. The study will examine the network routing for video streaming workloads when connected via Wi-Fi and 4G from different countries. The network traceroute will be used to determine the underlying network equipment architecture for each network type and country. The energy requirements for the network will then be calculated based on equipment characteristics for each workload to provide a range of energy estimates for each workload scenario.

### Methodology

1. Participants who are willing to run a network trace on their personal computer will be recruited from multiple countries. We will need at least 10 participants but are not setting an upper limit.
2. YouTube, Netflix, Facebook Video and Instagram make up a majority of all internet and mobile traffic (Sandvine, [2019](https://www.sandvine.com/global-internet-phenomena-report-2019), [2020](https://www.sandvine.com/download-report-mobile-internet-phenomena-report-2020-sandvine)). These will be used as the destinations for the traceroutes. They use sophisticated mechanisms to ensure the best user experience which means the network destination can change for every user ([Adhikari et al., 2012](https://doi.org/10.1109/INFCOM.2012.6195644); [Juluri et al., 2013](https://ieeexplore.ieee.org/document/6573037); [Loh et al., 2019](https://doi.org/10.1145/3304109.3325819); [Nguyen, Fourmaux & Deleuze, 2019](https://doi.org/10.1007/978-3-030-14413-5_13)). The correct destination will be detected using the open source [`youtube-dl`](https://ytdl-org.github.io/youtube-dl/index.html ) running in simulation mode to reveal the destination URL but not download content. `youtube-dl` supports other sites, not just YouTube.
3. Traces will be collected using [Scamper](https://www.caida.org/tools/measurement/scamper/), an open source implementation of [Paris traceroute](https://paris-traceroute.net ) designed for academic research ([Luckie, 2010](https://doi.org/10.1145/1879141.1879171)). *Paris traceroute* deals with the inability of `traceroute` to handle load balancing ([Augustin, Friedman & Teixeira, 2007](https://doi.org/10.1109/E2EMON.2007.375313)). Detecting accurate routing is important to record the correct hops. No personal information will be collected; the source IP will be removed.
4. Steps 2-3 have been implemented in this Python wrapper so the participant can run a command to collect the data, once over Wi-Fi and once tethered over 4G. No content is downloaded and a traceroute uses a tiny amount of data, so this will not affect 4G data caps. The participant will return the results to via e-mail to david.mytton19@imperial.ac.uk.
5. This will allow workload specific ranges for the energy usage of the internet to be estimated.

### Content

YouTube, Netflix, Facebook Video and Instagram make up a majority of all internet and mobile traffic (Sandvine, [2019](https://www.sandvine.com/global-internet-phenomena-report-2019), [2020](https://www.sandvine.com/download-report-mobile-internet-phenomena-report-2020-sandvine)). Netflix and Facebook require accounts to log in so will be excluded.

* **YouTube**: The video "[Luis Fonsi - Despacito ft. Daddy Yankee](https://www.youtube.com/watch?v=kJQP7kiw5Fk)" was selected as the number 1 most viewed video on YouTube as of 2020-04-21.
* **Instagram**: The video "[snowboarding from Kylie Jenner](https://www.instagram.com/p/B5vhf4innBN/)" was selected as the first video on the list of [most liked Instagram posts](https://en.wikipedia.org/wiki/List_of_most-liked_Instagram_posts) as of 2020-04-15.

## Results

The actual results from this study will be published once completed. This README will be updated with the relevant links.

## Usage Instructions

### Requirements

* macOS.
  * Developed on macOS 10.15 with Python 3.7.6
  * Some participants reported problems with certificate validation on macOS 10.12 and 10.13, which have outdated certificate repositories. [Upgrading the certificate store](https://stackoverflow.com/a/61142526) was tried but this didn't help. As such, certificate verification was disabled in the code.
* Known working on Python 3.7 and 3.6.

### Setup

1. Extract the release zip file into a new directory. In a terminal, `cd` into that directory.
2. Execute: `python3 -m venv venv`. macOS may ask you to download the free developer tools from Apple. Allow this to run when prompted then run this command again.
3. Execute: `source venv/bin/activate`
4. Execute: `pip3 install -r requirements.txt`
5. Test the scamper binary: `./scamper`. macOS may block execution. If so, go to System Preferences > Security & Privacy > General then allow access. Execute `./scamper` again to verify.

### Execution

1. Connect your computer over Wi-Fi.
2. Execute: `sudo python3 main.py --connection wifi`
3. Disconnect from Wi-Fi. Connect by tethering to your 4G phone.
4. Execute: `sudo python3 main.py --connection 4g`

#### Output

Several files prefixed with `results-` will be produced all of which should be returned as part of the research. Example output is provided in the [`example-results`](/example-results) directory.

`results-*-wifi.json` and `results-*-4g.json` contain the full technical traceroute details generated by scamper in JSON output mode. The public IP of the user is redacted if present.

## Analysis

The returned results files are stored pseudonymously so they can be analysed. The researchers will store them according to the following naming convention:

`results-COUNTRY-CITY-PARTICIPANT_ID-DESTINATION-CONNECTION.json`

e.g. `results-uk-london-15-www.instagram.com-4g.json`

[A script](/analyse.py) is provided to aggregate the results into CSV format for easier analysis:

`python3 analyse.py --results_dir example-results/ --ipinfo_key API_KEY`

### Parameters

`--results_dir` = the directory that contains all the Scamper results JSON files.

`--ipinfo_key` = your API key for [ipinfo.io](https://ipinfo.io), used to look up information about each trace IP address.

### Removal

1. Execute: `deactivate`
2. Then delete the folder that was extracted.

## Notes

* The `./scamper` binary is committed into the repo compiled on macOS 10.15.4 (19E287) from the [2020-03-12 scamper-cvs-20191102b](https://www.caida.org/tools/measurement/scamper/code/scamper-cvs-20191102b.tar.gz) release to avoid having to build a binary on a volunteer machine (or [install via homebrew](https://formulae.brew.sh/formula/scamper)).
* The code uses [jsonip.com](https://jsonip.com) to get the current public IP so it can be redacted from the results.
* If you are using something like Little Snitch, it needs to be completely disabled whilst running the tests because it interfers with the way that scamper manipulates the firewall.

## License

All the code in this repo is licensed under [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

Scamper is provided in a unmodified, compiled binary executable as part of this project. It is also licensed under [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) and the original code that was compiled is available from the [2020-03-12 scamper-cvs-20191102b](https://www.caida.org/tools/measurement/scamper/code/scamper-cvs-20191102b.tar.gz) release, included in this repo as [`scamper-cvs-20191102b.tar.gz`](/scamper-cvs-20191102b.tar.gz) for archive purposes.
