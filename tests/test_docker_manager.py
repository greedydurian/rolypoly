# test_docker_manager.py

import unittest
from unittest.mock import Mock, patch
from docker_manager import DockerManager
import docker 

class TestDockerManager(unittest.TestCase):

    def setUp(self):
        self.mock_client = Mock()
        self.docker_manager = DockerManager()
        self.docker_manager.client = self.mock_client


    def test_stop_and_remove_container_not_found(self):
        self.mock_client.containers.get.side_effect = docker.errors.NotFound("Not Found")

        result = self.docker_manager.stop_and_remove_container("container_name")

        self.assertEqual(result, False)

    def test_stop_and_remove_container_success(self):
        container_mock = Mock()
        self.mock_client.containers.get.return_value = container_mock
        
        result = self.docker_manager.stop_and_remove_container("container_name")
        
        self.assertTrue(result)
        self.mock_client.containers.get.assert_called_with("container_name")
        container_mock.stop.assert_called_once()
        container_mock.remove.assert_called_once()

    def test_start_new_container_success(self):
        result = self.docker_manager.start_new_container("container_name", "image")
        
        self.assertTrue(result)
        self.mock_client.containers.run.assert_called_once()

    def test_start_new_container_fail(self):
        self.mock_client.containers.run.side_effect = Exception("Error")
        
        result = self.docker_manager.start_new_container("container_name", "image")
        
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
