# Backend Software Engineer Coding Challenge

----

# Table of contents

1. [Introduction](#introduction)
2. [Challenge Description](#challenge-description)
3. [Submission Requirements](#submission-requirements)
4. [Review](#review)

----

# Introduction

Your challenge is to set up a video management server and ensure a reliable video backup system is present. 
There are two parts to the challenge: design and code. 
Consider the architecture design as a proposed long-term solution, and the code section as a rapid prototype. 
This gives you the ability to conceptually propose a long-term solution and code out a rapid prototype that only satisfies the basics to get the idea moving. 
It is suggested to start with the code, then once you have something working create a design for a long-term solution.  
If only the code is completed, that is 100% fine!  We would rather have a rapid prototype completed than two half finished components.

__Support Requests__

Team support is a big part of RAD's team culture.

If you have a roadblock, ask the VMS team lead for support so that you can make progress. Here is what we offer:

- Q/A through email
- Q/A through 15 minute video call

There is no limit to the number of support requests you have, but we do encourage you to organize your thoughts into a coherent support request.


__code__

Developing reliable code is a complex task, so please keep a limited scope and focus on solving the core problems before adding additional features. The core problems are listed as hard requirements in #challenge-description below.

__design__

Architecture design may include diagrams, description of design patterns, and descriptions of services (e.g. cloud server + API, cloud server + database, cloud server ...). 
It is important to note that you do not need to code out all components of your design. Instead, focus on conceptualizing so that you can propose solutions that solve the problems listed in #challenge-description. Your design may be very different from your code, and feel free to suggest alternative software stacks to those required in the coding section.


# Challenge Description

Set up and configure the Ant Media Server so that videos may be ingested and stored to its local file system.  A development video is provided and may be run from the Gstreamer container (view .docker/README.md).

Create a "Manager" that satisfies the following process:

1. provide the ability to set up a stream with AMS rest API
2. back up videos stored in AMS on regular intervals
3. store backup details in a database so that it can be fetched at a later date.
- use a back-up interval that is reasonable for development
- e.g. if the development video is two minutes long then back up every 30 seconds.

__assumptions__

- the two services "Video Server" (AMS) and "Manager" may exist on a single server.
- all microservices are dockerized and run on a single docker network for development's sake: Gstreamer, Video Server (AMS), Manager, Database, Zookeeper, and Kafka.
- The Manager should set up video streams before video content is streamed from the Gstreamer service to Video Server service.
- The Video Server (AMS) should cache video streams in its file system when video content is actively streaming.
- The Manager should back up videos saved in the Video Server's file system (AMS) to the cloud.
- The Manager should store pertinent backup information to the database


__setup__

- view docker container setup readme: .docker/README.md
- view the postman collection: docs/postman
- review the Dockerfiles and fix it until each one can be built properly (there are few errors are in the files)

__hard requirements__


- Any programming system should be implemented using a modern programming language, such as Python, C++, or Java.

- The Video Server should be able to ingest a single stream in Ant Media Server and use AMS video storage features to cache videos to its file system.

- The Manager should include an API framework, such as Flask or Spring Boot, and interact with AMS REST API (https://antmedia.io/rest/).

- The Manager should copy the local video files stored in AMS file system to another location

- The database should be a NoSQL database, such as MongoDB or Cassandra, and have pertinent information about the location of the backed up video files

- A Makefile must include project commands to build and run your project for ease of use. For example: docker build, docker run, docker stop, run tests, etc


__soft requirements__


- The Manager should run from a configuration file so that configurations like back up duration, database URL, cloud storage URL, and more may be adjusted for each run.

- The Manager's video backup mechanism should be able to store video from Ant Media Server in a cloud storage provider for long-term retention. Additionally, the Manager must be able to fetch previously stored videos and store them to AMS file system.

- The database should be able to store and retrieve all pertinent information about a stream, its backup history, and location of backups so that an external client may retrieve them at a later date via the Manager.

- (BONUS) Monitoring AMS: Create a visualization stack that provides useful information about Ant Media Server's health and performance.
- hint: reading AMS docs will help with suggested stacks and setup (https://resources.antmedia.io/docs)

----


# Submission Requirements

----

__email submission__

Once completed, Email the team lead (matt.m@radskunkworks.com) to notify your submission. The email can be as simple as "I have completed the challenge."
- Please ensure that all hard requirements are met before adding soft requirements.

__code submission__

- you will have a repo and branch to work with.

__design submission__

- if you have time to complete this section, add to the `docs` folder


----

# Review

A 30 minute discussion about your submission with our team members.

----


## Resources

- docker set up: `.docker/README.md`
- ams postman collection: `docs/postman`
- ams REST API: https://antmedia.io/rest/
- ams docs: https://resources.antmedia.io/docs
