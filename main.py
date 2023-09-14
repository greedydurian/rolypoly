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
    docker_manager = DockerManager()

    if not docker_manager.image_exists(target_image):
        json_log(f"Target image {target_image} not found. Aborting rollback.", level="ERROR")
        return

    volume_mounts = []
    if preserve_volumes:
        volume_mounts = docker_manager.get_container_volume_details(container_name)

    user_input = input(f"Are you sure you want to stop and remove the container {container_name}? (y/n): ")
    if user_input.lower() != 'y' and not force:
        json_log("Operation cancelled by the user.")
        return

    if docker_manager.stop_and_remove_container(container_name) or force:
        json_log(f"Stopped and removed container {container_name}")
    else:
        json_log(f"Container {container_name} not found. Will attempt to start new container.")

    if docker_manager.start_new_container(container_name, target_image, volume_mounts):
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
