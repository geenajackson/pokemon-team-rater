# -*- mode: Python -*-

docker_build('pokemon-team-rater-image', '.')
k8s_yaml('kubernetes.yml')
k8s_resource('hello', port_forwards=8000)
