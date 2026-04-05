import numpy as np
import pytest
from unittest.mock import patch, MagicMock


class TestPredictFromHtml:
    @patch("service.brain_analysis.clean_text", return_value="cleaned text")
    @patch("service.brain_analysis._get_model")
    def test_returns_preds_and_segments(self, mock_get_model, mock_clean):
        mock_model = MagicMock()
        mock_model.get_events_dataframe.return_value = MagicMock()
        mock_model.predict.return_value = (np.zeros((3, 20484)), ["seg1", "seg2", "seg3"])
        mock_get_model.return_value = mock_model

        from service.brain_analysis import predict_from_html

        preds, segments = predict_from_html("<p>hello</p>")

        mock_clean.assert_called_once_with("<p>hello</p>")
        mock_model.get_events_dataframe.assert_called_once()
        mock_model.predict.assert_called_once()
        assert preds.shape == (3, 20484)
        assert len(segments) == 3


class TestInsertDataToDb:
    @pytest.mark.asyncio
    @patch("service.brain_analysis.get_supabase_client")
    async def test_inserts_correct_rows(self, mock_get_sb):
        mock_table = MagicMock()
        mock_table.insert.return_value.execute.return_value = MagicMock(
            data=[{"id": 1}, {"id": 2}]
        )
        mock_sb = MagicMock()
        mock_sb.table.return_value = mock_table
        mock_get_sb.return_value = mock_sb

        from service.brain_analysis import insert_data_to_db

        seg1 = MagicMock(start=0.0, duration=1.0)
        seg2 = MagicMock(start=1.0, duration=1.0)
        preds = np.array([[0.1, 0.2], [0.3, 0.4]])

        result = await insert_data_to_db(preds, [seg1, seg2], "test_source", "user1")

        mock_sb.table.assert_called_once_with("predictions")
        mock_table.insert.assert_called_once()
        rows = mock_table.insert.call_args[0][0]
        assert len(rows) == 2
        assert rows[0]["user_id"] == "user1"
        assert rows[0]["raw_text"] == "test_source"
        assert rows[0]["timepoint"] == 0.0
        assert rows[0]["activations"] == [0.1, 0.2]
        assert len(result) == 2


class TestSaveBrainAnalysisResults:
    @pytest.mark.asyncio
    @patch("service.brain_analysis.insert_data_to_db")
    @patch("service.brain_analysis.predict_from_html")
    async def test_text_pipeline(self, mock_predict, mock_insert):
        mock_predict.return_value = (np.zeros((2, 10)), ["s1", "s2"])
        mock_insert.return_value = [{"id": 1}, {"id": 2}]

        from service.brain_analysis import save_brain_analysis_results

        preds, segments = await save_brain_analysis_results("<p>hello</p>", "user1")

        mock_predict.assert_called_once_with("<p>hello</p>")
        mock_insert.assert_called_once()
        assert preds.shape == (2, 10)
        assert len(segments) == 2
