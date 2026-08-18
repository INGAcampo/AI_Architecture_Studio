from aias_next083_queue_report import QueueReport

def test_report_counts_pending_items():
    result = QueueReport().generate([{"queue_status": "PENDING_REVIEW"}, {"queue_status": "PENDING_REVIEW"}])
    assert result == {"report": "AIAS-NEXT-083", "total": 2, "pending_review": 2, "approved": 0}
