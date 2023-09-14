import docker
import logging

class DockerManager:
    def __init__(self, client=None):
        self.client = client or docker.from_env()

    # check if the target image exists
    def image_exists(self, image_name):
        try:
            self.client.images.get(image_name)
            return True
        except docker.errors.ImageNotFound:
            return False

    def stop_and_remove_container(self, container_name):
        try:
            container = self.client.containers.get(container_name)
            container.stop()
            container.remove()
            logging.info(f"Successfully stopped and removed container {container_name}")
            return True
        except docker.errors.NotFound:
            logging.warning(f"Container {container_name} not found")
            return False

    def start_new_container(self, container_name, image, volume_mounts=[]):
        """
        Starts a new container with the given image and name 
        :param container_name: Name of the container to start
        :param image: Docker image to use for the new container
        :param volume_mounts: List of volume mounts to attach to the container
        :return: True if the container starts successfully, False otherwise
        """
        try:
            new_container = self.client.containers.run(image, name=container_name, detach=True, mounts=volume_mounts)
            logging.info(f"Successfully started new container {container_name} with image {image}")
            return True
        except docker.errors.ImageNotFound:
            logging.error(f"Image {image} not found")
            return False
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False


    def get_container_volume_details(self, container_name):
        """
        Retrieve the volume details for a given container.
        
        :param container_name: Name of the container to inspect.
        :return: A list of volume mounts if the container exists, an empty list otherwise.
        """
        try:
            container = self.client.containers.get(container_name)
            volume_mounts = container.attrs['HostConfig']['Mounts']
            return volume_mounts
        except docker.errors.NotFound:
            return []