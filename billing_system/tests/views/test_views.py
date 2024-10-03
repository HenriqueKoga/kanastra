import os
from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def mock_file(tmpdir):
    file = tmpdir.join("debts.csv")
    file.write("name,governmentId,email,debtAmount,debtDueDate,debtId\nJohn Doe,11111111111,johndoe@example.com,1000.00,2023-10-10,1")
    mock_file = MagicMock()
    mock_file.name = "debts.csv"
    mock_file.chunks.return_value = [
        b'name, governmentId, email, debtAmount, debtDueDate, debtId\n',
        b'John Doe, 11111111111, johndoe@example.com, 1000.00, 2023-10-10, 1'
    ]
    return mock_file


@pytest.fixture
def mock_shared_folder(monkeypatch, tmpdir):
    shared_folder_mock = str(tmpdir.mkdir("shared_folder"))
    monkeypatch.setattr('billing_system.settings.SHARED_FOLDER', shared_folder_mock)
    return shared_folder_mock


def test_upload_csv_success(client, mock_file, mock_shared_folder):
    url = reverse('upload')
    with patch('billing_system.tasks.debts_tasks.process_csv.delay') as mock_process_csv:
        response = client.post(url, {'file': mock_file}, format='multipart')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == "Started processing debts"
        file_path = os.path.join(mock_shared_folder, mock_file.name)
        mock_process_csv.assert_called_once_with(file_path)


def test_upload_csv_exception(client, mock_file):
    url = reverse('upload')
    with patch('builtins.open', side_effect=Exception("Test Exception")):
        response = client.post(url, {'file': mock_file}, format='multipart')

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data['error'] == "Error processing debts"
