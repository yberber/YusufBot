from unittest.mock import MagicMock, patch
from rag import ask


def test_ask_returns_answer_and_usage():
    mock_retriever = MagicMock()
    mock_retriever.invoke.return_value = [MagicMock(page_content="I love data science.")]

    mock_response = MagicMock()
    mock_response.content = "I want to work there because of the data culture."
    mock_response.usage_metadata = {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30}

    with patch("rag.ChatGroq") as MockChatGroq:
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = mock_response
        MockChatGroq.return_value = mock_llm

        answer, usage = ask("Why Commerzbank?", "llama-3.3-70b-versatile", mock_retriever)

    assert answer == "I want to work there because of the data culture."
    assert usage["total_tokens"] == 30
    assert usage["input_tokens"] == 10
    assert usage["output_tokens"] == 20


def test_ask_passes_question_to_retriever():
    mock_retriever = MagicMock()
    mock_retriever.invoke.return_value = [MagicMock(page_content="context text")]

    mock_response = MagicMock()
    mock_response.content = "some answer"
    mock_response.usage_metadata = {"input_tokens": 5, "output_tokens": 10, "total_tokens": 15}

    with patch("rag.ChatGroq") as MockChatGroq:
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = mock_response
        MockChatGroq.return_value = mock_llm

        ask("What is your background?", "llama-3.3-70b-versatile", mock_retriever)

    mock_retriever.invoke.assert_called_once_with("What is your background?")


def test_ask_injects_retrieved_context_into_prompt():
    mock_retriever = MagicMock()
    mock_retriever.invoke.return_value = [MagicMock(page_content="I studied at Heidelberg.")]

    mock_response = MagicMock()
    mock_response.content = "some answer"
    mock_response.usage_metadata = {"input_tokens": 5, "output_tokens": 10, "total_tokens": 15}

    with patch("rag.ChatGroq") as MockChatGroq:
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = mock_response
        MockChatGroq.return_value = mock_llm

        ask("Where did you study?", "llama-3.3-70b-versatile", mock_retriever)

        messages = mock_llm.invoke.call_args[0][0]
        assert "I studied at Heidelberg." in messages[0].content
