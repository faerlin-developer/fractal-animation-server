# Fractal Animation Server

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#key-features">Key Features</a></li>
        <li><a href="#use-cases">Use Cases</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

__Fractal Animation Server__ is a service that generates and serves fractal visualizations (e.g. Julia set animations)
on demand. The application features a modern service-oriented design, exposing a simple RESTful API for users to request
Julia set animations in MP4 format.

<figure>
  <img src="design.png" width="850"/>
  <figcaption>Figure 1: High-level system design showing Python microservices, PostgreSQL, Redis queue, Traefik, and 
              MinIO object storage in a Kubernetes cluster.</figcaption>
</figure>

For example, a 5-second animation starting at the Julia set defined at $c = (-0.80, -0.18)$ is shown below:

https://github.com/user-attachments/assets/075da75b-eb61-40b1-81c0-5516d780bc2e

### Key Features

__API-driven__: Users can request animated fractals via RESTful endpoints. At present, the only supported fractal is the
Julia set. The resulting animation is returned in MP4 format, showing how the Julia set evolves as parameters vary.

__Microservice Architecture__: The system is built as a set of Python-based microservices running inside a Kubernetes
cluster, orchestrated with `Traefik` as the ingress controller. User requests are received via REST endpoints, queued in
`Redis` queue for processing, and handled by worker services that generate Julia set animations. User and task metadata
information are persisted in Postgres, while the rendered MP4 files are stored in `MinIO` (object storage service).
Users can retrieve their completed fractal animations directly from object storage via pre-signed URLs.

__Extensible architecture__: Easily extendable with new fractal types (e.g. Burning Ship, Newton fractals).

### Use Cases

- __Educational Material__. If you’re interested in learning how to build the backend of a microservice architecture on
  Kubernetes, take it apart, explore it, and study how it works from the inside.
- __Creative art__. Generate unique Julia set animations defined at different points of the complex plane.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Next][Kubernetes]][Kubernetes-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

<!-- ROADMAP -->

## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (
and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites
to kick things off!

* [Img Shields](https://shields.io)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Kubernetes]: https://img.shields.io/badge/kubernetes-326CE5?&style=plastic&logo=kubernetes&logoColor=white

[Kubernetes-url]: https://kubernetes.io/

<!--
## Notes

- RBAC grants access to pods
- An Ingress is a Kubernetes resource that define rules for routing external HTTP(s) traffic to services inside the
  cluster.
- An Ingres Controler is the actual gatekeeper — the thing that listens on port 80/443 and knows what to do based on the
  Ingress rules. Example: traefik. It reads Kubernetes Ingress resources. Then it dynamically configures itself to
  route traffic to the appropriate services.
- The traefik's NodePort exposes Traefik on a fixed port outside of the cluster.
- `172.17.0.1`, that’s the default gateway IP of the Docker bridge network on Linux/macOS

-->
