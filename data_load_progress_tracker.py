
def fun():
    print('be patient and wait 100s for first results')
    height = 510000
    old = col.count()
    time.sleep(100)
    while True:
        new = col.count()
        print('number of blocks inserted: {}, being {}% of all, and {}h left'.format(
            new, 
            str(100 * new / height )[:4],
            str(100 * (height - new) / ((new - old) * 3600))[:4]
        ))
        old = new
        time.sleep(100)

if __name__ == '__main__':
    fun()
