import docker
import logging
import time

class DockerManager:
    def __init__(self, client=None):
        self.client = client or docker.from_env()

    # check if the target image exists
    def image_exists(self, image_name):
        try:
            self.client.images.get(image_name)
            return True
        except docker.errors.ImageNotFound:
            print(f"Image {image_name} not found in local Docker images. Attempting to pull...")
            try:
                self.client.images.pull(image_name)
                print(f"Successfully pulled {image_name}")
                return True
            except Exception as e:
                print(f"Failed to pull {image_name}: {e}")
                return False

    def get_container_port_mappings(self, container_name):
        """
        Retrieve the port mappings for a given container.

        :param container_name: Name of the container to inspect.
        :return: A dictionary of port mappings if the container exists, an empty dictionary otherwise.
        """
        try:
            container = self.client.containers.get(container_name)
            host_config = container.attrs.get('HostConfig', {})
            port_bindings = host_config.get('PortBindings', {})
            return port_bindings
        except docker.errors.NotFound:
            logging.warning(f"Container {container_name} not found. Unable to fetch port mappings.")
            return {}


    def stop_and_remove_container(self, container_name, timeout=10):
        try:
            container = self.client.containers.get(container_name)
            
            # Attempt graceful shutdown first
            container.kill(signal="SIGTERM")  
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                if container.status == 'exited':
                    break
                time.sleep(1)
            
            # Fallback to forceful shutdown if container is still running
            if container.status != 'exited':
                container.stop()
            
            container.remove()
            logging.info(f"Successfully stopped and removed container {container_name}")
            return True
        except docker.errors.NotFound:
            logging.warning(f"Container {container_name} not found")
            return False

    def start_new_container(self, container_name, image, volume_mounts=[], env_vars=[], port_mappings={}):
        """
        Starts a new container with the given image and name 
        :param container_name: Name of the container to start
        :param image: Docker image to use for the new container
        :param volume_mounts: List of volume mounts to attach to the container
        :return: True if the container starts successfully, False otherwise
        """
        try:
            new_container = self.client.containers.run(
                image, 
                name=container_name, 
                detach=True, 
                mounts=volume_mounts, 
                environment=env_vars,
                ports=port_mappings 
            )
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
            host_config = container.attrs.get('HostConfig', {})
            volume_mounts = host_config.get('Mounts', [])
            print(container.attrs['HostConfig'])

            return volume_mounts
        except docker.errors.NotFound:
            return []
        
    def get_container_env_variables(self, container_name):
        try:
            container = self.client.containers.get(container_name)
            return container.attrs['Config']['Env']
        except docker.errors.NotFound:
            logging.warning(f"Container {container_name} not found. Unable to fetch environment variables.")
            return []
