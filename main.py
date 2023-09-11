import argparse
from docker_manager import DockerManager  # Make sure docker_manager.py is in the same directory

def rollback_image(container_name, target_image, force=False):
    docker_manager = DockerManager()

    if docker_manager.stop_and_remove_container(container_name) or force:
        print(f"Stopped and removed container {container_name}")
    else:
        print(f"Container {container_name} not found. Will attempt to start new container.")

    if docker_manager.start_new_container(container_name, target_image):
        print(f"Started new container {container_name} with image {target_image}")
    else:
        print(f"Failed to start new container {container_name} with image {target_image}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docker image rollback tool")

    parser.add_argument("container_name", type=str, help="Name of the container to rollback")
    parser.add_argument("target_image", type=str, help="Target image to rollback to")
    parser.add_argument("--force", action="store_true", help="Forcefully stop and remove running containers")

    args = parser.parse_args()

    rollback_image(args.container_name, args.target_image, force=args.force)
