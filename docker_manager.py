import docker

class DockerManager:

    def __init__(self, client=None):
        self.client = client or docker.from_env()

    def stop_and_remove_container(self, container_name):
        try:
            container = self.client.containers.get(container_name)
            container.stop()
            container.remove()
            return True
        except docker.errors.NotFound:
            return False

    def start_new_container(self, container_name, image):
        try:
            new_container = self.client.containers.run(image, name=container_name, detach=True)
            return True
        except docker.errors.ImageNotFound:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
