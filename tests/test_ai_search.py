from contextlib import nullcontext

import src.frontend.pages.ai_search as ai_search


def test_generate_response_uses_model(mocker, tmp_path):
    data_file = tmp_path / "crawled.jsonl"
    data_file.write_text('{"content": "hello"}\n')

    mock_model = mocker.MagicMock()
    mock_model.generate_content.return_value.text = "answer"
    mocker.patch(
        "src.frontend.pages.ai_search.genai.GenerativeModel", return_value=mock_model
    )

    result = ai_search.generate_response("query", data_file=str(data_file))

    assert result == "answer"
    mock_model.generate_content.assert_called_once()


def test_render_shows_response(mocker):
    mocker.patch("src.frontend.pages.ai_search.st.title")
    mocker.patch(
        "src.frontend.pages.ai_search.st.spinner", return_value=nullcontext()
    )
    mocker.patch("src.frontend.pages.ai_search.st.text_input", return_value="hello")
    write = mocker.patch("src.frontend.pages.ai_search.st.write")
    mocker.patch(
        "src.frontend.pages.ai_search.generate_response", return_value="ans"
    )

    ai_search.render()

    write.assert_called_once_with("ans")
