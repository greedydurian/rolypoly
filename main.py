#!/usr/bin/env python3

import argparse
import logging
import json
from docker_manager import DockerManager

def setup_logging():
    logHandler = logging.FileHandler("logfile.txt")
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    ## logs into console
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

def json_log(message, level="INFO"):
    log_entry = json.dumps({"level": level, "message": message})
    if level == "INFO":
        logging.info(log_entry)
    elif level == "ERROR":
        logging.error(log_entry)

def rollback_image(container_name, target_image, force=False, preserve_volumes=False):
    """
    Rolling back image yoooo 

    :param container_name: name of the container to inspect.
    :param target_image: image to which the container should be rolled back
    :param force: default False. if True, forcefully stop and remove running containers 
    :param preserve_volumes: default False. if True, the volumes from the original container will be re-attached to the new container

    logical sequence: 
    (1) fetch existing environment  
    (2) stop and remove the existing container
    (3) validate the target image exists 
    (4) start the new container with the target image

    """
    docker_manager = DockerManager()

    # 1
    env_vars = docker_manager.get_container_env_variables(container_name)
    volume_mounts = []
    if preserve_volumes:
        volume_mounts = docker_manager.get_container_volume_details(container_name)

    # 2
    if force:
        if docker_manager.stop_and_remove_container(container_name):
            json_log(f"Forcefully stopped and removed container {container_name}")
        else:
            json_log(f"Failed to forcefully stop and remove container {container_name}.", level="ERROR")
            return
    else:
        user_input = input(f"Are you sure you want to stop and remove the container {container_name}? (y/n): ")
        if user_input.lower() == 'y':
            if docker_manager.stop_and_remove_container(container_name):
                json_log(f"Stopped and removed container {container_name}")
            else:
                json_log(f"Failed to stop and remove container {container_name}.", level="ERROR")
        else:
            json_log("Operation cancelled by the user.")

    # 3
    if not docker_manager.image_exists(target_image):
        json_log(f"Target image {target_image} not found. Aborting rollback.", level="ERROR")
        return

    # 4
    if docker_manager.start_new_container(container_name, target_image, volume_mounts, env_vars):
        json_log(f"Started new container {container_name} with image {target_image}")
    else:
        json_log(f"Failed to start new container {container_name} with image {target_image}", level="ERROR")

if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(description="Docker image rollback tool")
    parser.add_argument("container_name", type=str, help="Name of the container to rollback")
    parser.add_argument("--preserve-volumes", action="store_true", help="Preserve volumes during rollback")
    parser.add_argument("target_image", type=str, help="Target image to rollback to")
    parser.add_argument("--force", action="store_true", help="Forcefully stop and remove running containers")
    args = parser.parse_args()
    rollback_image(args.container_name, args.target_image, force=args.force, preserve_volumes=args.preserve_volumes)
