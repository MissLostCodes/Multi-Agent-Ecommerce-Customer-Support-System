def test_pipeline():
    from app.main import workflow
    result = workflow.run("Damaged item refund")
    assert result is not None
