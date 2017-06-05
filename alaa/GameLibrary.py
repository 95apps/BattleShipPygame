def save(ScoresDictionary):
    """
    A function that will save the name of the winning player, time, number of moves,  as
    a CSV file

    Parameters: recent version of trip dictionary with
    stop info
    Returns: ElephantTrip
    Process:
    - open CSV file to write over
    - initialize variable for each entry
    - for loop with decision structure to make sure each
    log entry has all information associated with its key
    - write each entry into the file
    """
    Scores = open ("HighscoreValues.csv","w+")
    for i in ScoresDictionary.values():
        x = ""
        for record in range(0,len(i)):
            if record == len(i)-1:
                x += str(i[record ])+ '\n'
            else:
                x += str(i[record ])+","
        Scores.write(x)
    return (Scores)

def openShow(showScore):
    """
    A function that will convert any Csv file to a medium that can be shown in python shell

    Parameters: show(opened csv file)
    Returns: csvReader1
    Process:
    - imports function csv
    - uses function .reader()
    - csvReader1 is the printable version of one line of csv
    - returns csvReader1
    """
    import csv
    csvReader1 = csv.reader(showScore)
    return csvReader1
