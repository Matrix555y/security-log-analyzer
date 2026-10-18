from analyzer import count_events, find_repeated_failed_logins


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


def test_repeated_failed_logins():
    log_lines =[
        "[ERROR] Failed login for user admin",
        "[ERROR] Failed login for user admin",
        "[ERROR] Failed login for user admin", 
        "[ERROR] Failed login for user guest",  
    ]

    result = find_repeated_failed_logins(log_lines)

    assert result == {"admin":3}

def test_no_repeated_failed_logins():
    log_lines= [
        "[ERROR] Failed login for user admin",
        "[ERROR] Failed login for user guest",
    ]

    result = find_repeated_failed_logins(log_lines)

    assert result =={}


def test_empty_log_for_failed_logins():
    result = find_repeated_failed_logins([])

    assert result == {}

    test_repeated_failed_logins()
    test_no_repeated_failed_logins()
    test_empty_log_for_failed_logins()

print("All 6 tests passed!")