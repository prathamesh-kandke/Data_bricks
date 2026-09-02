from ex import expense
import calendar
import datetime

def main():
    print('run ho raha h ky check kar rahe h!!! ')

    expense_file_path = "expenses.csv"
    budget = 150000

    expense_chk = check_expense()
    save_file(expense_chk,expense_file_path)
    summerise_expense(expense_file_path,budget)


def check_expense():
    print('ky kharcha karne wale h ?')

    expense_name = input("where do you spend the money : ")
    expense_amount = eval(input('kitna kharcha kiya h ? :'))

    expense_category = ["Food","Travel","Fun","Work","Misc"]

    while True:
        print('Konse category me kharcha kar rahe ho ? ')

        for i,category_name in enumerate(expense_category):
            print(f'{i+1}.{category_name}')

        value_range = f"[1 - {len(expense_category)}]"
        select_index = int(input(f'category bata do : {value_range} : '))-1

        if select_index in range(len(expense_category)):
            selected_category = expense_category[select_index]
            print(selected_category)


            new_expense = expense(name=expense_name,amt=expense_amount,cat=selected_category)

            return new_expense
        else:
            print('Invalid category')

        break 



def save_file(expense_chk:expense,expense_file_path):
    print("Kharcha file me save kar rahe h !!!")
    with open(expense_file_path,'a',encoding='utf-8') as f:
        f.write(f'{expense_chk.name},{expense_chk.amount},{expense_chk.category}\n')



def summerise_expense(expense_file_path,budget):
    print("Hum summary bana rahe h!!")
    expenses :list[expense] =  []
    with open(expense_file_path,'r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            #print(line)
            expense_name,expense_amount,expense_category = line.strip().split(",")
            print(f'{expense_name} {expense_amount} {expense_category}')
            line_expense = expense(
                name =expense_name,
                amt=float(expense_amount),
                cat=expense_category
            )
            expenses.append(line_expense)
        print(expenses)
    
    amount_by_category = {}
    for e in expenses:
        key = e.category
        if key in amount_by_category:
            amount_by_category[key] += e.amount
        else:
            amount_by_category[key]= e.amount
    print('ye apka category wise kharcha h')
    for key,amount in amount_by_category.items():
        print(f'{key} : Rs.{amount:.2f}')
    
    total_kharcha = sum([x.amount for x in expenses])
    print(f'Itna kharcha hua h : Rs.{total_kharcha} \-')

    remaining_amount = budget - total_kharcha
    print(f'Itne paise bake h : Rs.{remaining_amount}')

    now = datetime.datetime.now()
    day_in_month = calendar.monthrange(now.year,now.month)[1]
    remaining_days = day_in_month - now.day

    daily_budget = remaining_amount /remaining_days
    print(f'Budget per day : Rs.{daily_budget:.2f}')



if __name__ == "__main__":
    main()

