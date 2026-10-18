from analyzer import count_events


def test_count_events():
    log_lines = [
        "[INFO] Server started",
        "[WARNING] Multiple login attempts",
        "[ERROR] Login failed",
        "[INFO] User logged in",
        "[DEBUG] Database checked"
    ]

    counts, errors, unknown = count_events(log_lines)


    assert counts["INFO"] == 2
    assert counts["WARNING"] == 1 
    assert counts["ERROR"] == 1 


    assert len(errors)== 1
    assert len(unknown)==1
    assert unknown[0] == "[DEBUG] Database checked"



def test_empty_log():
    counts,errors, unknown =count_events([])

    assert counts == {

        "INFO": 0,
        "WARNING":0,
        "ERROR":0,

    }

    assert errors ==[]
    assert unknown == []

def test_blank_lines():
    counts,errors, unknown = count_events(["","  ", "\n"])

    assert sum(counts.values())== 0
    assert errors == []
    assert unknown ==[]

test_count_events()
test_empty_log()
test_blank_lines()

print("All 3 tests passed!")