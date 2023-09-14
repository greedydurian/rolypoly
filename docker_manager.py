import docker
import logging

class DockerManager:

    def __init__(self, client=None):
        self.client = client or docker.from_env()

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

    def start_new_container(self, container_name, image):
        try:
            new_container = self.client.containers.run(image, name=container_name, detach=True)
            logging.info(f"Successfully started new container {container_name} with image {image}")
            return True
        except docker.errors.ImageNotFound:
            logging.error(f"Image {image} not found")
            return False
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
