import click
import csv
import os
from datetime import datetime

@click.command()
@click.argument("method",default="list")
@click.option('--description', default="" )
@click.option('--amount',default=0.0)
@click.option('--id',type=int)
@click.option('--month',type=int)


def main(method,description="",amount=0.0,id=None,month=None):
    if os.path.exists('expense.csv'):
        with open('expense.csv','r') as file:
            reader = csv.reader(file)
            next(reader,None)
            data=list(reader)

    else:
        data=[]
    
    if method == "add":
        if description and amount:
            new_id=len(data)+1
            data.append([new_id,description,str(datetime.now().date()),float(amount)])
            with open('expense.csv','w',newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Description", "Date", "Amount"])
                writer.writerows(data)

            print(f"Added expense: {new_id}")
        else:
            print("please provide both description and amount.")

    elif method == "list":
        if data:
            try:
                total = 0
                if month:
                    print("Your current expenses for month {}: ".format(month))
                    for row in data:
                        if datetime.strptime(row[2],'%Y-%m-%d').month == month:
                            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                            total += float(row[3])
                    print("Total expenses for month {}: {}".format(month,total))
                else:
                    print("Your current expenses: ")
                    for row in data:
                        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        total += float(row[3])
                    print(f"Total expenses: {total}")
            except ValueError:
                print("Error processing dates.")
        else:
            print("No expenses found.")

    elif method == "delete":
        if data and id is not None:
            try:
                data = [row for row in data if int(row[0]) != id]
                
                with open('expense.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Description", "Date", "Amount"])
                    writer.writerows(data)
                
                print(f"Deleted expense with ID: {id}")
            except ValueError:
                print("Invalid ID format.")
        else:
            print("No valid ID provided or no expenses found.")

    elif method == 'summary':
        if data:
            try:
                total = 0
                if m:
                    total = sum(float(row[3]) for row in data if datetime.strptime(row[2], '%Y-%m-%d').month == month)
                else:
                    total = sum(float(row[3]) for row in data)
                print(f"Total expenses: {total}")
            except ValueError:
                print("Error processing dates.")
        else:
            print("No expenses to summarize.")
            
if __name__ == '__main__':
    main()

    

    

