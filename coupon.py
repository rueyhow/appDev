import shelve, random, string, math, itertools, os.path
from typing import List
__path__ = os.path.dirname(__file__)
DBNAME = f'{__path__}/CouponDB'

def generateAmount() -> int:
    '''Generates a random int from 2-20'''
    return random.choice([2,3,4,5,6,7,8,9,10]*8 + [11,12,13,14,15,16,17,18,19,20])
    
def generateCoupon() -> None:
    '''Inserts feedback object into the database'''
    with shelve.open(DBNAME) as db:
        while True: #(26*2)+9 ^12 combinations of coupon codes
            newid = ''.join(random.choices(string.ascii_letters + string.digits, k = 12)) #prevent enumeration of users
            if newid not in db: #make sure key is not already in db
                db[newid] = generateAmount()
                return

def customCoupon(coupon : str, discount: int) -> bool:
    '''Inserts custom coupon into the database'''
    with shelve.open(DBNAME) as db:
        if coupon not in db:
            if isinstance(discount, int):
                db[coupon] = discount
                return True
    return False

def redeem(coupon : str) -> int: 
    '''redeems the coupon code
    returns % if the deletion is successful'''
    with shelve.open(DBNAME) as db:
        try:
            discount = db[coupon]
            del db[coupon]
            return discount
        except KeyError: 
            return 0

def deleteAll() -> bool: #is not imported with *
    '''deletes all coupon code in shelve'''
    with shelve.open(DBNAME) as db:
        try:
            for id in db.keys():
                del db[id]
            return True
        except KeyError: return False

def traversePage(page: int, increment_level : int) -> List[tuple]:
    with shelve.open(DBNAME) as db:
        length = len(db)
        maxpages = math.ceil(length/increment_level)
        if 0 < page <=maxpages :
            return list(itertools.islice(db.items(), page*increment_level, page*increment_level+increment_level))
        else: return list()
if __name__ == '__main__':
    # deleteAll()
    # for i in range(20):
    #     generateCoupon()
    # print(customCoupon('huathuat88', 90))
    '''Uses rich library'''
    import rich.table
    import rich.console
    # table = rich.table.Table(title="coupon")
    # table.add_column("coupon", style= "green")
    # table.add_column("%", style="blue")
    # with shelve.open(DBNAME) as db:
    #     for key, value in db.items():
    #         table.add_row(key, str(value))
    #     console = rich.console.Console()
    #     console.print(table)
    # while 1:
    #     table = rich.table.Table(title="coupon")
    #     table.add_column("coupon", style= "green")
    #     page = input("Enter page to traverse to: ")
    #     table.add_column("%", style="blue")
    #     for key, value in traversePage(page, increment_level=5):
    #         table.add_row(key, str(value))
    #     console = rich.console.Console()
    #     console.print(table)

    '''statistics'''
    # import statistics
    # dataset = [generateAmount() for _ in range(1000000)] #dataset of 1million
    # print(statistics.mean(dataset)) #7.1
    # print(statistics.median(dataset)) #7
__all__ = ['redeem', 'generateCoupon', 'customCoupon']
