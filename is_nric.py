# variables & function to check nric/fin
NRIC_PTN = re.compile("^[FSTG]\d{7}[ABCDEFGHIJKLMNPQRTUWXZ]$")
NRIC_WEIGHT = [2, 7, 6, 5, 4, 3, 2]
FG_postfix = "-KLMNPQRTUWX"
ST_postfix = "-ABCDEFGHIZJ"

def is_nric(nric):
    if NRIC_PTN.match(nric):
        zvalue = 4 if nric[0] in 'TG' else 0
        numbers = [int(n) for n in nric[1:8]]        
        weighted = zvalue + sum(x * y for x, y in zip(numbers, NRIC_WEIGHT))
        checksum = 11 - (weighted % 11)
        postfix = FG_postfix[checksum] if nric[0] in 'FG' else ST_postfix[checksum]
        if postfix == nric[-1]:
            return True
#        else:
#            print("Wrong postfix")
#    else:
#        print("wrong pattern")
    return False

###### use the function #####
# test data 1 - direct call
is_nric('S7509183X')

# test data 2 - data is in a dataframe - single column ID
data = [
    ['ID', 'S1234567S']
]
df = pd.DataFrame(data=data, columns = ['ID'])

# vectorize the new column
# assign the result checking into the new column
is_nric_col = np.vectorize(is_nric)
df = df.assign(IsCorrectNRIC=is_nric_col(df['ID']))

# retrive the list of incorrect result only
df[~df['IsCorrectNRIC']]

# use the new column and update the value to differentiate nric or fin or not nric/fin
df.assign(id_type = df['IsCorrectNRIC'])
df.loc[df['IsCorrectNRIC'] & df['ID'].str.startswith('S'), 'id_type'] = 'NRIC'
df.loc[df['IsCorrectNRIC'] & df['ID'].str.startswith('T'), 'id_type'] = 'NRIC'
df.loc[df['IsCorrectNRIC'] & df['ID'].str.startswith('F'), 'id_type'] = 'FIN'
df.loc[df['IsCorrectNRIC'] & df['ID'].str.startswith('G'), 'id_type'] = 'FIN'
df.loc[~df['IsCorrectNRIC'], 'id_type'] = 'Not NRIC-FIN'
