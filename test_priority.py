from app import classify_priority

def test_high():
    priority, matches = classify_priority("This is urgent and not working")
    assert priority == "High"
    assert "urgent" in matches

def test_medium():
    priority, matches = classify_priority("The application is slow and there is a delay")
    assert priority == "Medium"
    assert "slow" in matches

def test_low():
    priority, matches = classify_priority("Please provide account information")
    assert priority == "Low"
    assert matches == []

if __name__ == "__main__":
    test_high()
    test_medium()
    test_low()
    print("All priority classification tests passed.")
