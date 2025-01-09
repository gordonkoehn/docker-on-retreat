# Welcome to Docker on Retreat

This document and repo has a minimal viable example of how to develop a python application containerized/dockerized locally and run it on the cluster.

We have a small python script that relies on a few dependenceies installed via _Conda_.
Out python script has requires some imput files and prints and creates some output.

A typical flow of a scientific investigation.

## Prerequisites

This workbook is meant for a quick life demo, hence it may be better to just follow. Yet if you want to take the challange. Please make sure your machine is set up. 

Install Docker on your local computer and create an account on [dockerhub](https://hub.docker.com/). You can find instructions [here](https://docs.docker.com/get-started/get-docker/). Note that you need admin rights to install and use Docker, and if you are installing Docker on Windows, you need a recent Windows version. 

<details>
<summary>If working on Windows</summary>

During the course exercises you will be mainly interacting with docker through the command line. Although windows powershell is suitable for that, it might cause some issues with bind mounting directories. Hence, it is easier to follow the exercises if you have a UNIX or ‘UNIX-like’ terminal. You can get one by using WSL2. With VScode, you can also add the WSL extension. Make sure you install the latest versions before installing docker.

</details>

## Creating your Program.

Our example program is in `src/main.py`. Let's check it out:
- We import some libaries, supported by our virtual envrioment manager _Conda_. See `environment.yml`.
- We get out input and output paths.
- We import the data. Two float numbers.
- We do some heavy computation with _numpy_.
- We do some Output Formating with a cool, but uselless tool called _figlet_. You'll see.
- We save the result, to the output file and console.

### Make a docker out of it.

```
docker build -t beatenberg .
```

What just happend? This command refers to the Docker Engine, the Runtime engine of this particular containerization technology.