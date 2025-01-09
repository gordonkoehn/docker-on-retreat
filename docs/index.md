# Welcome to Docker on Retreat

This document and repo has a minimal viable example of how to develop a python application containerized/dockerized locally and run it on the cluster.

We have a small python script that relies on a few dependenceies installed via _Conda_.
Out python script has requires some imput files and prints and creates some output.

A typical flow of a scientific investigation.

## Prerequisites

This workbook is meant for a quick life demo, hence it may be better to just follow. Yet if you want to take the challange. Please make sure your machine is set up. 

Install Docker on your local computer and create an account on [dockerhub](https://hub.docker.com/). You can find instructions [here](https://docs.docker.com/get-started/get-docker/). Note that you need admin rights to install and use Docker, and if you are installing Docker on Windows, you need a recent Windows version. 


Please also login into your docker hub account in the Docker GUI or with 

```
docker login
```

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

Make sure you are in the root directory of this project.

```
docker build .
```

What just happend? This command refers to the Docker Engine, the Runtime engine of this particular containerization technology. This command be default looks in the current directory for the container _Manifest_, for Dockers the _Dockerfile_. It contains all the instructions to make the image. The above command did just that. It build the image given the instructions in the manifest. So where is the image ? We'll it's not a file you see. But you can check for it with:

```
docker image list
```

Let's properly name out container now. But before take care if you have..
<details>
<summary>If using an Apple M chip (newer Macs)</summary>

If you are using a computer with an Apple M chip, you have the less common ARM system architecture, which can limit transferability of images to (more common) x86_64/AMD64 machines. When building images on a Mac with an M chip (especially if you have sharing in mind), it’s best to set the DOCKER_DEFAULT_PLATFORM to linux/amd64 with:

```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

This is unfortunate currently, but containers protect us for any issues with operating systems but the chip-set may still cause issues, so it's best to use the default. Especially because clusters won't use ARM chips. Clusters are not optimized for energy efficiency that way.

</details>

```
docker build -t beatenberg:v1 .
```


Let's check again 

```
docker image list
```

Now you should see your container with a tag in the list.

Let's check the input and output files in 
`in/input.csv` and `out/output.txt`.

Let's now run the docker locally. Because we have input and output files we need to mount these directories. As a container isolates your application with seemingly its own operating system and file system. To get data in and out, you need to mount. We already saw which are the directories used inside of the container. Next, we define their equivalent outside of the container and run it. The next command takes the image we just created and makes a container out of it.


```
docker run -v $(pwd)/in:/app/in -v $(pwd)/out:/app/out beatenberg:v1
```

To be explicit we need to pass the `.env` file, here we just relied on the defaults.

```
docker run --env-file .env -v $(pwd)/in:/app/in -v $(pwd)/out:/app/out beatenberg:v1
```

Woha, this worked. And it's quite useful. This gets useful if your installation is complicated or unreliable across machines.

Note that this container just runs and exits, that's usually what we want on a cluster.



Let's look inside for context.

```
docker run -v $(pwd)/in:/app/in -v $(pwd)/out:/app/out -it beatenberg:v1 /bin/bash
```

There is our application. And look its ubuntu.

In another terminal, let's see this container:

```
docker ps
````
It shows information about the containers that are currently running, including their container ID, image, command, creation time, status, ports, and names. 


To see all containers, including those that are stopped, you can use the -a flag:
```
docker ps -a
```

### Let's share the image

Now we will share the image to dockerhub. If you haven't already you have to login to your dockerhub account with:

```
docker login
```

Now that we have created our first own docker image, we can store it and share it with the world on docker hub. Before we get there, we first have to (re)name and tag it.

Before pushing an image to dockerhub, docker has to know to which user and which repository the image should be added. That information should be in the name of the image, like this: user/imagename. We can rename an image with docker tag (which is a bit of misleading name for the command). So we could push to dockerhub like this:

```
docker tag beatenberg:v1 [USER NAME]/beatenberg:v1
docker push [USER NAME]/beatenberg:v1
```

So you just shared your image wiht the world.

### Let's run it on the cluster

On a cluster there is no container runtime engine, hence we cannot use _docker_, but instead we are going to use _apptainer_.

Apptainer can take several image formats (e.g. a docker image), and convert them into it’s own .sif format. Unlike docker this image doesn’t live in a local image cache, but it’s stored as an actual file.

We can get our image from _dockerhub_ wiht:

```
apptainer pull docker://[USER NAME]/[IMAGE NAME]:[TAG]
```

so 

```
apptainer pull docker://[USER NAME]/beatenberg:v1
```

if you got stuck just use mine:

```
apptainer pull docker://gordonkoehn/beatenberg:v1
```

Let's have a look:

```
ls
```
Look there is the `.sif`, this is the image in apptainer format.


Apptainer is also different from Docker in the way it handles mounting. By default, Apptainer binds your home directory and a number of paths in the root directory to the container. This results in behaviour that is almost like if you are working on the directory structure of the host.

## Credits

This mini course is a desitilate and derivatieve of the Swiss Instirute of Bioinformatics course called [Introduction to Containers and Snakemake](https://sib-swiss.github.io/containers-snakemake-training/latest/course_material/day1/introduction_containers/).