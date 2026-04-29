from unittest.mock import MagicMock
from rag import ask


def test_ask_returns_answer_string():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "I want to work there because of the data culture."}

    result = ask("Why Commerzbank?", mock_chain)

    assert result == "I want to work there because of the data culture."


def test_ask_passes_input_key_to_chain():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "some answer"}

    ask("What is your background?", mock_chain)

    mock_chain.invoke.assert_called_once_with({"input": "What is your background?"})
