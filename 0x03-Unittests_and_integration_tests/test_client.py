#!/usr/bin/env python3
"""Unit tests for GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from client import GithubOrgClient  # Your GitHub org client
from fixtures import TEST_PAYLOAD  # Your test data
from parameterized import parameterized_class
from parameterized import parameterized
from unittest.mock import patch, MagicMock

class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct data"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL from mocked org"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names"""
        expected_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = expected_payload

        with patch.object(
            GithubOrgClient, "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_url:
            mock_public_url.return_value = "https://fake.url/repos"
            client = GithubOrgClient("test_org")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://fake.url/repos")
            mock_public_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
    for org_payload, repos_payload, expected_repos, apache2_repos in TEST_PAYLOAD  # ✅ CORRECT unpacking
])

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos"""
    def test_public_repos(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = self.repos_payload
            client = GithubOrgClient(self.org_payload['login'])
            result = client.public_repos()
            self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = self.repos_payload
            client = GithubOrgClient(self.org_payload['login'])
            result = client.public_repos(license="apache-2.0")
            self.assertEqual(result, self.apache2_repos)

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get"""
        cls.get_patcher = patch('requests.get')

        # Start patcher and get the mock object
        cls.mock_get = cls.get_patcher.start()

        # Configure side_effect for different URLs
        def side_effect(url):
            mock_response = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter (apache-2.0)"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
